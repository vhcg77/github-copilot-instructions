---
applyTo: ["etl", "data-engineering", "bigquery", "pipelines"]
role: "data-engineer"
description: "Prompt examples for Data Engineer role with GCP services"
tags: ["gcp", "bigquery", "dataflow", "composer", "sql", "python", "data-modeling", "etl"]
priority: "high"
---

# **Data Engineer: Prompt Examples (GCP & Python)**

## **1. BigQuery SQL Query**

### **Prompt**

"Write a BigQuery SQL query to find the top 5 customers by total spending from a table named `my-project.mydataset.sales`. The table has the columns `customer_id`, `product_id`, `quantity`, and `price`. The query should join with a `my-project.mydataset.customers` table on `customer_id` to get the `customer_name`. The final output should be `customer_name` and `total_spent`."

---

## **2. Dataflow Pipeline (Python)**

### **Prompt**

"Generate a Python script for a simple Apache Beam batch pipeline that reads text files from a Google Cloud Storage (GCS) bucket, counts the occurrences of each word, and writes the results to another GCS bucket as a text file. The script should use the Beam SDK and be runnable on Dataflow. Include comments explaining the PCollection and transformations (Read, Map, Count, Write)."

---

## **3. Data Modeling (DDL)**

### **Prompt**

"Generate the BigQuery DDL (`CREATE TABLE` statement) for a dimension table named `dim_products`. The table should include the following columns:
*   `product_key` (INTEGER, primary key, auto-incrementing)
*   `product_id` (STRING, the source system ID)
*   `product_name` (STRING)
*   `category` (STRING)
*   `brand` (STRING)
*   `unit_price` (NUMERIC)
*   `effective_start_date` (DATE)
*   `effective_end_date` (DATE)

Partition the table by `effective_end_date` on a monthly basis and cluster it by `category`."

---

## **4. Cloud Composer (Airflow) DAG**

### **Prompt**

"Create a basic Airflow DAG for Cloud Composer to perform a daily data loading task. The DAG should:
1.  Be scheduled to run daily (`@daily`).
2.  Have a start date of yesterday.
3.  Define two tasks:
    *   A `BashOperator` task named `start_task` that prints the execution date.
    *   A `BigQueryExecuteQueryOperator` task named `load_data_to_bigquery` that runs a simple `INSERT` statement from a staging table to a final table.

The second task should depend on the first one."

---

## **5. Python Script for GCS**

### **Prompt**

"Write a Python function that uses the `google-cloud-storage` client library to list all blobs in a specific GCS bucket that have a `.csv` extension. The function should take the `bucket_name` as an argument and return a list of the blob names."
