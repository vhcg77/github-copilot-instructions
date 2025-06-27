---
applyTo: ["mlops", "deployment", "monitoring", "vertex-ai"]
role: "mlops-engineer"
description: "Prompt examples for MLOps Engineer role with Vertex AI and deployment"
tags: ["gcp", "vertex-ai", "cloud-build", "docker", "ci-cd", "monitoring", "automation"]
priority: "high"
---

# **MLOps Engineer: Prompt Examples (GCP & Vertex AI)**

## **1. CI/CD for Model Training (Cloud Build)**

### **Prompt**

"Create a `cloudbuild.yaml` configuration file for a CI/CD pipeline that automates the training and deployment of a machine learning model. The pipeline should have the following steps:
1.  **Install Dependencies**: Run `pip install -r requirements.txt`.
2.  **Run Unit Tests**: Execute `pytest` to ensure code quality.
3.  **Train Model**: Run the training script `python src/train.py` which saves a `model.joblib` file.
4.  **Deploy to Vertex AI**: Upload the model to the Vertex AI Model Registry using a custom script or gcloud commands."

---

## **2. Vertex AI Pipeline (KFP)**

### **Prompt**

"Generate a Python script using the Kubeflow Pipelines (KFP) SDK v2 to define a simple, three-step Vertex AI Pipeline:
1.  **Data Ingestion**: A component that downloads data from a GCS URL.
2.  **Data Validation**: A component that validates the schema of the ingested data.
3.  **Model Training**: A component that trains a simple scikit-learn model on the validated data.

Define each step as a lightweight Python function-based component. The pipeline should orchestrate these components in sequence."

---

## **3. Model Monitoring Setup**

### **Prompt**

"I have a deployed model on a Vertex AI Endpoint. I need to set up model monitoring to detect training-serving skew and prediction drift. Generate the Python code using the Vertex AI SDK to create a model monitoring job with the following configuration:
*   **Sampling Rate**: 30% of incoming requests.
*   **Monitoring Frequency**: Every 24 hours.
*   **Skew Detection Thresholds**: Specify thresholds for 3 key features (e.g., `age`, `income`, `country`).
*   **Drift Detection Thresholds**: Specify thresholds for the same 3 features.
*   **Notification Channel**: Set up email notifications to `mlops-alerts@example.com`."

---

## **4. Automating Model Retraining (Cloud Functions & Pub/Sub)**

### **Prompt**

"Design a serverless architecture to automatically trigger a model retraining pipeline in Vertex AI whenever new training data is uploaded to a GCS bucket. The architecture should use:
1.  **GCS**: A bucket (`my-training-data`) where new data arrives.
2.  **Cloud Functions**: A function triggered by the GCS `google.storage.object.finalize` event.
3.  **Pub/Sub**: A topic that the Cloud Function publishes a message to.
4.  **Vertex AI Pipelines**: A pipeline that is triggered by messages on the Pub/Sub topic.

Generate the Python code for the Cloud Function that publishes the GCS file path to the Pub/Sub topic."

---

## **5. Containerizing a Prediction Service (Docker)**

### **Prompt**

"Create a `Dockerfile` to containerize a Flask application that serves predictions from a machine learning model. The Dockerfile should:
1.  Use a Python 3.9 slim base image.
2.  Set a working directory `/app`.
3.  Copy the `requirements.txt` file and install the dependencies.
4.  Copy the application source code (including the model file) into the container.
5.  Expose port 8080.
6.  Define the command to run the Flask application using `gunicorn`."
