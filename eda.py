
print("Starting Exploratory Data Analysis...")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Load the merged dataset
data = pd.read_csv("data/Plant_1_Merged_Data.csv")
data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])

print("Dataset loaded successfully!")
print("Dataset shape:", data.shape)
print(data.head())

# Create output folder if it does not exist
Path("data").mkdir(exist_ok=True)

# Graph 1: Solar power over time
plt.figure(figsize=(14, 5))
plt.plot(data["DATE_TIME"], data["AC_POWER"], linewidth=1)
plt.title("Solar Power Generation Over Time")
plt.xlabel("Date and Time")
plt.ylabel("Total AC Power")
plt.xticks(rotation=45)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("data/power_over_time.png", dpi=150)
plt.show()
plt.close()

# Graph 2: Irradiation vs solar power
plt.figure(figsize=(8, 5))
sns.scatterplot(data=data, x="IRRADIATION", y="AC_POWER", alpha=0.5)
plt.title("Irradiation vs Solar AC Power")
plt.xlabel("Irradiation")
plt.ylabel("Total AC Power")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("data/irradiation_vs_power.png", dpi=150)
plt.show()
plt.close()

# Graph 3: Correlation heatmap
columns = [
    "AC_POWER",
    "DC_POWER",
    "AMBIENT_TEMPERATURE",
    "MODULE_TEMPERATURE",
    "IRRADIATION"
]

correlation = data[columns].corr()

plt.figure(figsize=(9, 6))
sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    vmin=-1,
    vmax=1
)
plt.title("Correlation Between Solar Power and Weather")
plt.tight_layout()
plt.savefig("data/correlation_heatmap.png", dpi=150)
plt.show()
plt.close()

print("\nAll three graphs have been saved in the data folder!")
