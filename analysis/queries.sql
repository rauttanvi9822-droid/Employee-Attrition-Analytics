-- Employee Attrition Analytics
-- SQL Analysis Queries

-- 1. Overall Attrition
SELECT
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition_status = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(
        SUM(CASE WHEN attrition_status = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS attrition_rate_percentage
FROM Attrition;


-- 2. Department-wise Attrition
SELECT
    department_name,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition_status = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(
        SUM(CASE WHEN attrition_status = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS attrition_rate_percentage
FROM employee_analytics
GROUP BY department_name
ORDER BY attrition_rate_percentage DESC;


-- 3. Job Role-wise Attrition
SELECT
    job_role_name,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition_status = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(
        SUM(CASE WHEN attrition_status = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS attrition_rate_percentage
FROM employee_analytics
GROUP BY job_role_name
ORDER BY attrition_rate_percentage DESC;


-- 4. Overtime vs Attrition
SELECT
    overtime,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition_status = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(
        SUM(CASE WHEN attrition_status = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS attrition_rate_percentage
FROM employee_analytics
GROUP BY overtime;


-- 5. Job Satisfaction vs Attrition
SELECT
    job_satisfaction,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition_status = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(
        SUM(CASE WHEN attrition_status = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS attrition_rate_percentage
FROM employee_analytics
GROUP BY job_satisfaction
ORDER BY job_satisfaction;


-- 6. Attrition Risk Analysis
SELECT
    employee_id,
    department_name,
    job_role_name,
    risk_score,
    risk_level
FROM employee_attrition_risk
ORDER BY risk_score DESC;


-- 7. Risk Level Summary
SELECT
    risk_level,
    COUNT(*) AS employee_count
FROM employee_attrition_risk
GROUP BY risk_level
ORDER BY employee_count DESC;