# 📱 Teen Smartphone Addiction Predictor

> This app is part of my final project for the IT Academy Data Analytics course (Barcelona Activa). The full analysis, the Power BI dashboard and the presentation are in [it_academy_barcelona_activa](https://github.com/esrakesken/it_academy_barcelona_activa/tree/main/Lifestyle_Factors_on_Teen_Phone_Addiction).

An interactive web app that estimates a teenager's **smartphone addiction level on a 0–10 scale** from ten daily habits: screen time, social media, gaming, sleep, exercise and more.

🌐 **Live app:** [teenphone-addiction.streamlit.app](https://teenphone-addiction.streamlit.app/)

> ⚠️ Educational project. The app raises awareness of phone habits; it is **not** a clinical or diagnostic tool.

## What it does

1. In the sidebar, enter the teenager's habits (hours of use, phone checks per day, sleep, exercise, parental control…).
2. Press **Predict Addiction Level**.
3. The app shows:
   - the predicted level, for example **7.85 / 10**;
   - a risk message: ✅ low (< 4), ⚠️ moderate (4–7) or 🚨 high (≥ 7);
   - a histogram of all teenagers in the dataset, with a red line marking where the prediction falls.

## Data

- **Teen Smartphone Usage and Addiction Impact Dataset** (Kaggle): 3,000 teenagers, 25 columns.
- The dataset is **synthetic**: names and towns are generated, so it contains no real personal data.
- The target `Addiction_Level` is very skewed: the average is 8.9, half of the rows are exactly 10, and 86 % are 7 or higher.

## Model

| | |
|---|---|
| Algorithm | Random Forest Regressor (scikit-learn, 200 trees) |
| Inputs | 10 features a teenager or parent can answer (below) |
| Split | 80 % train / 20 % test (`random_state=42`) |

**Features:** daily usage hours, apps used daily, time on social media, time on gaming, phone checks per day, sleep hours, weekend usage hours, academic performance, exercise hours, parental control.

**Results on the test set (600 teenagers):**

| Metric | Random Forest | Baseline (always predict the mean) |
|---|---|---|
| MAE | **0.36** | 1.28 |
| RMSE | 0.53 | — |
| R² | **0.89** | 0 |

On average the prediction is about a third of a point away from the real level, compared with 1.3 points for the baseline.

**What matters most to the model:** daily usage hours (43 % of the importance), followed by apps used, social media time and gaming time (about 12 % each). Parental control has almost no weight.

## Run it locally

```bash
git clone https://github.com/esrakesken/teen_phone_addiction_app.git
cd teen_phone_addiction_app
pip install -r teen_phone_app/requirements.txt
streamlit run teen_phone_app/app.py
```

Run the commands from the repository root: the app reads the data from `teen_phone_app/`.

## Project structure

```
teen_phone_addiction_app/
├── README.md
└── teen_phone_app/
    ├── app.py                             # model training + Streamlit app
    ├── addiction_model_simple.pkl         # trained Random Forest
    ├── teen_phone_addiction_dataset.csv   # dataset (3,000 rows)
    └── requirements.txt
```

## Limitations

- **Synthetic data:** the results show what the model learned from this dataset, not how real teenagers behave.
- **Skewed target:** with so many 10s, the model has seen few low-addiction cases, so low predictions are less reliable.
- **Single train/test split:** the metrics come from one split; cross-validation would give a more stable estimate.
- **Training at start-up:** `app.py` retrains the model every time the app starts, which makes start-up slower.

## Possible improvements

- Move training to its own script (`train.py`) and keep `app.py` only for the interface.
- Evaluate with cross-validation and compare with simpler models (linear regression) and other ensembles.
- Show which inputs pushed the prediction up or down for each teenager (e.g. with SHAP).

## Tools

Python · Pandas · NumPy · scikit-learn · Matplotlib · Streamlit · Streamlit Community Cloud

## Author

**Esra Kesken** · [GitHub](https://github.com/esrakesken) · [LinkedIn](https://www.linkedin.com/in/esrakesken)
