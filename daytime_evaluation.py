
import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load dataset
data = pd.read_csv("data/Plant_1_Merged_Data.csv")
data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])

# Create time features
data["HOUR"] = data["DATE_TIME"].dt.hour
data["MINUTE"] = data["DATE_TIME"].dt.minute
data["DAY_OF_WEEK"] = data["DATE_TIME"].dt.dayofweek

features = [
    "IRRADIATION",
    "AMBIENT_TEMPERATURE",
    "MODULE_TEMPERATURE",
    "HOUR",
    "MINUTE",
    "DAY_OF_WEEK"
]

X = data[features]
y = data["AC_POWER"]

# Keep the same chronological train/test split
split_index = int(len(data) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]
y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

# Select daytime test records only
daytime_mask = X_test["IRRADIATION"] > 0
X_day = X_test.loc[daytime_mask]
y_day = y_test.loc[daytime_mask]

print("Total test records:", len(X_test))
print("Daytime test records:", len(X_day))
print("Daytime records with power > 0:", int((y_day > 0).sum()))

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

for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_day)

    results.append({
        "Model": name,
        "Daytime MAE": mean_absolute_error(y_day, predictions),
        "Daytime RMSE": np.sqrt(
            mean_squared_error(y_day, predictions)
        ),
        "Daytime R2": r2_score(y_day, predictions)
    })

results_df = pd.DataFrame(results)

print("\nDAYTIME MODEL COMPARISON")
print(results_df.to_string(index=False))

results_df.to_csv("data/daytime_model_comparison.csv", index=False)
print("\nSaved data/daytime_model_comparison.csv")
