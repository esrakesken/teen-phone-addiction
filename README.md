# 📱 Teen Smartphone Addiction: Lifestyle Factors

Final project of the **IT Academy Data Analytics course (Barcelona Activa)**. It studies how daily habits relate to smartphone addiction in teenagers and goes from analysis to a working product:

| Part | What it answers | Where |
|---|---|---|
| 1. Exploratory analysis | Which habits go together with higher addiction? | [`notebooks/01_eda_analysis.ipynb`](notebooks/01_eda_analysis.ipynb) |
| 2. Clustering (K-Means) | Addiction is high almost everywhere, so how does it affect teenagers differently? | [`notebooks/02_regression_and_clustering.ipynb`](notebooks/02_regression_and_clustering.ipynb) |
| 3. Regression | Can we predict the addiction level from habits? | [`notebooks/02_regression_and_clustering.ipynb`](notebooks/02_regression_and_clustering.ipynb), [`notebooks/03_app_model.ipynb`](notebooks/03_app_model.ipynb) |
| 4. Power BI dashboard | Interactive view of the findings | [`dashboard/`](dashboard/) |
| 5. Streamlit app | Estimate the level for one teenager | [`teen_phone_app/`](teen_phone_app/) |

📊 **Presentation:** [`presentation/final_project_presentation.pdf`](presentation/final_project_presentation.pdf)
🌐 **Live app:** [teenphone-addiction.streamlit.app](https://teenphone-addiction.streamlit.app/)

> ⚠️ Educational project. The app raises awareness of phone habits; it is **not** a clinical or diagnostic tool.

## 1. Exploratory analysis

Main findings:

- Addiction rises as daily usage rises: a **strong positive trend**.
- Many teenagers sit at the **highest level (10)**.
- **Gender** shows no meaningful effect on addiction.
- Some teenagers show high addiction even with **low daily usage**, so screen time alone does not explain everything.

## 2. Clustering: three profiles of teenagers

Because almost everyone in the dataset is highly addicted, the question became **how** that addiction shows up in their lives. I grouped the teenagers with **K-Means**:

- **Features:** daily usage, sleep, social media, gaming, study time, academic performance, self-esteem, anxiety, depression and parental control.
- **Preprocessing:** `StandardScaler`, because K-Means works with distances.
- **Choosing k:** elbow method (WCSS for k = 1–10) → **k = 3**.

| Cluster | Profile | Daily use (h) | Academic perf. | Anxiety | Depression | Parental control |
|---|---|---|---|---|---|---|
| 0 · Low risk | **Resilient Adolescents** | 5.0 | 73.8 | 2.7 | 5.1 | 0.50 |
| 1 · Medium risk | **High-Functioning Anxious Adolescents** | 4.2 | 81.0 | 7.7 | 4.5 | 0.43 |
| 2 · High risk | **Vulnerable Adolescents** | 5.9 | 69.6 | 6.9 | 6.9 | 0.61 |

- **Resilient:** moderate grades, balanced parental control and low anxiety; emotionally stable despite high digital use. *Support:* digital literacy and healthy usage habits.
- **High-Functioning Anxious:** best grades and more educational use, but less parental control and high anxiety; ambitious yet emotionally strained. *Support:* stress management and emotional regulation.
- **Vulnerable:** lowest grades, highest depression and longest usage, despite the highest parental control. *Support:* mentoring, emotional support, less overuse and renewed school engagement.

**Takeaway:** the addiction level is about the same in all three groups (≈ 9/10), but its **impact is different**, which calls for a different intervention for each profile. Parental control on its own is not enough: the most controlled group is the most vulnerable.

Cluster averages: [`data/Cluster_Summary.csv`](data/Cluster_Summary.csv)

## 3. Regression: predicting the addiction level

First comparison, with all the habit and well-being features (test set):

| Model | MAE | RMSE | R² |
|---|---|---|---|
| Linear Regression | 1.10 | 1.34 | 0.29 |
| **Random Forest** | **0.37** | **0.59** | **0.86** |

The relationship is clearly non-linear, so Random Forest wins by far. For the app I then trained a **simpler Random Forest** that only uses ten questions a teenager or parent can answer (see [The app](#5-the-app) below). Predictions on the test set: [`data/Addiction_Predictions.csv`](data/Addiction_Predictions.csv)

## 4. Power BI dashboard

[`dashboard/teen_phone_addiction_dashboard.pbix`](dashboard/teen_phone_addiction_dashboard.pbix) brings together the analysis, the cluster profiles and the predictions in an interactive report (open it with Power BI Desktop).

## 5. The app

An interactive web app that estimates a teenager's **smartphone addiction level on a 0–10 scale** from ten daily habits: screen time, social media, gaming, sleep, exercise and more.

### What it does

1. In the sidebar, enter the teenager's habits (hours of use, phone checks per day, sleep, exercise, parental control…).
2. Press **Predict Addiction Level**.
3. The app shows:
   - the predicted level, for example **7.85 / 10**;
   - a risk message: ✅ low (< 4), ⚠️ moderate (4–7) or 🚨 high (≥ 7);
   - a histogram of all teenagers in the dataset, with a red line marking where the prediction falls.

### Data

- **Teen Smartphone Usage and Addiction Impact Dataset** (Kaggle): 3,000 teenagers, 25 columns.
- The dataset is **synthetic**: names and towns are generated, so it contains no real personal data.
- The target `Addiction_Level` is very skewed: the average is 8.9, half of the rows are exactly 10, and 86 % are 7 or higher.

### App model

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
├── notebooks/
│   ├── 01_eda_analysis.ipynb               # exploratory analysis
│   ├── 02_regression_and_clustering.ipynb  # model comparison + K-Means
│   └── 03_app_model.ipynb                  # simplified model used by the app
├── data/
│   ├── Cluster_Summary.csv                 # average profile of each cluster
│   └── Addiction_Predictions.csv           # test-set predictions
├── dashboard/
│   └── teen_phone_addiction_dashboard.pbix # Power BI report
├── presentation/
│   └── final_project_presentation.pdf
└── teen_phone_app/
    ├── app.py                             # model training + Streamlit app
    ├── addiction_model_simple.pkl         # trained Random Forest
    ├── teen_phone_addiction_dataset.csv   # dataset (3,000 rows)
    └── requirements.txt
```

The notebooks are kept exactly as they were run during the course, outputs included. To run them again, point `pd.read_csv(...)` to `../teen_phone_app/teen_phone_addiction_dataset.csv`.

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
