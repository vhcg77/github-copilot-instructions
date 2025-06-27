---
applyTo: ["etl", "pipelines", "data-engineering", "data-processing"]
description: "ETL pipeline design and implementation instructions"
priority: "high"
---

# ETL Pipeline Development Instructions

## Objective
Design and implement robust, scalable ETL (Extract, Transform, Load) pipelines that efficiently process data from multiple sources to support analytics and machine learning workflows.

## Pipeline Architecture

### 1. Extract Phase
```python
# Multi-source data extraction
from abc import ABC, abstractmethod
import pandas as pd
from google.cloud import bigquery, storage

class DataExtractor(ABC):
    @abstractmethod
    def extract(self, **kwargs) -> pd.DataFrame:
        pass

class BigQueryExtractor(DataExtractor):
    def __init__(self, project_id: str):
        self.client = bigquery.Client(project=project_id)
    
    def extract(self, query: str, **kwargs) -> pd.DataFrame:
        """Extract data from BigQuery."""
        return self.client.query(query).to_dataframe()

class CloudStorageExtractor(DataExtractor):
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.client = storage.Client()
    
    def extract(self, blob_name: str, **kwargs) -> pd.DataFrame:
        """Extract data from Cloud Storage."""
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(blob_name)
        return pd.read_csv(blob.open())
```

### 2. Transform Phase
```python
# Data transformation pipeline
from typing import List, Callable
import numpy as np

class DataTransformer:
    def __init__(self):
        self.transformations: List[Callable] = []
    
    def add_transformation(self, func: Callable):
        """Add transformation function to pipeline."""
        self.transformations.append(func)
        return self
    
    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        """Execute all transformations in sequence."""
        for transform in self.transformations:
            df = transform(df)
        return df

# Example transformations
def clean_null_values(df: pd.DataFrame) -> pd.DataFrame:
    """Remove or impute null values."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    
    categorical_cols = df.select_dtypes(include=['object']).columns
    df[categorical_cols] = df[categorical_cols].fillna('Unknown')
    
    return df

def standardize_formats(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize data formats."""
    # Convert date columns
    date_cols = ['created_date', 'updated_date']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
    
    # Standardize text columns
    text_cols = df.select_dtypes(include=['object']).columns
    for col in text_cols:
        df[col] = df[col].str.strip().str.lower()
    
    return df
```

### 3. Load Phase
```python
# Data loading strategies
class DataLoader:
    def __init__(self, destination_config: dict):
        self.config = destination_config
    
    def load_to_bigquery(self, df: pd.DataFrame, table_id: str, 
                        write_disposition: str = 'WRITE_TRUNCATE'):
        """Load data to BigQuery table."""
        client = bigquery.Client(project=self.config['project_id'])
        
        job_config = bigquery.LoadJobConfig(
            write_disposition=write_disposition,
            autodetect=True
        )
        
        job = client.load_table_from_dataframe(
            df, table_id, job_config=job_config
        )
        job.result()  # Wait for job to complete
        
    def load_to_storage(self, df: pd.DataFrame, blob_name: str):
        """Load data to Cloud Storage."""
        client = storage.Client()
        bucket = client.bucket(self.config['bucket_name'])
        blob = bucket.blob(blob_name)
        
        blob.upload_from_string(df.to_csv(index=False), 'text/csv')
```

## Pipeline Orchestration

### 1. Apache Airflow Implementation
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'daily_etl_pipeline',
    default_args=default_args,
    description='Daily ETL pipeline for customer data',
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    catchup=False,
    max_active_runs=1
)

def extract_data(**context):
    """Extract data from source systems."""
    extractor = BigQueryExtractor(project_id='my-project')
    data = extractor.extract("""
        SELECT * FROM source_table 
        WHERE date = '{{ ds }}'
    """)
    # Save to temporary location
    data.to_parquet(f'/tmp/extracted_data_{{ ds }}.parquet')

def transform_data(**context):
    """Transform extracted data."""
    df = pd.read_parquet(f'/tmp/extracted_data_{{ ds }}.parquet')
    
    transformer = DataTransformer()
    transformer.add_transformation(clean_null_values)
    transformer.add_transformation(standardize_formats)
    
    transformed_df = transformer.execute(df)
    transformed_df.to_parquet(f'/tmp/transformed_data_{{ ds }}.parquet')

def load_data(**context):
    """Load transformed data to destination."""
    df = pd.read_parquet(f'/tmp/transformed_data_{{ ds }}.parquet')
    
    loader = DataLoader({'project_id': 'my-project'})
    loader.load_to_bigquery(df, 'analytics.customer_data')

# Define tasks
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag
)

# Set dependencies
extract_task >> transform_task >> load_task
```

### 2. Error Handling and Monitoring
```python
import logging
from typing import Optional

class PipelineMonitor:
    def __init__(self, pipeline_name: str):
        self.pipeline_name = pipeline_name
        self.logger = logging.getLogger(pipeline_name)
    
    def log_start(self, stage: str):
        """Log pipeline stage start."""
        self.logger.info(f"Starting {stage} for {self.pipeline_name}")
    
    def log_completion(self, stage: str, records_processed: int):
        """Log successful completion."""
        self.logger.info(
            f"Completed {stage} for {self.pipeline_name}. "
            f"Records processed: {records_processed}"
        )
    
    def log_error(self, stage: str, error: Exception):
        """Log pipeline errors."""
        self.logger.error(
            f"Error in {stage} for {self.pipeline_name}: {str(error)}"
        )
    
    def send_alert(self, message: str):
        """Send alert to monitoring system."""
        # Integration with alerting system (Slack, email, etc.)
        pass

class RobustPipeline:
    def __init__(self, name: str):
        self.name = name
        self.monitor = PipelineMonitor(name)
    
    def execute_with_monitoring(self, stage_func, stage_name: str, *args, **kwargs):
        """Execute pipeline stage with monitoring."""
        try:
            self.monitor.log_start(stage_name)
            result = stage_func(*args, **kwargs)
            
            # Count processed records if result is DataFrame
            record_count = len(result) if hasattr(result, '__len__') else 0
            self.monitor.log_completion(stage_name, record_count)
            
            return result
        except Exception as e:
            self.monitor.log_error(stage_name, e)
            self.monitor.send_alert(f"Pipeline failure in {stage_name}: {str(e)}")
            raise
```

## Data Quality Framework

### 1. Quality Checks
```python
class DataQualityChecker:
    def __init__(self, rules: dict):
        self.rules = rules
    
    def validate_schema(self, df: pd.DataFrame) -> bool:
        """Validate DataFrame schema."""
        expected_columns = set(self.rules.get('required_columns', []))
        actual_columns = set(df.columns)
        
        missing_columns = expected_columns - actual_columns
        if missing_columns:
            raise ValueError(f"Missing columns: {missing_columns}")
        
        return True
    
    def validate_data_quality(self, df: pd.DataFrame) -> dict:
        """Perform comprehensive data quality checks."""
        quality_report = {
            'total_records': len(df),
            'null_percentages': df.isnull().sum() / len(df),
            'duplicate_count': df.duplicated().sum(),
            'data_types': df.dtypes.to_dict()
        }
        
        # Check business rules
        for rule_name, rule_func in self.rules.get('business_rules', {}).items():
            quality_report[rule_name] = rule_func(df)
        
        return quality_report
```

### 2. Performance Optimization
```python
# Chunked processing for large datasets
def process_large_dataset(file_path: str, chunk_size: int = 10000):
    """Process large datasets in chunks."""
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        # Process chunk
        transformed_chunk = transform_data(chunk)
        
        # Load to destination
        load_data(transformed_chunk)

# Parallel processing
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

def parallel_transform(data_chunks: List[pd.DataFrame]) -> List[pd.DataFrame]:
    """Transform data chunks in parallel."""
    with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        futures = [executor.submit(transform_data, chunk) for chunk in data_chunks]
        return [future.result() for future in futures]
```

## Best Practices

### 1. Configuration Management
```yaml
# pipeline_config.yaml
pipeline:
  name: "customer_data_pipeline"
  schedule: "0 2 * * *"
  
sources:
  - name: "crm_database"
    type: "postgresql"
    connection_string: "${CRM_DB_URL}"
  - name: "analytics_files"
    type: "gcs"
    bucket: "analytics-raw-data"

transformations:
  - clean_null_values
  - standardize_formats
  - calculate_derived_metrics

destinations:
  - name: "data_warehouse"
    type: "bigquery"
    dataset: "analytics"
    table: "customer_data"

quality_rules:
  required_columns: ["customer_id", "created_date"]
  max_null_percentage: 0.05
  duplicate_threshold: 0.01
```

### 2. Testing Strategy
```python
import pytest
from unittest.mock import Mock, patch

class TestETLPipeline:
    def test_data_extraction(self):
        """Test data extraction functionality."""
        extractor = BigQueryExtractor('test-project')
        
        with patch.object(extractor.client, 'query') as mock_query:
            mock_query.return_value.to_dataframe.return_value = pd.DataFrame({
                'id': [1, 2, 3],
                'name': ['A', 'B', 'C']
            })
            
            result = extractor.extract("SELECT * FROM test_table")
            assert len(result) == 3
            assert 'id' in result.columns
    
    def test_data_transformation(self):
        """Test data transformation logic."""
        df = pd.DataFrame({
            'value': [1, None, 3],
            'text': [' Hello ', None, ' World ']
        })
        
        cleaned_df = clean_null_values(df)
        assert cleaned_df['value'].isnull().sum() == 0
        assert cleaned_df['text'].isnull().sum() == 0
    
    def test_quality_validation(self):
        """Test data quality checks."""
        df = pd.DataFrame({'required_col': [1, 2, 3]})
        rules = {'required_columns': ['required_col']}
        
        checker = DataQualityChecker(rules)
        assert checker.validate_schema(df) == True
```

### 3. Documentation Requirements
- Pipeline architecture diagrams
- Data lineage documentation
- Transformation logic specifications
- Quality check definitions
- Monitoring and alerting setup
- Disaster recovery procedures
- Performance optimization guide

## Deployment and Operations

### 1. Infrastructure as Code
```terraform
# ETL infrastructure
resource "google_composer_environment" "etl_environment" {
  name     = "etl-production"
  region   = var.region
  
  config {
    software_config {
      image_version = "composer-2-airflow-2"
      pypi_packages = {
        "pandas" = ">=1.5.0"
        "google-cloud-bigquery" = ">=3.0.0"
      }
    }
    
    node_config {
      zone         = var.zone
      machine_type = "n1-standard-2"
      disk_size_gb = 100
    }
  }
}
```

### 2. Monitoring and Alerting
- Pipeline execution metrics
- Data freshness monitoring
- Quality score tracking
- Performance benchmarks
- Error rate alerting
- SLA compliance monitoring
