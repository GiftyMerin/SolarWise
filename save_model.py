
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor

data = pd.read_csv("data/Plant_1_Merged_Data.csv")
data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])

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

# Train on the first 80% of timestamps
split_index = int(len(data) * 0.8)

model = RandomForestRegressor(
    n_estimators=100,
    max_depth=12,
    random_state=42,
    n_jobs=-1
)

model.fit(X.iloc[:split_index], y.iloc[:split_index])

joblib.dump(
    model,
    "data/solar_power_model.joblib"
)

print("Model saved successfully!")
