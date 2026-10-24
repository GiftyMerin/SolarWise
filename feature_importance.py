
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor

# Load the merged dataset
data = pd.read_csv("data/Plant_1_Merged_Data.csv")
data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])

# Create time features
data["HOUR"] = data["DATE_TIME"].dt.hour
data["MINUTE"] = data["DATE_TIME"].dt.minute
data["DAY_OF_WEEK"] = data["DATE_TIME"].dt.dayofweek

# Define inputs and target
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

# Use the same chronological training split
split_index = int(len(data) * 0.8)
X_train = X.iloc[:split_index]
y_train = y.iloc[:split_index]

# Train Random Forest
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=12,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Extract and display feature importance
importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
}).sort_values("Importance", ascending=False)

print("\nFEATURE IMPORTANCE")
print(importance.to_string(index=False))

# Plot feature importance
plt.figure(figsize=(9, 5))
plt.barh(importance["Feature"], importance["Importance"])
plt.gca().invert_yaxis()
plt.title("Random Forest Feature Importance")
plt.xlabel("Importance Score")
plt.ylabel("Feature")
plt.tight_layout()

plt.savefig("data/feature_importance.png", dpi=150)
plt.show()
plt.close()

print("\nSaved data/feature_importance.png")
