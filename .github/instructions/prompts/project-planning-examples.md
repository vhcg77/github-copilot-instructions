---
applyTo: ["project-planning", "examples", "management", "coordination"]
description: "Project planning prompt examples and templates"
tags: ["planning", "resource-allocation", "timeline", "stakeholder-management", "agile"]
priority: "medium"
---

# Project Planning Prompt Examples

## Prompt: Create Project Plan for ML Platform

**User Input:**
"I need to create a project plan for building a machine learning platform that will serve real-time predictions for our e-commerce recommendation system. We have a team of 6 people and a budget of $200k. The platform needs to be ready in 4 months."

**Expected Response Format:**

### Project Charter
**Project Name:** E-commerce ML Recommendation Platform

**Problem Statement:** 
Current recommendation system is rule-based and doesn't adapt to user behavior, resulting in low conversion rates (2.1% vs industry standard 3.5%).

**Success Metrics:**
- Increase conversion rate to 3.2% within 6 months of deployment
- Reduce recommendation response time to <100ms
- Achieve 99.9% platform uptime
- Process 10M+ recommendations daily

**Scope & Deliverables:**
- Real-time ML inference API
- Model training and deployment pipeline
- A/B testing framework
- Monitoring and alerting system
- Data pipeline for feature engineering

**Timeline Overview:**
- **Phase 1 (Weeks 1-4):** Discovery & Architecture
- **Phase 2 (Weeks 5-12):** Development & Testing
- **Phase 3 (Weeks 13-16):** Deployment & Optimization

### Resource Allocation
| Role | Team Members | Allocation | Key Responsibilities |
|------|-------------|------------|---------------------|
| Data Scientist | 2 | 100% | Model development, feature engineering |
| MLOps Engineer | 1 | 100% | Pipeline development, deployment |
| Data Engineer | 1 | 80% | Data infrastructure, ETL |
| Cloud Architect | 1 | 60% | Platform design, security |
| Frontend Developer | 1 | 40% | Admin dashboard, monitoring UI |

### Risk Assessment
| Risk | Probability | Impact | Mitigation Strategy |
|------|------------|--------|-------------------|
| Data quality issues | High | High | Implement data validation framework early |
| Model performance below target | Medium | High | Prototype multiple algorithms, set interim checkpoints |
| Infrastructure scaling | Medium | Medium | Load testing, auto-scaling configuration |
| Team availability | Low | High | Cross-training, documentation |

### Communication Plan
- **Daily:** 15-min standup (development team)
- **Weekly:** Progress review with stakeholders
- **Bi-weekly:** Sprint demos and retrospectives
- **Monthly:** Executive steering committee update

---

## Prompt: Resource Planning for Data Migration

**User Input:**
"We need to migrate our legacy data warehouse to Google Cloud. The current system has 15TB of data across 200+ tables. What resources and timeline do we need?"

**Expected Response Format:**

### Migration Project Plan

**Scope Assessment:**
- **Data Volume:** 15TB across 200+ tables
- **Complexity:** Legacy schema requires normalization
- **Dependencies:** 12 downstream systems, 5 BI tools
- **Compliance:** GDPR, SOX requirements

**Resource Requirements:**
- **Data Engineers:** 3 FTE (6 months)
- **Cloud Architect:** 1 FTE (3 months)
- **DBA/Legacy Expert:** 0.5 FTE (6 months)
- **QA Engineer:** 1 FTE (4 months)
- **Project Manager:** 0.5 FTE (6 months)

**Technology Stack:**
- Google Cloud BigQuery (target warehouse)
- Cloud Storage (staging area)
- Dataflow (ETL processing)
- Data Catalog (metadata management)
- Cloud Monitoring (observability)

**Timeline Breakdown:**
```
Phase 1: Assessment & Planning (4 weeks)
├── Schema analysis and mapping
├── Data quality assessment
├── Architecture design
└── Migration strategy finalization

Phase 2: Infrastructure Setup (3 weeks)
├── GCP environment provisioning
├── Security configuration
├── Network connectivity
└── Monitoring setup

Phase 3: Data Migration (16 weeks)
├── Week 1-4: Core transactional tables
├── Week 5-8: Historical data migration
├── Week 9-12: Reference and lookup tables
├── Week 13-16: Validation and optimization

Phase 4: Testing & Cutover (4 weeks)
├── End-to-end testing
├── Performance validation
├── User acceptance testing
└── Go-live preparation
```

**Budget Estimation:**
- **Personnel:** $450,000 (6 months)
- **GCP Infrastructure:** $25,000 (6 months)
- **Migration Tools:** $15,000
- **Contingency (15%):** $73,500
- **Total:** $563,500
