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
# 3. GET EMPLOYEE ID
# =========================================================

employee_id = int(input("\nEnter Employee ID: "))


# =========================================================
# 4. FETCH EMPLOYEE DATA
# =========================================================

query = """
SELECT *
FROM employee_analytics
WHERE employee_id = %s
"""

cursor = connection.cursor()
cursor.execute(query, (employee_id,))

data = cursor.fetchone()
columns = cursor.column_names

cursor.close()
connection.close()


# =========================================================
# 5. CHECK EMPLOYEE EXISTS
# =========================================================

if data is None:
    print("\nEmployee not found.")
    exit()


df = pd.DataFrame([data], columns=columns)

print("\nEmployee found successfully!")


# =========================================================
# 6. PREPARE DATA FOR ML MODEL
# =========================================================

X = df.drop(columns=["employee_id", "attrition_status"])


# =========================================================
# 7. PREDICT ATTRITION
# =========================================================

prediction = model.predict(X)[0]

probability = model.predict_proba(X)[0][1]


# =========================================================
# 8. DETERMINE RISK LEVEL
# =========================================================

if probability >= 0.70:
    risk_level = "HIGH"
elif probability >= 0.40:
    risk_level = "MEDIUM"
else:
    risk_level = "LOW"


# =========================================================
# 9. DISPLAY RESULT
# =========================================================

print("\n====================================")
print("       ATTRITION PREDICTION")
print("====================================")

print("Employee ID :", employee_id)

if prediction == 1:
    print("Prediction  : YES")
else:
    print("Prediction  : NO")

print(f"Probability : {probability:.2%}")
print("Risk Level  :", risk_level)

print("====================================")