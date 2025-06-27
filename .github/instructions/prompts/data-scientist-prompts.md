---
applyTo: ["data-science", "eda", "modeling", "analysis"]
role: "data-scientist"
description: "Prompt examples for Data Scientist role with Python and Vertex AI"
tags: ["python", "pandas", "scikit-learn", "eda", "feature-engineering", "modeling", "vertex-ai"]
priority: "high"
---

# **Data Scientist: Prompt Examples (Python & Vertex AI)**

## **1. Exploratory Data Analysis (EDA)**

### **Prompt**

"I have a pandas DataFrame named `df` loaded from a CSV with columns `user_id`, `purchase_date`, `product_category`, `spend`, and `region`. Generate Python code to perform an initial exploratory data analysis. The code should:
1.  Display the first 5 rows (`.head()`).
2.  Show summary statistics (`.describe()`).
3.  Check for missing values in each column (`.isnull().sum()`).
4.  Plot a histogram of the `spend` column using Seaborn.
5.  Plot a bar chart showing the count of purchases per `product_category` using Matplotlib."

---

## **2. Feature Engineering**

### **Prompt**

"Given a pandas DataFrame `df` with a `purchase_date` column (as a datetime object), generate code to create the following new features:
1.  `day_of_week`: The day of the week of the purchase (e.g., Monday).
2.  `is_weekend`: A binary flag that is 1 if the purchase was made on a weekend and 0 otherwise.
3.  `purchase_month`: The month of the purchase (e.g., January).

Additionally, for a categorical column `product_category`, create one-hot encoded features using `pandas.get_dummies`."

---

## **3. Model Training (Scikit-learn)**

### **Prompt**

"Write Python code to train a Random Forest Classifier model using scikit-learn. Assume I have feature matrix `X_train` and a target vector `y_train`.

The code should:
1.  Instantiate a `RandomForestClassifier` with `n_estimators=100` and `random_state=42`.
2.  Train the model using the `.fit()` method on the training data.
3.  After training, print the feature importances, sorted in descending order, along with the corresponding feature names (assuming `X_train` is a pandas DataFrame)."

---

## **4. Model Evaluation**

### **Prompt**

"I have a trained classification model (`model`) and test data (`X_test`, `y_test`). Generate Python code to evaluate the model's performance. The code must:
1.  Generate predictions on `X_test`.
2.  Calculate and print the accuracy score.
3.  Generate and print the classification report from `sklearn.metrics`.
4.  Generate and plot a confusion matrix using `seaborn.heatmap`."

---

## **5. Deploying to Vertex AI**

### **Prompt**

"I have a trained and saved scikit-learn model file (`model.joblib`). I need to deploy this model to a Vertex AI Endpoint. Generate the Python code using the Vertex AI SDK to:
1.  Upload the model to the Vertex AI Model Registry. Specify the correct pre-built container for scikit-learn predictions (e.g., `us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-0:latest`).
2.  Create a new Vertex AI Endpoint.
3.  Deploy the uploaded model to the created endpoint."
