import streamlit as st
import numpy as np
import pickle
from datetime import datetime

# Load trained model
model = pickle.load(open("loan_model.pkl", "rb"))

# Page config
st.set_page_config(page_title="Loan Approval Predictor", page_icon="🏦", layout="centered")

# CSS
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #0e1117;
    color: white;
    text-align: center;
    padding: 10px;
}
.footer img {
    width: 28px;
    margin: 0 10px;
    vertical-align: middle;
    cursor: pointer;
}
.statement-box {
    border: 2px solid #0e1117;
    border-radius: 10px;
    padding: 20px;
    background-color: #f8f9fa;
    font-family: monospace;
}

/* Light theme text */
@media (prefers-color-scheme: light) {
    .statement-box {
        color: black;
        background-color: #f8f9fa;
    }
}

/* Dark theme text */
@media (prefers-color-scheme: dark) {
    .statement-box {
        color: white;
        background-color: #1e1e1e;
        border: 2px solid #ffffff;
    }
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🏦 Loan Approval Prediction System")
st.markdown("### Enter customer details to check loan status")

st.divider()

# User name
customer_name = st.text_input("Customer Name")

col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
    married = st.selectbox("Married", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])

with col2:
    self_employed = st.selectbox("Self Employed", ["Yes", "No"])
    applicant_income = st.number_input("Applicant Income", min_value=0)
    coapplicant_income = st.number_input("Coapplicant Income", min_value=0)
    loan_amount = st.number_input("Loan Amount", min_value=0)
    loan_term = st.number_input("Loan Amount Term", min_value=1)
    credit_history = st.selectbox("Credit History", [1, 0])
    property_area = st.selectbox("Property Area", ["Rural", "Semiurban", "Urban"])

# Encoding
gender = 1 if gender == "Male" else 0
married = 1 if married == "Yes" else 0
education = 1 if education == "Graduate" else 0
self_employed = 1 if self_employed == "Yes" else 0
property_area = {"Rural":0, "Semiurban":1, "Urban":2}[property_area]
dependents = 4 if dependents == "3+" else int(dependents)

# Prediction
if st.button("💳 Check Loan Status"):

    if customer_name.strip() == "":
        st.warning("⚠️ Please enter Customer Name before checking loan status.")
    else:
        input_data = np.array([[gender, married, dependents, education,
                                self_employed, applicant_income, coapplicant_income,
                                loan_amount, loan_term, credit_history, property_area]])

        prediction = model.predict(input_data)[0]


    status = "APPROVED ✅" if prediction == 1 else "REJECTED ❌"
    time_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    statement = f"""
    -------- MINI LOAN STATEMENT --------
    Bank        : Rakshith Bank
    Customer    : {customer_name}
    Date/Time   : {time_now}

    Applicant Income   : {applicant_income}
    Loan Amount        : {loan_amount}
    Credit History     : {credit_history}

    LOAN STATUS : {status}
    ------------------------------------
    """

    st.subheader("🏦 Loan Statement")
    st.markdown(f"<div class='statement-box'><pre>{statement}</pre></div>", unsafe_allow_html=True)

    st.download_button(
        label="📥 Download Statement",
        data=statement,
        file_name="loan_statement.txt",
        mime="text/plain"
    )

# Footer
st.markdown("""
<div class="footer">
    Developed by <b>Rakshith</b>
    <a href="mailto:rakshithgowdaka09@gmail.com">
        <img src="https://cdn-icons-png.flaticon.com/512/732/732200.png">
    </a>
    <a href="https://www.linkedin.com/in/rakshithgowdahj/" target="_blank">
        <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png">
    </a>
</div>
""", unsafe_allow_html=True)
