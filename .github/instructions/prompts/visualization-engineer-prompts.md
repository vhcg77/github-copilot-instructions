---
applyTo: ["visualization", "dashboards", "analytics"]
role: "visualization-engineer"
description: "Prompt examples for Visualization Engineer role"
tags: ["looker-studio", "plotly", "dash", "streamlit", "bigquery-integration", "dashboard-design"]
priority: "high"
---

# **Visualization Engineer: Prompt Examples (Looker Studio, Plotly & GCP)**

## **1. Dashboard Design Principles**

### **Prompt**

"I need to design a new sales performance dashboard in Looker Studio for executive stakeholders. The key metrics to display are Total Revenue, Revenue by Region, Top 10 Products, and Sales Growth Over Time. What are the key design principles I should follow to make this dashboard effective, clear, and actionable for a non-technical audience? Provide a checklist of best practices."

---

## **2. Creating a Looker Studio Data Source**

### **Prompt**

"Describe the step-by-step process to create a new data source in Looker Studio that connects directly to a BigQuery table named `my-project.mydataset.quarterly_sales`. Explain how to configure the data source, including setting data types for key metrics (e.g., `revenue` as currency) and dimensions (e.g., `sale_date` as date)."

---

## **3. Interactive Plotly Chart (Python)**

### **Prompt**

"Generate Python code using Plotly Express to create an interactive scatter plot. Assume I have a pandas DataFrame `df` with columns `average_income`, `life_expectancy`, `country`, and `continent`. The scatter plot should:
*   Map `average_income` to the x-axis and `life_expectancy` to the y-axis.
*   Color the points by `continent`.
*   Size the points by `population` (another column in the DataFrame).
*   Display the `country` name when a user hovers over a point.
*   Have a clear title and axis labels."

---

## **4. Building a Simple Dashboard with Dash**

### **Prompt**

"Generate the Python code for a simple web dashboard using Plotly Dash. The dashboard should have a single dropdown menu that allows a user to select a stock ticker (e.g., 'AAPL', 'GOOGL', 'MSFT'). When a ticker is selected, the dashboard should display a line chart showing the stock's closing price over the last year. Use the `yfinance` library to fetch the stock data. The layout should be clean and simple."

---

## **5. BigQuery SQL for Visualization**

### **Prompt**

"Write a BigQuery SQL query optimized for a time-series visualization in Looker Studio. The query should aggregate daily user sign-ups from a table `my-project.events.user_signups` which has a `signup_timestamp` (TIMESTAMP) column. The query needs to return two columns: `signup_date` (formatted as a DATE) and `total_signups` (the count of users for that day). The results should be sorted by date in ascending order for the last 90 days."
