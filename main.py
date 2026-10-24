
import pandas as pd
import numpy as np

# 1. Load the datasets
generation = pd.read_csv(
    "data/Plant_1_Generation_Data.csv"
)

weather = pd.read_csv(
    "data/Plant_1_Weather_Sensor_Data.csv"
)

# 2. Convert timestamps
generation["DATE_TIME"] = pd.to_datetime(
    generation["DATE_TIME"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)

weather["DATE_TIME"] = pd.to_datetime(
    weather["DATE_TIME"],
    errors="coerce"
)

generation = generation.dropna(
    subset=["DATE_TIME"]
)

weather = weather.dropna(
    subset=["DATE_TIME"]
)

# 3. Aggregate inverter power at each timestamp
plant_generation = (
    generation
    .groupby("DATE_TIME", as_index=False)
    .agg(
        AC_POWER=("AC_POWER", "sum"),
        DC_POWER=("DC_POWER", "sum")
    )
)

print("Generation timestamps:",
      len(plant_generation))

# 4. Keep the weather measurements
weather_clean = weather[
    [
        "DATE_TIME",
        "AMBIENT_TEMPERATURE",
        "MODULE_TEMPERATURE",
        "IRRADIATION"
    ]
].copy()

# 5. Merge on timestamp
data = pd.merge(
    plant_generation,
    weather_clean,
    on="DATE_TIME",
    how="inner",
    validate="one_to_one",
    indicator=True
)

print("\nMerge results:")
print(data["_merge"].value_counts())

data = data.drop(columns=["_merge"])
data = data.sort_values("DATE_TIME").reset_index(
    drop=True
)

# 6. Inspect the merged dataset
print("\nMerged dataset shape:", data.shape)
print("\nColumn names:")
print(data.columns.tolist())

print("\nFirst five rows:")
print(data.head())

print("\nMissing values:")
print(data.isnull().sum())

# 7. Save the merged dataset
data.to_csv(
    "data/Plant_1_Merged_Data.csv",
    index=False
)

print("\nMerged dataset saved successfully!")
