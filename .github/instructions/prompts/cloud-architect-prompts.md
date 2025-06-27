---
applyTo: ["architecture", "gcp", "infrastructure", "security"]
role: "cloud-architect"
description: "Prompt examples for Cloud Architect role with GCP and Terraform"
tags: ["gcp", "architecture-design", "security", "cost-optimization", "iac", "terraform", "networking"]
priority: "high"
---

# **Cloud Architect: Prompt Examples (GCP & Terraform)**

## **1. Architecture Design**

### **Prompt**

"Design a scalable and resilient architecture on Google Cloud Platform for a web application that serves real-time user dashboards. The architecture should include:
1.  A global load balancer.
2.  A managed instance group of Compute Engine VMs for the backend API.
3.  A Cloud SQL for PostgreSQL database for transactional data.
4.  Cloud Storage for static assets.
5.  A Redis instance on Memorystore for caching.

Generate a high-level description of the data flow and the role of each component. Also, create a simple diagram using Mermaid syntax."

---

## **2. Infrastructure as Code (Terraform)**

### **Prompt**

"Write a Terraform configuration (`main.tf`) to provision a new Google Cloud Storage bucket with the following specifications:
*   A unique name prefixed with `my-app-data-`.
*   Location set to `us-central1`.
*   Standard storage class.
*   Uniform bucket-level access enabled.
*   Versioning enabled to retain the 3 most recent versions of each object.
*   A lifecycle rule to delete objects older than 365 days."

---

## **3. Security & IAM**

### **Prompt**

"Define a custom IAM role for a 'Data Analyst' in GCP using a Terraform resource (`google_project_iam_custom_role`). The role should only grant the following permissions:
*   `bigquery.jobs.create`
*   `bigquery.tables.getData`
*   `bigquery.tables.list`
*   `storage.objects.get`
*   `storage.objects.list`

Also, create a `google_project_iam_member` resource to assign this custom role to a specific service account (`data-analyst-sa@my-project.iam.gserviceaccount.com`)."

---

## **4. Cost Optimization**

### **Prompt**

"Our monthly GCP bill for a project has increased significantly. The primary cost drivers appear to be Compute Engine and BigQuery. Provide a checklist of potential areas to investigate for cost optimization. For each area, suggest a specific action or tool to use. For example:
*   **Compute Engine**: Check for idle VMs, analyze rightsizing recommendations.
*   **BigQuery**: Analyze expensive queries, review storage costs for old partitions."

---

## **5. Networking (VPC & Firewall)**

### **Prompt**

"Generate a Terraform configuration to create a custom VPC network named `my-custom-vpc`. Within this VPC, create a subnet named `my-subnet` in the `us-east1` region with an IP range of `10.10.1.0/24`. Additionally, create a firewall rule that allows SSH traffic (TCP port 22) from a specific IP range (`203.0.113.0/24`) to all instances in the VPC."
