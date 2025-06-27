---
title: "Create GCP Architecture Design"
description: "Design scalable, secure, and cost-effective GCP architecture"
mode: "agent"
tools: ["terraform", "gcp", "mermaid", "architecture"]
role: "cloud-architect"
priority: "high"
---

# Create GCP Architecture Design

## Objective
Design a complete Google Cloud Platform architecture following the Google Cloud Architecture Framework principles.

## Context
You are a Cloud Architect designing solutions for a data science and analytics platform on GCP. Focus on scalability, security, cost-effectiveness, and operational excellence.

## Architecture Pillars to Address

### 1. System Design
- Define overall architecture and component interactions
- Justify technology choices (e.g., Cloud Run vs GKE)
- Create architecture diagrams using Mermaid syntax

### 2. Security & Compliance
- IAM roles and policies (principle of least privilege)
- VPC design and network security
- Data encryption at rest and in transit
- Secret management strategy

### 3. Reliability
- High availability and disaster recovery design
- Define SLOs and error budgets
- Monitoring and alerting strategy

### 4. Cost Optimization
- Service selection rationale
- Cost estimation and optimization strategies
- Resource right-sizing recommendations

### 5. Performance Optimization
- Service sizing and scaling strategies
- Data flow optimization
- Caching and CDN strategies

### 6. Operational Excellence
- CI/CD pipeline design
- Infrastructure as Code strategy
- Monitoring and logging architecture

## Expected Output Format

### Architecture Diagram (Mermaid)
```mermaid
graph TB
    subgraph "VPC - Production"
        subgraph "Private Subnet"
            GKE[GKE Cluster]
            CloudSQL[(Cloud SQL)]
        end
        subgraph "Public Subnet"
            LB[Load Balancer]
        end
    end
    
    Users --> LB
    LB --> GKE
    GKE --> CloudSQL
    GKE --> BigQuery[(BigQuery)]
```

### Technology Justification
- Detailed rationale for each service selection
- Alternative options considered
- Trade-offs and decision factors

### Cost Estimation
- High-level monthly cost breakdown
- Cost optimization opportunities
- Scaling cost implications

## Prompt
Ask the user for:
1. Business requirements and constraints
2. Expected scale (users, data volume, traffic)
3. Compliance requirements
4. Budget constraints
5. Existing infrastructure or migrations

Then provide a comprehensive architecture design following GCP best practices.
