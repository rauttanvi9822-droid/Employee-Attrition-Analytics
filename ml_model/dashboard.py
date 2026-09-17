import streamlit as st
import mysql.connector
import pandas as pd

# =========================================================
# EMPLOYEE ATTRITION ANALYTICS DASHBOARD
# =========================================================

st.set_page_config(
    page_title="Employee Attrition Analytics",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# DASHBOARD STYLE
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    margin-bottom: 25px;
}

.section-title {
    font-size: 24px;
    font-weight: 600;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)
# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("HR Analytics")
st.sidebar.write("Employee Attrition Dashboard")

st.sidebar.markdown("---")

st.sidebar.write("### Dashboard Sections")
st.sidebar.write("📊 Risk Overview")
st.sidebar.write("🏢 Department Analysis")
st.sidebar.write("🤖 ML Prediction")
st.sidebar.write("👥 High-Risk Employees")
st.sidebar.write("📈 Model Performance")
# =========================================================
# MYSQL DATABASE CONNECTION
# =========================================================

connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="Tanviraut@123",
    database="employee_attrition_db"
)

# =========================================================
# DASHBOARD TITLE
# =========================================================

st.markdown(
    '<div class="main-title">Employee Attrition Analytics Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">ML-Based HR Attrition Risk Analysis</div>',
    unsafe_allow_html=True
)

# =========================================================
# PROJECT OVERVIEW
# =========================================================

st.info(
    """
    **Project:** Employee Attrition Analytics

    This dashboard combines HR database analytics with a
    Machine Learning model to identify employees at different
    levels of attrition risk.

    **ML Model:** Logistic Regression
    """
)
# =========================================================
# LOAD ML RISK SUMMARY
# =========================================================

query = """
SELECT
    ml_risk_level,
    COUNT(*) AS employee_count
FROM ml_attrition_analytics
GROUP BY ml_risk_level;
"""

risk_data = pd.read_sql(query, connection)

# =========================================================
# CALCULATE METRICS
# =========================================================

total_employees = risk_data["employee_count"].sum()

low_risk = risk_data.loc[
    risk_data["ml_risk_level"] == "LOW",
    "employee_count"
].sum()

medium_risk = risk_data.loc[
    risk_data["ml_risk_level"] == "MEDIUM",
    "employee_count"
].sum()

high_risk = risk_data.loc[
    risk_data["ml_risk_level"] == "HIGH",
    "employee_count"
].sum()

# =========================================================
# DISPLAY METRICS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Employees", total_employees)
col2.metric("Low Risk", low_risk)
col3.metric("Medium Risk", medium_risk)
col4.metric("High Risk", high_risk)

# =========================================================
# ML RISK DISTRIBUTION
# =========================================================

st.subheader("ML Risk Distribution")

chart_data = risk_data.set_index("ml_risk_level")

st.bar_chart(
    chart_data["employee_count"]
)

# =========================================================
# ML RISK PERCENTAGE
# =========================================================

st.subheader("ML Risk Percentage")

risk_percentage = risk_data.copy()

risk_percentage["percentage"] = (
    risk_percentage["employee_count"]
    / risk_percentage["employee_count"].sum()
    * 100
)

st.dataframe(
    risk_percentage[
        ["ml_risk_level", "employee_count", "percentage"]
    ],
    use_container_width=True
)

# =========================================================
# DEPARTMENT-WISE ML RISK
# =========================================================

st.subheader("Department-wise ML Risk")

department_query = """
SELECT
    department_name,
    ml_risk_level,
    COUNT(*) AS employee_count
FROM ml_attrition_analytics
GROUP BY department_name, ml_risk_level
ORDER BY department_name;
"""

department_data = pd.read_sql(department_query, connection)

department_chart = department_data.pivot(
    index="department_name",
    columns="ml_risk_level",
    values="employee_count"
).fillna(0)

st.bar_chart(department_chart)

# =========================================================
# DEPARTMENT ATTRITION RATE
# =========================================================

st.subheader("Department-wise Attrition Rate")

department_attrition_query = """
SELECT
    department_name,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN actual_attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(
        SUM(CASE WHEN actual_attrition = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS attrition_rate
FROM ml_attrition_analytics
GROUP BY department_name
ORDER BY attrition_rate DESC;
"""

department_attrition_data = pd.read_sql(
    department_attrition_query,
    connection
)

st.dataframe(
    department_attrition_data,
    use_container_width=True
)
# =========================================================
# ACTUAL VS ML PREDICTION
# =========================================================

st.subheader("Actual Attrition vs ML Prediction")

prediction_query = """
SELECT
    actual_attrition,
    ml_prediction,
    COUNT(*) AS employee_count
FROM ml_attrition_analytics
GROUP BY actual_attrition, ml_prediction
ORDER BY actual_attrition, ml_prediction;
"""

prediction_data = pd.read_sql(prediction_query, connection)

prediction_chart = prediction_data.pivot(
    index="actual_attrition",
    columns="ml_prediction",
    values="employee_count"
).fillna(0)

st.bar_chart(prediction_chart)

# =========================================================
# HIGH-RISK EMPLOYEES
# =========================================================

st.subheader("Top High-Risk Employees")

high_risk_query = """
SELECT
    employee_id,
    age,
    department_name,
    job_role_name,
    monthly_income,
    job_satisfaction,
    work_life_balance,
    overtime,
    ml_prediction,
    ml_probability,
    ml_risk_level
FROM ml_attrition_analytics
WHERE ml_risk_level = 'HIGH'
ORDER BY ml_probability DESC
LIMIT 20;
"""

high_risk_data = pd.read_sql(high_risk_query, connection)

st.dataframe(
    high_risk_data,
    use_container_width=True
)

# =========================================================
# ML MODEL PERFORMANCE
# =========================================================

st.subheader("ML Model Performance")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Accuracy", "82.10%")
col2.metric("Precision", "75.78%")
col3.metric("Recall", "62.38%")
col4.metric("F1 Score", "68.43%")

st.write("Model: Logistic Regression")
st.write("Test Dataset: 1,000 employees")

# =========================================================
# CONFUSION MATRIX
# =========================================================

st.subheader("Confusion Matrix")

confusion_data = pd.DataFrame(
    {
        "Predicted NO": [627, 117],
        "Predicted YES": [62, 194]
    },
    index=["Actual NO", "Actual YES"]
)

st.dataframe(confusion_data, use_container_width=True)

# =========================================================
# EMPLOYEE ML PREDICTION SEARCH
# =========================================================

st.subheader("Employee Attrition Prediction")

employee_id = st.number_input(
    "Enter Employee ID",
    min_value=100001,
    step=1
)

if st.button("Check Prediction"):

    employee_query = """
    SELECT
        employee_id,
        department_name,
        job_role_name,
        ml_prediction,
        ml_probability,
        ml_risk_level
    FROM ml_attrition_analytics
    WHERE employee_id = %s;
    """

    employee_data = pd.read_sql(
        employee_query,
        connection,
        params=(employee_id,)
    )

    if employee_data.empty:
        st.error("Employee ID not found.")
    else:
        employee = employee_data.iloc[0]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Prediction",
            employee["ml_prediction"]
        )

        col2.metric(
            "Probability",
            f'{employee["ml_probability"]:.2f}%'
        )

        col3.metric(
            "Risk Level",
            employee["ml_risk_level"]
        )

        st.write("**Department:**", employee["department_name"])
        st.write("**Job Role:**", employee["job_role_name"])

        # =========================================================
# ACTUAL ATTRITION SUMMARY
# =========================================================

st.subheader("Actual Employee Attrition")

attrition_query = """
SELECT
    actual_attrition,
    COUNT(*) AS employee_count
FROM ml_attrition_analytics
GROUP BY actual_attrition;
"""

attrition_data = pd.read_sql(
    attrition_query,
    connection
)

st.bar_chart(
    attrition_data.set_index("actual_attrition")["employee_count"]
)

# =========================================================
# DOWNLOAD ML PREDICTIONS
# =========================================================

st.subheader("Download ML Prediction Report")

download_query = """
SELECT
    employee_id,
    age,
    department_name,
    job_role_name,
    monthly_income,
    job_satisfaction,
    work_life_balance,
    overtime,
    actual_attrition,
    ml_prediction,
    ml_probability,
    ml_risk_level,
    prediction_date
FROM ml_attrition_analytics
ORDER BY ml_probability DESC;
"""

download_data = pd.read_sql(
    download_query,
    connection
)

csv_data = download_data.to_csv(index=False)

st.download_button(
    label="Download Prediction Report",
    data=csv_data,
    file_name="employee_attrition_ml_predictions.csv",
    mime="text/csv"
)
# =========================================================
# DATABASE CONNECTION CLOSE
# =========================================================

connection.close()