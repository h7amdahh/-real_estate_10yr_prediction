import joblib
import pandas as pd
import streamlit as st

@st.cache_resource
def load_model():
    return joblib.load("real_estate_model.pkl")

model = load_model()
st.title("UAE Real Estate Trend Prediction")
st.caption("Explore recorded ten-year labels. The dataset has no verified property price history.")

with st.expander("Explore the training data and model comparison"):
    st.write("Training profiles labeled Increased, by emirate (%)")
    st.bar_chart(pd.read_csv("emirates.csv").set_index("City_Emirate"))
    st.write("Validation scores")
    st.dataframe(pd.read_csv("comparison.csv").round(3), hide_index=True)

values = {}
fields = ["City_Emirate", "Current_Housing", "Employment_Sector", "Preferred_Property_Type"]
options = model.named_steps["preprocess"].named_transformers_["categories"]["encode"].categories_
with st.form("profile"):
    for field, choices in zip(fields, options):
        values[field] = st.selectbox(field.replace("_", " "), choices)
    values["Annual_Income_AED"] = st.number_input("Annual income (AED)", min_value=0, value=180000)
    values["Monthly_Savings_AED"] = st.number_input("Monthly savings (AED)", min_value=0, value=4000)
    values["Debt_To_Income_Ratio"] = st.number_input("Debt-to-income ratio", min_value=0.0, value=0.30)
    values["Credit_Score"] = st.number_input("Credit score", 300, 900, 700)
    values["Existing_Properties"] = st.number_input("Existing properties", min_value=0, value=0)
    values["Estimated_Budget_AED"] = st.number_input("Property budget (AED)", min_value=0, value=700000)
    values["Mortgage_Interest_Rate_Pct"] = st.slider("Annual mortgage rate (%)", 0.0, 100.0, 4.5)
    submitted = st.form_submit_button("Predict")

if submitted:
    profile = pd.DataFrame([values])
    st.subheader("Predicted trend: " + model.predict(profile)[0])
    probabilities = pd.Series(model.predict_proba(profile)[0], index=model.classes_)
    st.write("Model probabilities (%)")
    st.bar_chart(probabilities.mul(100))
