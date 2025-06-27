---
applyTo: ["testing", "unit-tests", "validation"]
task: "test-generation"
description: "Prompt examples for test generation tasks"
tags: ["pytest", "unittesting", "integration-testing", "mocking", "fixtures"]
priority: "high"
---

# **Task: Test Generation Prompts (Pytest)**

## **1. Unit Test for a Pure Function**

### **Prompt**

"Generate a unit test for the following Python function located in `src/utils/calculations.py` using the `pytest` framework. The function is:

```python
def add(a: int, b: int) -> int:
    return a + b
```

The test should be in a new file `tests/utils/test_calculations.py` and include cases for positive numbers, negative numbers, and zero."

---

## **2. Test with Mocks (Mocking an API Call)**

### **Prompt**

"I have a function in `src/data/api_client.py` that fetches user data from an external API:

```python
import requests

def get_user_data(user_id: int) -> dict:
    response = requests.get(f"https://api.example.com/users/{user_id}")
    response.raise_for_status()
    return response.json()
```

Generate a unit test for this function in `tests/data/test_api_client.py`. Use `pytest` and the `unittest.mock.patch` decorator to mock the `requests.get` call. The test should verify that the function correctly handles a successful API response (status 200) and returns the expected JSON data."

---

## **3. Test with Fixtures (Pandas DataFrame)**

### **Prompt**

"I need to test a function that processes a pandas DataFrame. Create a `pytest` fixture in `tests/conftest.py` named `sample_dataframe`. This fixture should return a simple pandas DataFrame with columns `id`, `name`, and `value`. Then, show how to write a test in `tests/processing/test_data_cleaning.py` that uses this fixture as an input to test a function `clean_data(df)`."

---

## **4. Parameterized Test**

### **Prompt**

"Generate a `pytest` test for a function `is_even(n: int) -> bool`. The test should use the `@pytest.mark.parametrize` decorator to efficiently test multiple input values. Include test cases for even numbers, odd numbers, and zero."

---

## **5. Testing for Exceptions**

### **Prompt**

"Write a `pytest` test for a function `divide(a, b)` that is expected to raise a `ZeroDivisionError` when the divisor `b` is zero. Use the `pytest.raises` context manager to assert that the correct exception is raised."
