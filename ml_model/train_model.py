import mysql.connector
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# =========================================================
# 1. CONNECT TO MYSQL DATABASE
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
# 2. GET EMPLOYEE DATA FROM MYSQL
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

cursor.close()
connection.close()

print("Employee data loaded successfully!")
print("Number of employees:", len(df))


# =========================================================
# 3. CREATE TARGET VARIABLE
# =========================================================

# Attrition is the value we want the ML model to predict.
# Yes = 1
# No  = 0

df["attrition_status"] = df["attrition_status"].map({
    "Yes": 1,
    "No": 0
})


# =========================================================
# 4. SEPARATE INPUT FEATURES AND TARGET
# =========================================================

# employee_id is only an identifier.
# We don't want the ML model to learn from it.

X = df.drop(columns=["employee_id", "attrition_status"])

y = df["attrition_status"]


# =========================================================
# 5. IDENTIFY NUMERICAL AND CATEGORICAL COLUMNS
# =========================================================

categorical_columns = [
    "gender",
    "marital_status",
    "education",
    "education_field",
    "department_name",
    "job_role_name",
    "overtime"
]

numerical_columns = [
    "age",
    "job_level",
    "total_working_years",
    "years_at_company",
    "years_in_current_role",
    "years_since_last_promotion",
    "years_with_curr_manager",
    "num_companies_worked",
    "monthly_income",
    "percent_salary_hike",
    "stock_option_level",
    "job_satisfaction",
    "environment_satisfaction",
    "relationship_satisfaction",
    "work_life_balance",
    "performance_rating",
    "job_involvement",
    "training_times_last_year"
]


# =========================================================
# 6. PREPROCESSING
# =========================================================

# Numerical data:
# Missing values are replaced with the median.
# Then the values are standardized.

numerical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])


# Categorical data:
# Missing values are replaced with the most common value.
# Then categories are converted into numbers.

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])


preprocessor = ColumnTransformer([
    ("numerical", numerical_pipeline, numerical_columns),
    ("categorical", categorical_pipeline, categorical_columns)
])


# =========================================================
# 7. CREATE ML MODEL
# =========================================================

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)


# Combine preprocessing + ML model

ml_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", model)
])


# =========================================================
# 8. SPLIT DATA INTO TRAINING AND TESTING DATA
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nTraining employees:", len(X_train))
print("Testing employees:", len(X_test))


# =========================================================
# 9. TRAIN THE MODEL
# =========================================================

print("\nTraining ML model...")

ml_pipeline.fit(X_train, y_train)

print("Model training completed!")


# =========================================================
# 10. MAKE PREDICTIONS
# =========================================================

y_pred = ml_pipeline.predict(X_test)


# =========================================================
# 11. MODEL EVALUATION
# =========================================================

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)


print("\n====================================")
print("       MODEL PERFORMANCE")
print("====================================")

print(f"Accuracy  : {accuracy:.2%}")
print(f"Precision : {precision:.2%}")
print(f"Recall    : {recall:.2%}")
print(f"F1 Score  : {f1:.2%}")


print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["No Attrition", "Attrition"],
    zero_division=0
))


print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# =========================================================
# 12. SAVE TRAINED MODEL
# =========================================================

joblib.dump(
    ml_pipeline,
    "ml_model/model.pkl"
)

print("\nTrained model saved as:")
print("ml_model/model.pkl")


# =========================================================
# 13. COMPLETE
# =========================================================

print("\n====================================")
print(" ML ATTRITION MODEL READY")
print("====================================")