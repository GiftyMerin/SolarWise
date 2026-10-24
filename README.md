#  SolarWise — Predictive Green Energy

A machine learning project for estimating household solar power generation using environmental and time-based features.

##  Project Overview

SolarWise uses a trained machine learning model to estimate solar power output based on factors such as solar irradiation, ambient temperature, module temperature, and time of day.

The project also includes data exploration, model evaluation, feature importance analysis, and a Streamlit interface for interactive predictions.

##  Features

- Interactive Streamlit application
- Solar power prediction using a trained Random Forest model
- Environmental and time-based input features
- Exploratory data analysis and visualizations
- Model comparison and evaluation
- Feature importance analysis

##  Tech Stack

- **Language:** Python
- **Machine Learning:** scikit-learn
- **Data Processing:** pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Web Application:** Streamlit
- **Model Persistence:** Joblib

##  Project Structure

```text
predictive-green-energy/
├── app.py
├── main.py
├── train_model.py
├── save_model.py
├── eda.py
├── feature_importance.py
├── daytime_evaluation.py
├── requirements.txt
├── .gitignore
└── data/
    ├── solar_power_model.joblib
    ├── correlation_heatmap.png
    ├── feature_importance.png
    ├── irradiation_vs_power.png
    ├── model_comparison.csv
    ├── model_predictions.png
    ├── power_over_time.png
    └── daytime_model_comparison.csv
```

##  Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/GiftyMerin/SolarWise-Predictive-Green-Energy.git
cd SolarWise-Predictive-Green-Energy
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
streamlit run app.py
```

##  Model Evaluation

The project includes scripts for model training, model comparison, feature importance, and daytime evaluation. Evaluation results and visualizations are available in the `data/` directory.

##  Dataset

The original generation and weather CSV files are excluded from Git using `.gitignore`. You may need to obtain the dataset separately to retrain the model.

The saved model is included so the application can load it without retraining, provided the model file is compatible with the installed dependencies.

## Author

**Gifty Merin**

GitHub: [@GiftyMerin](https://github.com/GiftyMerin)
