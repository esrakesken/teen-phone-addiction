import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import numpy as np

df = pd.read_csv("teen_phone_app/teen_phone_addiction_dataset.csv")

selected_features = [
    'Daily_Usage_Hours',
    'Apps_Used_Daily',
    'Time_on_Social_Media',
    'Time_on_Gaming',
    'Phone_Checks_Per_Day',
    'Sleep_Hours',
    'Weekend_Usage_Hours',
    'Academic_Performance',
    'Exercise_Hours',
    'Parental_Control'
]
X = df[selected_features]
y = df["Addiction_Level"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


rf_simple = RandomForestRegressor(
    n_estimators=200,
    max_depth=None,
    random_state=42
)
rf_simple.fit(X_train, y_train)

y_pred = rf_simple.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("✅ Model Evaluation (Simplified Version)")
print(f"MAE: {mae:.3f}")
print(f"RMSE: {rmse:.3f}")
print(f"R²: {r2:.3f}")

joblib.dump(rf_simple, "addiction_model_simple.pkl")
print("💾 Model saved as 'addiction_model_simple.pkl'")

import streamlit as st
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt

# Page configuration 
st.set_page_config(page_title="Smartphone Addiction Predictor", page_icon="📱", layout="wide")

#Load Model 
@st.cache_resource
def load_model():
    return joblib.load("addiction_model_simple.pkl")

model = load_model()

# Title and Introduction
st.title("📱 Teen Smartphone Addiction Level Predictor")
st.write("""
This interactive web app estimates a teenager’s **Smartphone Addiction Level (0–10)** 
based on behavioral and lifestyle factors.
""")

st.markdown("---")

# Sidebar Inputs 
st.sidebar.header("Enter Behavioral & Lifestyle Factors")

daily_use = st.sidebar.slider("Daily Usage Hours", 0.0, 10.0,5.0)
apps = st.sidebar.slider("Daily Apps Used",5,20,10)
social = st.sidebar.slider("Time on Social Media (hours)", 0.0, 5.0, 2.0)
gaming = st.sidebar.slider("Time on Gaming (hours)", 0.0, 4.0, 2.0)
checks = st.sidebar.slider("Phone Checks Per Day (20–150)", 20, 150, 50)
sleep = st.sidebar.slider("Sleep Hours", 4.0, 10.0, 6.0)
weekend = st.sidebar.slider("Weekend usage (Hours)", 0, 14, 7)
academic = st.sidebar.slider("Academic Performance (0–100)", 0, 100, 75)
exercise = st.sidebar.slider("Exercise_Hours(0–4)", 0.0, 4.0, 2.0)
parental_control = st.sidebar.radio("Parental Control Enabled?", ["Yes", "No"])

parental_control_val = 1 if parental_control == "Yes" else 0

# Input DataFrame 
input_data = pd.DataFrame({
    'Daily_Usage_Hours': [daily_use],
    'Apps_Used_Daily': [apps],
    'Time_on_Social_Media': [social],
    'Time_on_Gaming': [gaming],
    'Phone_Checks_Per_Day': [checks],
    'Sleep_Hours': [sleep],
    'Weekend_Usage_Hours': [weekend],
    'Academic_Performance': [academic],
    'Exercise_Hours': [exercise],
    'Parental_Control': [parental_control_val]
})


# Prediction 
if st.sidebar.button("Predict Addiction Level"):
    prediction = model.predict(input_data)[0]
    st.subheader(f"Predicted Addiction Level: **{prediction:.2f} / 10**")

    # Risk message
    if prediction < 4:
        st.success("✅ Low Risk of Addiction — healthy phone habits!")
    elif prediction < 7:
        st.warning("⚠️ Moderate Risk — Consider limiting screen time.")
    else:
        st.error("🚨 High Risk of Addiction — Signs of digital overuse detected!")

    st.markdown("---")
    
    #Histogram adddiction level and prediction level
    try:
        data = pd.read_csv("teen_phone_app/teen_phone_addiction_dataset.csv") 
        addiction_values = data["Addiction_Level"]

        plt.figure(figsize=(7,4))
        plt.hist(addiction_values, bins=20, color="#1b1f6d", alpha=0.7, edgecolor='black')
        plt.axvline(prediction, color='red', linestyle='--', linewidth=2,
                    label=f"Your Prediction: {prediction:.2f}")
        plt.title("Distribution of Addiction Levels")
        plt.xlabel("Addiction Level (0–10)")
        plt.ylabel("Number of Individuals")
        plt.legend()
        st.pyplot(plt)

    except Exception as e:
        st.info(f"Couldn't load histogram data: {e}")

st.markdown( 
    """
    ---
    **About this App:**  
    The model uses machine learning (Random Forest Regressor) trained on anonymized teen behavior data 
    to predict smartphone addiction level on a 0–10 scale.  
    This tool is designed for educational awareness — not for clinical diagnosis.
    """

)



