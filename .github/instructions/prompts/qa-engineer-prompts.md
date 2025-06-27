---
applyTo: ["testing", "quality-assurance", "validation"]
role: "qa-engineer"
description: "Prompt examples for QA Engineer role"
tags: ["pytest", "testing", "test-case-generation", "bug-report", "test-plan", "automation", "selenium"]
priority: "high"
---

# **QA Engineer: Prompt Examples (Pytest & GCP)**

## **1. Test Case Generation from Requirements**

### **Prompt**

"Given the following requirement for a BigQuery data transformation function `process_user_data(source_table, destination_table)`:
*   The function must read data from `source_table`.
*   It must filter out users with a `status` of 'inactive'.
*   It must calculate the user's age from their `date_of_birth`.
*   It must write the transformed data (including the new `age` column) to `destination_table`.

Generate a set of test cases in a human-readable format (e.g., Gherkin or a simple list) to validate this function. Include positive, negative, and edge cases (e.g., empty source table, null `date_of_birth`)."

---

## **2. Pytest Test Generation**

### **Prompt**

"Write a Python unit test using `pytest` for a function `calculate_average(numbers: list) -> float`. The test file should be named `test_calculations.py`. The test should cover the following scenarios:
1.  A list of positive integers.
2.  A list containing negative numbers and zero.
3.  An empty list (should raise a `ValueError`).
4.  A list with a single number.

Use `pytest.raises` to check for the exception. Use `pytest.mark.parametrize` to test the first two scenarios efficiently."

---

## **3. Bug Report Generation**

### **Prompt**

"I have identified a bug in the data visualization dashboard. When I filter the date range to the last 24 hours, the total revenue metric shows a negative value, which is incorrect. The expected result is a positive number or zero. This occurs in the production environment on the main sales dashboard.

Generate a formal bug report based on this information. The report should include:
*   A concise title.
*   Steps to reproduce.
*   Expected result.
*   Actual result.
*   Environment details.
*   Severity/Priority (suggest a level)."

---

## **4. Test Automation Script (Selenium)**

### **Prompt**

"Generate a Python script using Selenium to automate a login test for a web application. The script should:
1.  Navigate to the login page (`https://myapp.example.com/login`).
2.  Find the username and password input fields by their `id` (`username-field`, `password-field`).
3.  Find the login button by its `id` (`login-button`).
4.  Enter a test username and password.
5.  Click the login button.
6.  Assert that the URL changes to the dashboard page (`/dashboard`) after a successful login."

---

## **5. Test Plan Outline**

### **Prompt**

"Create a high-level test plan outline for a new feature that allows users to upload a CSV file, which is then processed by a Dataflow job and loaded into BigQuery. The plan should cover:
*   **Scope**: What will be tested.
*   **Objectives**: Goals of the testing.
*   **Test Strategy**: (e.g., Unit, Integration, E2E, Performance).
*   **Test Environment**: (e.g., GCP project, service accounts, sample data).
*   **Key Scenarios to Test**: (e.g., valid file upload, invalid file format, large file, Dataflow job failure).
*   **Exit Criteria**: Conditions for completing the testing phase."
