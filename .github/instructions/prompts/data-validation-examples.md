---
applyTo: ["data-validation", "examples", "quality-assurance", "testing"]
description: "Data validation prompt examples and frameworks"
tags: ["data-quality", "validation", "testing", "monitoring", "great-expectations"]
priority: "medium"
---

# Data Validation Prompt Examples

## Prompt: Implement Data Quality Framework

**User Input:**
"I need to implement comprehensive data validation for our customer data pipeline. The data comes from multiple sources and we've been having issues with inconsistent formats and missing values."

**Expected Response Format:**

### Data Validation Implementation

```python
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import logging
from datetime import datetime, timedelta

class CustomerDataValidator:
    """Comprehensive data validator for customer data pipeline."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.validation_results = {}
    
    def validate_schema(self, df: pd.DataFrame) -> bool:
        """Validate DataFrame schema against expected structure."""
        expected_columns = self.config['schema']['required_columns']
        expected_types = self.config['schema']['column_types']
        
        # Check required columns
        missing_columns = set(expected_columns) - set(df.columns)
        if missing_columns:
            self.logger.error(f"Missing required columns: {missing_columns}")
            return False
        
        # Validate data types
        for column, expected_type in expected_types.items():
            if column in df.columns:
                if not df[column].dtype == expected_type:
                    self.logger.warning(
                        f"Column {column} has type {df[column].dtype}, "
                        f"expected {expected_type}"
                    )
        
        return True
    
    def validate_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Perform comprehensive data quality checks."""
        results = {
            'timestamp': datetime.now(),
            'total_records': len(df),
            'quality_checks': {}
        }
        
        # Completeness check
        null_percentages = df.isnull().sum() / len(df)
        results['quality_checks']['completeness'] = {
            'null_percentages': null_percentages.to_dict(),
            'failed_threshold': null_percentages[
                null_percentages > self.config['thresholds']['max_null_percentage']
            ].to_dict()
        }
        
        # Uniqueness check
        if 'unique_columns' in self.config:
            for column in self.config['unique_columns']:
                if column in df.columns:
                    duplicate_count = df[column].duplicated().sum()
                    results['quality_checks'][f'{column}_uniqueness'] = {
                        'duplicate_count': duplicate_count,
                        'duplicate_percentage': duplicate_count / len(df)
                    }
        
        # Business rules validation
        results['quality_checks']['business_rules'] = {}
        for rule_name, rule_config in self.config.get('business_rules', {}).items():
            validation_result = self._validate_business_rule(df, rule_config)
            results['quality_checks']['business_rules'][rule_name] = validation_result
        
        # Data freshness check
        if 'timestamp_column' in self.config:
            timestamp_col = self.config['timestamp_column']
            if timestamp_col in df.columns:
                latest_timestamp = df[timestamp_col].max()
                age_hours = (datetime.now() - latest_timestamp).total_seconds() / 3600
                results['quality_checks']['freshness'] = {
                    'latest_timestamp': latest_timestamp,
                    'age_hours': age_hours,
                    'is_fresh': age_hours <= self.config['thresholds']['max_age_hours']
                }
        
        return results
    
    def _validate_business_rule(self, df: pd.DataFrame, rule_config: Dict) -> Dict:
        """Validate specific business rule."""
        rule_type = rule_config['type']
        
        if rule_type == 'range_check':
            column = rule_config['column']
            min_val = rule_config.get('min_value')
            max_val = rule_config.get('max_value')
            
            if column in df.columns:
                violations = 0
                if min_val is not None:
                    violations += (df[column] < min_val).sum()
                if max_val is not None:
                    violations += (df[column] > max_val).sum()
                
                return {
                    'violations': violations,
                    'violation_percentage': violations / len(df),
                    'passed': violations == 0
                }
        
        elif rule_type == 'pattern_check':
            column = rule_config['column']
            pattern = rule_config['pattern']
            
            if column in df.columns:
                matches = df[column].str.match(pattern, na=False)
                violations = (~matches).sum()
                
                return {
                    'violations': violations,
                    'violation_percentage': violations / len(df),
                    'passed': violations == 0
                }
        
        return {'error': f'Unknown rule type: {rule_type}'}
    
    def generate_quality_report(self, validation_results: Dict) -> str:
        """Generate human-readable quality report."""
        report = []
        report.append("=== DATA QUALITY REPORT ===")
        report.append(f"Timestamp: {validation_results['timestamp']}")
        report.append(f"Total Records: {validation_results['total_records']:,}")
        report.append("")
        
        # Completeness Report
        completeness = validation_results['quality_checks']['completeness']
        report.append("COMPLETENESS:")
        for column, null_pct in completeness['null_percentages'].items():
            status = "✓" if null_pct < 0.05 else "⚠️" if null_pct < 0.1 else "❌"
            report.append(f"  {status} {column}: {null_pct:.2%} null values")
        
        # Business Rules Report
        business_rules = validation_results['quality_checks']['business_rules']
        if business_rules:
            report.append("\nBUSINESS RULES:")
            for rule_name, result in business_rules.items():
                status = "✓" if result.get('passed', False) else "❌"
                violations = result.get('violations', 0)
                report.append(f"  {status} {rule_name}: {violations} violations")
        
        # Data Freshness Report
        if 'freshness' in validation_results['quality_checks']:
            freshness = validation_results['quality_checks']['freshness']
            status = "✓" if freshness['is_fresh'] else "❌"
            report.append(f"\nFRESHNESS:")
            report.append(f"  {status} Data age: {freshness['age_hours']:.1f} hours")
        
        return "\n".join(report)

# Configuration example
validation_config = {
    'schema': {
        'required_columns': ['customer_id', 'email', 'registration_date', 'status'],
        'column_types': {
            'customer_id': 'int64',
            'email': 'object',
            'registration_date': 'datetime64[ns]',
            'status': 'object'
        }
    },
    'thresholds': {
        'max_null_percentage': 0.05,  # 5%
        'max_age_hours': 24
    },
    'unique_columns': ['customer_id', 'email'],
    'timestamp_column': 'registration_date',
    'business_rules': {
        'valid_email_format': {
            'type': 'pattern_check',
            'column': 'email',
            'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        },
        'valid_customer_id': {
            'type': 'range_check',
            'column': 'customer_id',
            'min_value': 1,
            'max_value': 99999999
        }
    }
}

# Usage example
def validate_customer_data(df: pd.DataFrame):
    """Main validation function for customer data."""
    validator = CustomerDataValidator(validation_config)
    
    # Schema validation
    if not validator.validate_schema(df):
        raise ValueError("Schema validation failed")
    
    # Quality validation
    results = validator.validate_data_quality(df)
    
    # Generate report
    report = validator.generate_quality_report(results)
    print(report)
    
    # Check if validation passed
    overall_quality_score = calculate_quality_score(results)
    if overall_quality_score < 0.95:  # 95% threshold
        raise ValueError(f"Data quality too low: {overall_quality_score:.2%}")
    
    return results

def calculate_quality_score(results: Dict) -> float:
    """Calculate overall data quality score."""
    scores = []
    
    # Completeness score
    null_percentages = results['quality_checks']['completeness']['null_percentages']
    completeness_score = 1 - max(null_percentages.values())
    scores.append(completeness_score)
    
    # Business rules score
    business_rules = results['quality_checks']['business_rules']
    if business_rules:
        passed_rules = sum(1 for rule in business_rules.values() if rule.get('passed', False))
        business_score = passed_rules / len(business_rules)
        scores.append(business_score)
    
    # Freshness score
    if 'freshness' in results['quality_checks']:
        freshness_score = 1 if results['quality_checks']['freshness']['is_fresh'] else 0
        scores.append(freshness_score)
    
    return sum(scores) / len(scores) if scores else 0
```

### Integration with Data Pipeline

```python
# Airflow integration example
from airflow import DAG
from airflow.operators.python import PythonOperator

def data_validation_task(**context):
    """Airflow task for data validation."""
    # Load data
    df = load_data_from_source()
    
    # Validate data
    try:
        validation_results = validate_customer_data(df)
        
        # Store validation results
        store_validation_results(validation_results)
        
        # Send success notification
        send_notification("Data validation passed", "success")
        
    except ValueError as e:
        # Handle validation failure
        send_notification(f"Data validation failed: {str(e)}", "error")
        raise

# Add to DAG
validation_task = PythonOperator(
    task_id='validate_customer_data',
    python_callable=data_validation_task,
    dag=dag
)
```

---

## Prompt: Set Up Monitoring for Data Quality

**User Input:**
"We need to set up automated monitoring for our data quality metrics. I want alerts when data quality drops below certain thresholds and a dashboard showing trends over time."

**Expected Response Format:**

### Data Quality Monitoring System

```python
import pandas as pd
from google.cloud import monitoring_v3
from google.cloud import bigquery
import json
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

class DataQualityMonitor:
    """Monitor and alert on data quality metrics."""
    
    def __init__(self, project_id: str, dataset_id: str):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.bq_client = bigquery.Client(project=project_id)
        self.monitoring_client = monitoring_v3.MetricServiceClient()
        
    def create_custom_metrics(self):
        """Create custom Cloud Monitoring metrics for data quality."""
        project_name = f"projects/{self.project_id}"
        
        metrics_to_create = [
            {
                'type': 'custom.googleapis.com/data_quality/completeness_score',
                'metric_kind': monitoring_v3.MetricDescriptor.MetricKind.GAUGE,
                'value_type': monitoring_v3.MetricDescriptor.ValueType.DOUBLE,
                'description': 'Data completeness score (0-1)'
            },
            {
                'type': 'custom.googleapis.com/data_quality/accuracy_score',
                'metric_kind': monitoring_v3.MetricDescriptor.MetricKind.GAUGE,
                'value_type': monitoring_v3.MetricDescriptor.ValueType.DOUBLE,
                'description': 'Data accuracy score (0-1)'
            },
            {
                'type': 'custom.googleapis.com/data_quality/freshness_hours',
                'metric_kind': monitoring_v3.MetricDescriptor.MetricKind.GAUGE,
                'value_type': monitoring_v3.MetricDescriptor.ValueType.DOUBLE,
                'description': 'Data age in hours'
            }
        ]
        
        for metric_config in metrics_to_create:
            descriptor = monitoring_v3.MetricDescriptor(
                type=metric_config['type'],
                metric_kind=metric_config['metric_kind'],
                value_type=metric_config['value_type'],
                description=metric_config['description']
            )
            
            try:
                self.monitoring_client.create_metric_descriptor(
                    name=project_name, 
                    metric_descriptor=descriptor
                )
                print(f"Created metric: {metric_config['type']}")
            except Exception as e:
                print(f"Metric might already exist: {e}")
    
    def send_metric_to_monitoring(self, metric_type: str, value: float, labels: dict = None):
        """Send custom metric to Cloud Monitoring."""
        project_name = f"projects/{self.project_id}"
        
        series = monitoring_v3.TimeSeries()
        series.metric.type = metric_type
        
        if labels:
            for key, val in labels.items():
                series.metric.labels[key] = val
        
        series.resource.type = 'global'
        
        now = datetime.utcnow()
        seconds = int(now.timestamp())
        nanos = int((now.timestamp() - seconds) * 10**9)
        
        interval = monitoring_v3.TimeInterval(
            {"end_time": {"seconds": seconds, "nanos": nanos}}
        )
        
        point = monitoring_v3.Point(
            {"interval": interval, "value": {"double_value": value}}
        )
        
        series.points = [point]
        
        self.monitoring_client.create_time_series(
            name=project_name, 
            time_series=[series]
        )
    
    def calculate_and_send_metrics(self, table_name: str):
        """Calculate quality metrics and send to monitoring."""
        # Query data quality metrics
        query = f"""
        WITH quality_metrics AS (
            SELECT 
                -- Completeness metrics
                COUNTIF(customer_id IS NOT NULL) / COUNT(*) as customer_id_completeness,
                COUNTIF(email IS NOT NULL) / COUNT(*) as email_completeness,
                COUNTIF(registration_date IS NOT NULL) / COUNT(*) as date_completeness,
                
                -- Accuracy metrics
                COUNTIF(REGEXP_CONTAINS(email, r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{{2,}}$')) / 
                COUNTIF(email IS NOT NULL) as email_accuracy,
                
                -- Freshness metrics
                DATETIME_DIFF(CURRENT_DATETIME(), MAX(registration_date), HOUR) as data_age_hours,
                
                COUNT(*) as total_records
            FROM `{self.project_id}.{self.dataset_id}.{table_name}`
        )
        SELECT 
            (customer_id_completeness + email_completeness + date_completeness) / 3 as avg_completeness,
            email_accuracy,
            data_age_hours,
            total_records
        FROM quality_metrics
        """
        
        result = self.bq_client.query(query).to_dataframe()
        
        if not result.empty:
            row = result.iloc[0]
            
            # Send metrics to monitoring
            self.send_metric_to_monitoring(
                'custom.googleapis.com/data_quality/completeness_score',
                float(row['avg_completeness']),
                {'table': table_name}
            )
            
            self.send_metric_to_monitoring(
                'custom.googleapis.com/data_quality/accuracy_score',
                float(row['email_accuracy']),
                {'table': table_name}
            )
            
            self.send_metric_to_monitoring(
                'custom.googleapis.com/data_quality/freshness_hours',
                float(row['data_age_hours']),
                {'table': table_name}
            )
            
            return {
                'completeness_score': float(row['avg_completeness']),
                'accuracy_score': float(row['email_accuracy']),
                'freshness_hours': float(row['data_age_hours']),
                'total_records': int(row['total_records'])
            }
    
    def check_thresholds_and_alert(self, metrics: dict, table_name: str):
        """Check quality metrics against thresholds and send alerts."""
        thresholds = {
            'completeness_score': 0.95,
            'accuracy_score': 0.98,
            'freshness_hours': 24
        }
        
        alerts = []
        
        for metric_name, value in metrics.items():
            if metric_name in thresholds:
                threshold = thresholds[metric_name]
                
                if metric_name == 'freshness_hours':
                    # For freshness, alert if value is ABOVE threshold
                    if value > threshold:
                        alerts.append(
                            f"❌ Data freshness alert: {value:.1f} hours old "
                            f"(threshold: {threshold} hours)"
                        )
                else:
                    # For other metrics, alert if value is BELOW threshold
                    if value < threshold:
                        alerts.append(
                            f"❌ {metric_name.replace('_', ' ').title()} alert: "
                            f"{value:.2%} (threshold: {threshold:.2%})"
                        )
        
        if alerts:
            alert_message = f"Data Quality Alerts for {table_name}:\n\n" + "\n".join(alerts)
            self.send_alert(alert_message, severity='HIGH')
        else:
            print(f"✅ All quality metrics for {table_name} are within thresholds")
    
    def send_alert(self, message: str, severity: str = 'MEDIUM'):
        """Send alert notification."""
        # Email alert
        self.send_email_alert(message, severity)
        
        # Slack alert (if configured)
        # self.send_slack_alert(message, severity)
        
        # Log alert
        print(f"[{severity}] ALERT: {message}")
    
    def send_email_alert(self, message: str, severity: str):
        """Send email alert."""
        sender_email = "alerts@company.com"
        receiver_emails = ["data-team@company.com", "ops@company.com"]
        
        subject = f"[{severity}] Data Quality Alert"
        
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = ", ".join(receiver_emails)
        
        # Configure SMTP server
        try:
            with smtplib.SMTP('smtp.company.com', 587) as server:
                server.starttls()
                server.login(sender_email, "password")  # Use environment variable
                server.send_message(msg)
                print("Alert email sent successfully")
        except Exception as e:
            print(f"Failed to send email alert: {e}")

# Monitoring dashboard query
DASHBOARD_QUERY = """
WITH daily_quality AS (
    SELECT 
        DATE(created_at) as date,
        COUNTIF(customer_id IS NOT NULL) / COUNT(*) as completeness_score,
        COUNTIF(REGEXP_CONTAINS(email, r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')) / 
        COUNTIF(email IS NOT NULL) as accuracy_score,
        COUNT(*) as record_count
    FROM `{project}.{dataset}.{table}`
    WHERE created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
    GROUP BY DATE(created_at)
    ORDER BY date DESC
)
SELECT 
    date,
    completeness_score,
    accuracy_score,
    record_count,
    AVG(completeness_score) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as completeness_7day_avg,
    AVG(accuracy_score) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as accuracy_7day_avg
FROM daily_quality
"""

# Usage in Airflow DAG
def monitor_data_quality_task(**context):
    """Airflow task for data quality monitoring."""
    monitor = DataQualityMonitor('my-project', 'analytics')
    
    tables_to_monitor = ['customers', 'orders', 'products']
    
    for table in tables_to_monitor:
        # Calculate metrics
        metrics = monitor.calculate_and_send_metrics(table)
        
        # Check thresholds and alert
        monitor.check_thresholds_and_alert(metrics, table)
        
        # Log results
        print(f"Quality metrics for {table}: {metrics}")
```
