import mysql.connector
import pandas as pd
import joblib


# =========================================================
# 1. LOAD TRAINED ML MODEL
# =========================================================

model = joblib.load("ml_model/model.pkl")

print("ML model loaded successfully!")


# =========================================================
# 2. CONNECT TO MYSQL DATABASE
# =========================================================

connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="Tanviraut@123",
    database="employee_attrition_db"
)

print("MySQL connection successful!")


# =========================================================
# 3. LOAD ALL EMPLOYEE DATA
# =========================================================

query = """
SELECT *
FROM employee_analytics
"""

cursor = connection.cursor()
cursor.execute(query)

data = cursor.fetchall()
columns = cursor.column_names

df = pd.DataFrame(data, columns=columns)

print("Employee data loaded successfully!")
print("Total employees:", len(df))


# =========================================================
# 4. SAVE EMPLOYEE IDs
# =========================================================

employee_ids = df["employee_id"]


# =========================================================
# 5. PREPARE DATA FOR ML MODEL
# =========================================================

X = df.drop(columns=["employee_id", "attrition_status"])


# =========================================================
# 6. MAKE ML PREDICTIONS
# =========================================================

predictions = model.predict(X)

probabilities = model.predict_proba(X)[:, 1]


# =========================================================
# 7. CREATE RESULT TABLE
# =========================================================

results = pd.DataFrame({
    "employee_id": employee_ids,
    "prediction": predictions,
    "probability": probabilities
})


# =========================================================
# 8. CONVERT PREDICTION TO YES / NO
# =========================================================

results["prediction"] = results["prediction"].map({
    0: "NO",
    1: "YES"
})


# =========================================================
# 9. CREATE RISK LEVEL
# =========================================================

def get_risk_level(probability):

    if probability >= 0.70:
        return "HIGH"

    elif probability >= 0.40:
        return "MEDIUM"

    else:
        return "LOW"


results["risk_level"] = results["probability"].apply(
    get_risk_level
)


# =========================================================
# 10. CONVERT PROBABILITY TO PERCENTAGE
# =========================================================

results["probability"] = (
    results["probability"] * 100
).round(2)


# =========================================================
# 11. DISPLAY FIRST 10 RESULTS
# =========================================================

print("\n====================================")
print("       ML ATTRITION RESULTS")
print("====================================")

print(results.head(10).to_string(index=False))


# =========================================================
# 12. INSERT ML RESULTS INTO MYSQL
# =========================================================

print("\nSaving ML predictions to MySQL...")

insert_query = """
INSERT INTO ml_attrition_predictions
(
    employee_id,
    prediction,
    probability,
    risk_level
)
VALUES (%s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    prediction = VALUES(prediction),
    probability = VALUES(probability),
    risk_level = VALUES(risk_level),
    prediction_date = CURRENT_TIMESTAMP
"""


for _, row in results.iterrows():

    cursor.execute(
        insert_query,
        (
            int(row["employee_id"]),
            row["prediction"],
            float(row["probability"]),
            row["risk_level"]
        )
    )


connection.commit()

print("ML predictions successfully saved to MySQL!")


# =========================================================
# 13. CLOSE MYSQL CONNECTION
# =========================================================

cursor.close()
connection.close()


# =========================================================
# 14. SAVE RESULTS TO CSV
# =========================================================

results.to_csv(
    "ml_model/attrition_predictions.csv",
    index=False
)

print("\nPrediction results saved to:")
print("ml_model/attrition_predictions.csv")


# =========================================================
# 15. RISK SUMMARY
# =========================================================

print("\n====================================")
print("       RISK SUMMARY")
print("====================================")

print(results["risk_level"].value_counts())


# =========================================================
# 16. COMPLETE
# =========================================================

print("\n====================================")
print(" ML DATABASE INTEGRATION COMPLETE")
print("====================================")