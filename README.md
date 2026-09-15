# Employee Attrition Analytics Database

## Project Overview

Employee Attrition Analytics is a DBMS project designed to analyze employee attrition and identify factors associated with employee turnover.

The project uses a normalized relational database to store employee information, compensation, satisfaction, performance, and attrition data.

## Objectives

- Analyze employee attrition rates.
- Identify departments and job roles with higher attrition.
- Analyze the relationship between overtime and attrition.
- Study employee satisfaction and work-life balance.
- Analyze compensation and employee turnover.
- Identify employees with potential attrition risk.
- Provide HR-focused analytical views for decision-making.

## Technologies Used

- MySQL
- MySQL Workbench
- SQL
- GitHub

## Database Structure

The database contains the following main tables:

- Employees
- Departments
- Job_Roles
- Compensation
- Satisfaction
- Performance
- Attrition

A raw staging table is also used for initial data loading.

## Key Features

### Attrition Analysis
Calculates total employees, employees who left, active employees, and overall attrition rate.

### Department Analysis
Analyzes employee attrition across different departments.

### Job Role Analysis
Compares attrition rates across different job roles.

### Satisfaction Analysis
Studies job satisfaction, environment satisfaction, relationship satisfaction, and work-life balance.

### Compensation Analysis
Analyzes salary, salary hikes, and stock options in relation to attrition.

### Attrition Risk Analysis
Uses a rule-based risk score based on factors such as overtime, job satisfaction, work-life balance, years at company, and distance from home.

## Database Views

- `employee_analytics`
- `hr_dashboard_summary`
- `department_dashboard`
- `job_role_dashboard`
- `employee_attrition_risk`
- `risk_dashboard`

## Dataset

The project uses a dataset containing 5,000 employee records and 36 attributes.

## Project Outcome

The database provides HR analytics that can help identify patterns related to employee attrition and highlight employees who may require attention.

## ER Diagram

The project includes an Entity Relationship Diagram showing the relationships between the normalized database tables.

## Author

Tanvi Raut
