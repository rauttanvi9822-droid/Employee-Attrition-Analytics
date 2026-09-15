-- Employee Attrition Analytics Database
-- Project: HR Analytics and Attrition Risk Analysis

CREATE DATABASE IF NOT EXISTS employee_attrition_db;

-- Main tables

CREATE TABLE Departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Job_Roles (
    job_role_id INT AUTO_INCREMENT PRIMARY KEY,
    job_role_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Employees (
    employee_id INT PRIMARY KEY,
    age INT,
    gender VARCHAR(20),
    marital_status VARCHAR(30),
    education VARCHAR(50),
    education_field VARCHAR(100),
    business_travel VARCHAR(50),
    distance_from_home INT,
    department_id INT,
    job_role_id INT,
    job_level INT,
    total_working_years INT,
    years_at_company INT,
    years_in_current_role INT,
    years_since_last_promotion INT,
    years_with_curr_manager INT,
    num_companies_worked INT,
    FOREIGN KEY (department_id) REFERENCES Departments(department_id),
    FOREIGN KEY (job_role_id) REFERENCES Job_Roles(job_role_id)
);

CREATE TABLE Compensation (
    compensation_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    monthly_income DECIMAL(10,2),
    monthly_rate DECIMAL(10,2),
    daily_rate DECIMAL(10,2),
    hourly_rate DECIMAL(10,2),
    percent_salary_hike INT,
    stock_option_level INT,
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

CREATE TABLE Satisfaction (
    satisfaction_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    job_satisfaction INT,
    environment_satisfaction INT,
    relationship_satisfaction INT,
    work_life_balance INT,
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

CREATE TABLE Performance (
    performance_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    performance_rating INT,
    job_involvement INT,
    training_times_last_year INT,
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

CREATE TABLE Attrition (
    attrition_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    attrition_status VARCHAR(10),
    overtime VARCHAR(10),
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);