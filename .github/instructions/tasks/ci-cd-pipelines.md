---
applyTo: ["ci-cd", "mlops", "vertex-ai", "cloud-build", "deployment", "automation"]
description: "Instructions for creating CI/CD pipelines for ML workflows on GCP"
priority: "high"
---

# **Task: CI/CD Pipeline Creation (MLOps)**

Create automated CI/CD pipelines for machine learning workflows using Google Cloud Platform services.

## **Pipeline Architecture**

### **1. ML Pipeline Components**
- **Source Control**: Git repositories with ML code and configurations
- **Build Stage**: Container creation, dependency management, testing
- **Training Stage**: Model training on Vertex AI with parameter tracking
- **Validation Stage**: Model evaluation, performance testing, approval gates
- **Deployment Stage**: Model deployment to Vertex AI Endpoints
- **Monitoring Stage**: Performance monitoring and drift detection

### **2. GCP Services Integration**
- **Cloud Build**: CI/CD orchestration and container builds
- **Vertex AI Pipelines**: ML workflow orchestration
- **Vertex AI Model Registry**: Model versioning and artifact management
- **Cloud Storage**: Artifact storage and data versioning
- **Cloud Monitoring**: Pipeline and model monitoring

## **Cloud Build Configuration**

### **Basic cloudbuild.yaml Template**
```yaml
steps:
  # Step 1: Install dependencies and run tests
  - name: 'python:3.9'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        pip install -r requirements.txt
        python -m pytest tests/ -v
        python -m flake8 src/ --max-line-length=100

  # Step 2: Build and push container
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - 'gcr.io/$PROJECT_ID/ml-pipeline:$COMMIT_SHA'
      - '-t'
      - 'gcr.io/$PROJECT_ID/ml-pipeline:latest'
      - '.'

  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - 'gcr.io/$PROJECT_ID/ml-pipeline:$COMMIT_SHA'

  # Step 3: Submit Vertex AI Pipeline
  - name: 'gcr.io/$PROJECT_ID/vertex-ai-cli'
    entrypoint: 'python'
    args:
      - 'pipelines/submit_pipeline.py'
      - '--project-id=$PROJECT_ID'
      - '--region=us-central1'
      - '--pipeline-template=pipelines/training_pipeline.yaml'
      - '--model-version=$COMMIT_SHA'

substitutions:
  _REGION: 'us-central1'
  _ARTIFACT_REGISTRY: 'gcr.io/$PROJECT_ID'

options:
  logging: CLOUD_LOGGING_ONLY
  machineType: 'E2_HIGHCPU_8'
```

## **Vertex AI Pipeline Templates**

### **Training Pipeline Structure**
```python
from kfp.v2 import dsl
from kfp.v2.dsl import component, pipeline, Input, Output, Dataset, Model, Metrics

@component(
    base_image="gcr.io/project/ml-base:latest",
    packages_to_install=["scikit-learn==1.3.0", "pandas==2.0.0"]
)
def data_preprocessing(
    input_dataset: Input[Dataset],
    processed_dataset: Output[Dataset],
    test_size: float = 0.2
):
    """Data preprocessing component."""
    import pandas as pd
    from sklearn.model_selection import train_test_split
    
    # Load and process data
    df = pd.read_csv(input_dataset.path)
    # ... preprocessing logic ...
    
    # Save processed data
    df.to_csv(processed_dataset.path, index=False)

@component(base_image="gcr.io/project/ml-base:latest")
def train_model(
    dataset: Input[Dataset],
    model: Output[Model],
    metrics: Output[Metrics],
    learning_rate: float = 0.01
):
    """Model training component."""
    import joblib
    import json
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, f1_score
    
    # Load data and train model
    # ... training logic ...
    
    # Save model
    joblib.dump(trained_model, model.path + '/model.joblib')
    
    # Save metrics
    metrics_dict = {
        'accuracy': accuracy,
        'f1_score': f1,
        'feature_importance': feature_importance.tolist()
    }
    with open(metrics.path, 'w') as f:
        json.dump(metrics_dict, f)

@pipeline(
    name="ml-training-pipeline",
    description="End-to-end ML training pipeline"
)
def training_pipeline(
    input_data_path: str,
    model_name: str,
    learning_rate: float = 0.01,
    test_size: float = 0.2
):
    """Complete training pipeline."""
    
    # Data preprocessing
    preprocess_task = data_preprocessing(
        input_dataset=input_data_path,
        test_size=test_size
    )
    
    # Model training
    train_task = train_model(
        dataset=preprocess_task.outputs['processed_dataset'],
        learning_rate=learning_rate
    )
    
    # Model validation
    validate_task = validate_model(
        model=train_task.outputs['model'],
        test_dataset=preprocess_task.outputs['processed_dataset']
    )
    
    # Model registration (conditional on validation)
    with dsl.Condition(validate_task.outputs['approval'] == 'approved'):
        register_task = register_model(
            model=train_task.outputs['model'],
            model_name=model_name,
            metrics=train_task.outputs['metrics']
        )
```

## **Deployment Strategies**

### **1. Blue-Green Deployment**
```python
def deploy_model_blue_green(
    model_registry_name: str,
    model_version: str,
    endpoint_name: str,
    traffic_percentage: int = 10
):
    """Deploy model using blue-green strategy."""
    
    # Deploy new version with limited traffic
    deployment_config = {
        'deployed_model': {
            'model': model_registry_name,
            'display_name': f'{model_version}-deployment',
            'traffic_percentage': traffic_percentage
        }
    }
    
    # Monitor performance before full rollout
    # ... monitoring logic ...
    
    # If successful, gradually increase traffic
    # ... traffic management logic ...
```

### **2. Canary Deployment**
```yaml
# Vertex AI Endpoint configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: deployment-config
data:
  canary_percentage: "5"
  rollout_strategy: "gradual"
  success_threshold: "0.95"
  monitoring_duration: "24h"
```

## **Quality Gates and Validation**

### **1. Model Performance Gates**
```python
def validate_model_performance(
    model_metrics: dict,
    baseline_metrics: dict,
    thresholds: dict
) -> bool:
    """Validate model meets performance thresholds."""
    
    checks = {
        'accuracy_improvement': model_metrics['accuracy'] >= baseline_metrics['accuracy'] * thresholds['min_improvement'],
        'precision_threshold': model_metrics['precision'] >= thresholds['min_precision'],
        'recall_threshold': model_metrics['recall'] >= thresholds['min_recall'],
        'f1_threshold': model_metrics['f1_score'] >= thresholds['min_f1']
    }
    
    return all(checks.values())
```

### **2. Data Drift Detection**
```python
def check_data_drift(
    reference_data: str,
    current_data: str,
    drift_threshold: float = 0.1
) -> dict:
    """Check for data drift using statistical tests."""
    
    from scipy import stats
    import pandas as pd
    
    ref_df = pd.read_csv(reference_data)
    curr_df = pd.read_csv(current_data)
    
    drift_results = {}
    for column in ref_df.select_dtypes(include=[np.number]).columns:
        statistic, p_value = stats.ks_2samp(ref_df[column], curr_df[column])
        drift_results[column] = {
            'drift_detected': p_value < drift_threshold,
            'p_value': p_value,
            'statistic': statistic
        }
    
    return drift_results
```

## **Monitoring and Alerting**

### **1. Pipeline Monitoring**
```yaml
# Cloud Monitoring alert policy
displayName: "ML Pipeline Failure Alert"
conditions:
  - displayName: "Pipeline execution failure"
    conditionThreshold:
      filter: 'resource.type="cloud_build"'
      comparison: COMPARISON_EQUAL
      thresholdValue: 1
      duration: "60s"
alertStrategy:
  notificationRateLimit:
    period: "300s"
```

### **2. Model Performance Monitoring**
```python
def setup_model_monitoring(
    endpoint_name: str,
    feature_thresholds: dict,
    prediction_thresholds: dict
):
    """Setup continuous model monitoring."""
    
    monitoring_config = {
        'prediction_drift_detection': {
            'drift_thresholds': prediction_thresholds,
            'sampling_rate': 0.1
        },
        'feature_drift_detection': {
            'drift_thresholds': feature_thresholds,
            'sampling_rate': 0.1
        },
        'explanation_config': {
            'enable_feature_attributes': True
        }
    }
    
    return monitoring_config
```

## **Security and Compliance**

### **1. Secret Management**
- Use **Secret Manager** for API keys and credentials
- Implement **least privilege** IAM policies
- Enable **audit logging** for all pipeline activities
- Use **Workload Identity** for secure GKE authentication

### **2. Data Governance**
- Implement **data lineage** tracking
- Ensure **GDPR/CCPA compliance** for personal data
- Use **Data Loss Prevention (DLP)** API for sensitive data detection
- Maintain **model cards** for documentation and transparency

## **Best Practices**

1. **Version Everything**: Code, data, models, and pipeline configurations
2. **Automated Testing**: Unit tests, integration tests, and model validation tests
3. **Gradual Rollouts**: Use canary deployments for production models
4. **Monitoring**: Comprehensive monitoring of data, models, and infrastructure
5. **Rollback Strategy**: Quick rollback mechanisms for failed deployments
6. **Documentation**: Clear documentation of pipeline stages and dependencies
