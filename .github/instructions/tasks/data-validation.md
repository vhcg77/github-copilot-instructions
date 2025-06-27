---
applyTo: ["data-validation", "quality-assurance", "testing", "data-integrity"]
description: "Data validation frameworks and quality monitoring instructions"
priority: "high"
---

# Data Validation Instructions

## Objective
Ensure data quality, integrity, and reliability throughout the data pipeline from ingestion to model outputs, implementing comprehensive validation frameworks for data science projects.

## Validation Framework

### 1. Data Ingestion Validation
```python
# Schema validation example
def validate_schema(df, expected_schema):
    """Validate DataFrame against expected schema."""
    assert df.columns.tolist() == expected_schema['columns']
    for col, dtype in expected_schema['dtypes'].items():
        assert df[col].dtype == dtype
    return True

# Data freshness validation
def validate_freshness(df, timestamp_col, max_age_hours=24):
    """Ensure data is within acceptable freshness window."""
    latest_timestamp = df[timestamp_col].max()
    age_hours = (pd.Timestamp.now() - latest_timestamp).total_seconds() / 3600
    assert age_hours <= max_age_hours, f"Data too old: {age_hours} hours"
```

### 2. Data Quality Checks
- **Completeness**: Check for missing values, null percentages
- **Consistency**: Validate data formats, value ranges
- **Accuracy**: Cross-reference with source systems
- **Uniqueness**: Identify and handle duplicates
- **Validity**: Ensure data conforms to business rules

### 3. Statistical Validation
```python
# Data distribution validation
def validate_distribution(df, column, expected_stats):
    """Validate statistical properties of data."""
    actual_mean = df[column].mean()
    actual_std = df[column].std()
    
    assert abs(actual_mean - expected_stats['mean']) < expected_stats['tolerance']
    assert abs(actual_std - expected_stats['std']) < expected_stats['tolerance']
```

## Validation Rules

### Business Rules Validation
- **Domain-specific constraints**: Revenue > 0, Age between 0-120
- **Referential integrity**: Foreign key relationships
- **Business logic**: Order date <= Delivery date
- **Regulatory compliance**: Data retention, privacy rules

### Data Pipeline Validation
1. **Input Validation**: Raw data quality checks
2. **Transformation Validation**: ETL process verification
3. **Output Validation**: Final dataset quality
4. **Model Input Validation**: Feature engineering results

## Testing Framework

### Unit Tests for Data
```python
import pytest
import pandas as pd
from src.validation import DataValidator

class TestDataValidation:
    def test_schema_validation(self):
        validator = DataValidator()
        df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        assert validator.validate_schema(df, expected_schema)
    
    def test_missing_values(self):
        df = pd.DataFrame({'col1': [1, None, 3]})
        assert validator.check_missing_values(df, threshold=0.1) == False
```

### Integration Tests
- End-to-end pipeline validation
- Data flow integrity checks
- Performance benchmarks
- Error handling validation

## Monitoring and Alerting

### Data Quality Metrics
- **Completeness Rate**: % of non-null values
- **Accuracy Score**: % of valid values
- **Consistency Index**: Standardization compliance
- **Timeliness Metric**: Data freshness score

### Alert Thresholds
```yaml
data_quality_thresholds:
  completeness: 0.95
  accuracy: 0.98
  freshness_hours: 6
  duplicate_rate: 0.01
```

### Monitoring Dashboard
- Real-time data quality metrics
- Trend analysis and anomaly detection
- Alert history and resolution tracking
- Data lineage visualization

## Validation Automation

### CI/CD Integration
```yaml
# .github/workflows/data-validation.yml
name: Data Validation
on:
  push:
    paths: ['data/**', 'src/etl/**']

jobs:
  validate-data:
    runs-on: ubuntu-latest
    steps:
      - name: Run Data Quality Tests
        run: pytest tests/data_validation/
      
      - name: Generate Data Quality Report
        run: python src/validation/generate_report.py
```

### Scheduled Validation
- Hourly: Critical data freshness checks
- Daily: Comprehensive quality reports
- Weekly: Historical trend analysis
- Monthly: Data governance review

## Documentation Requirements

### Validation Reports
- Data quality scorecards
- Validation rule documentation
- Test coverage reports
- Incident post-mortems

### Standard Operating Procedures
- Data validation workflow
- Alert response procedures
- Escalation protocols
- Quality improvement processes

## Tools and Libraries
- **Python**: Pandas, Numpy, Great Expectations
- **SQL**: Data profiling queries, constraint validation
- **Monitoring**: Apache Airflow, Grafana, DataDog
- **Testing**: Pytest, unittest, data-driven tests
- **Reporting**: Jupyter notebooks, automated reports
