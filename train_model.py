
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("Loading solar dataset...")

# 1. Load the merged dataset
data = pd.read_csv("data/Plant_1_Merged_Data.csv")
data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])

# 2. Create time-based features
data["HOUR"] = data["DATE_TIME"].dt.hour
data["MINUTE"] = data["DATE_TIME"].dt.minute
data["DAY_OF_WEEK"] = data["DATE_TIME"].dt.dayofweek

# 3. Select input features and target
features = [
    "IRRADIATION",
    "AMBIENT_TEMPERATURE",
    "MODULE_TEMPERATURE",
    "HOUR",
    "MINUTE",
    "DAY_OF_WEEK"
]

target = "AC_POWER"

X = data[features]
y = data[target]

# 4. Split chronologically: earlier data for training,
#    later data for testing
split_index = int(len(data) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))

# 5. Train two models
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(
        n_estimators=100,
        max_depth=12,
        random_state=42,
        n_jobs=-1
    )
}

results = []
predictions = {}

for name, model in models.items():
    print(f"\nTraining {name}...")

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    results.append({
        "Model": name,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    })

    predictions[name] = y_pred

# 6. Display evaluation results
results_df = pd.DataFrame(results)

print("\nMODEL COMPARISON")
print(results_df.to_string(index=False))

# 7. Plot actual versus predicted power
plt.figure(figsize=(12, 5))

plt.plot(
    y_test.iloc[:200].to_numpy(),
    label="Actual AC Power",
    linewidth=2
)

for name, y_pred in predictions.items():
    plt.plot(
        y_pred[:200],
        label=name,
        alpha=0.8
    )

plt.title("Actual vs Predicted Solar AC Power")
plt.xlabel("Test Sample (15-minute intervals)")
plt.ylabel("AC Power")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("data/model_predictions.png", dpi=150)
plt.show()

# 8. Save model comparison results
results_df.to_csv("data/model_comparison.csv", index=False)

print("\nSaved model_comparison.csv and model_predictions.png")
