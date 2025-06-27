---
applyTo: ["code-review", "quality-assurance", "feedback"]
task: "code-review"
description: "Prompt examples for code review tasks"
tags: ["review", "feedback", "pull-request", "best-practices", "readability", "performance"]
priority: "medium"
---

# **Task: Code Review Prompts**

## **1. General Code Review**

### **Prompt**

"Act as a senior developer and perform a code review on the following Python script. Check for adherence to PEP 8, clarity, potential bugs, and performance issues. Provide constructive feedback with specific examples and suggestions for improvement. The script is located at `src/processing/new_feature.py`."

---

## **2. Security-Focused Review**

### **Prompt**

"Please perform a security-focused code review on the following Flask API endpoint located in `src/api/endpoints.py`. Look for common web vulnerabilities such as SQL injection, Cross-Site Scripting (XSS), insecure direct object references, and improper error handling. The code handles user input to query a database."

---

## **3. Review Against a Specific Standard**

### **Prompt**

"Review the following function against our project's coding standards, which require Google-style docstrings and full type hinting. Identify any areas that do not comply and provide the corrected code. The function is `def my_function(arg1, arg2): ...` in `src/utils/helpers.py`."

---

## **4. Performance Review**

### **Prompt**

"I have a Python script that processes a large CSV file using pandas. It seems to be very slow. Please review the code in `src/etl/data_transform.py` and identify any performance bottlenecks. Suggest more efficient, vectorized alternatives to any loops or inefficient operations you find."

---

## **5. Pull Request Review Summary**

### **Prompt**

"I am about to approve a pull request. Please review the changes (diff provided below) and generate a concise, encouraging summary comment for the pull request. The comment should acknowledge the contributor's work, highlight one or two key improvements, and confirm that the changes meet the requirements.

[Paste PR diff here]"
