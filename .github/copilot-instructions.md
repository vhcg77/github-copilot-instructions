# **GitHub Copilot General Instructions**

## **About Me**

I am a Senior Data Scientist. My main focus is on developing robust, scalable, and maintainable data science solutions. I work with Python in Visual Studio Code. My expertise includes data cleaning, exploratory data analysis (EDA), statistical modeling, machine learning, and MLOps.

## **About This Project**

This repository contains **utilities for Gasco** - a comprehensive data application built on Google Cloud Platform for inventory analysis and resource management. The project encompasses everything from data engineering and MLOps to frontend development. 

### **Project Structure**
* `/data`: Raw and processed datasets, configuration files
* `/notebooks`: Jupyter notebooks for exploration (e.g., `analisis_exploratorio_inventario.ipynb`)
* `/src`: Modular Python source code (data processing, utilities, documentation tools)
* `/tests`: Unit and integration tests using pytest
* `/terraform`: Infrastructure as Code for GCP deployment
* `/.vscode`: VS Code workspace configuration with GitHub Copilot integration
* `/.github/instructions`: Hierarchical instruction system for GitHub Copilot

### **Current Dataset Context**
- **Primary focus**: Inventory analysis (`inventario_recursos_gasco_2025_06_25.csv`)
- **Asset management**: JSON data for assets tracking (`assets_gasco_2025_06_25.json`)
- **Analysis outputs**: Query analysis logs and structured reports
- **Business domain**: Resource inventory, asset tracking, operational analytics

## **Tech Stack**

This project utilizes a modern, cloud-native tech stack centered around **Python** and **Google Cloud Platform (GCP)**.

The specific technologies and libraries for a given task depend on the role being performed. You **MUST** refer to the detailed tech stack defined in the relevant file within the **`.github/instructions/roles/`** directory (e.g., `data-scientist.md`, `data-engineer.md`, `mlops-engineer.md`, `frontend-developer.md`, `cloud-architect.md`, `qa-engineer.md`, `visualization-engineer.md`, `business-analyst.md`, `project-manager.md`).

## **🔧 VS Code Configuration (CRITICAL)**

This project requires specific VS Code configuration to function properly. The `.vscode/settings.json` file contains:

### **GitHub Copilot Integration**
- **`github.copilot.chat.codeGeneration.useInstructionFiles: true`** - Enables the hierarchical instruction system
- **Task-specific instructions** - Automatic application of role/task-specific guidelines
- **Prompt files support** - Access to `.github/instructions/prompts/` directory
- **Advanced debugging** - Uses Claude Sonnet 4 engine for enhanced capabilities

### **Python & Data Science Settings**
- **Strict type checking** - Enforces type hint requirements
- **Auto-formatting** - Black formatter with PEP 8 compliance
- **Linting enabled** - Pylint and Flake8 for code quality
- **Jupyter integration** - Seamless notebook development
- **Import organization** - Automatic import sorting on save

### **Security & Content Exclusions**
- **Sensitive data protection** - Excludes secrets, environment files, and credentials
- **Large file exclusions** - Prevents processing of large datasets and build artifacts
- **Version control safety** - Excludes `.git` directories and state files

### **Critical Settings Verification**
Before using this system, verify these settings are active in your VS Code:
```json
{
    "github.copilot.chat.codeGeneration.useInstructionFiles": true,
    "chat.promptFiles": true,
    "python.analysis.typeCheckingMode": "strict",
    "editor.formatOnSave": true
}
```

## **General Principles & Coding Style**

1. **Clarity and Readability**: Write clean, self-explanatory code. Follow the PEP 8 style guide.  
2. **Modularity**: Break down complex problems into smaller, reusable functions. Avoid monolithic scripts.  
3. **Documentation**:  
   * All public functions and methods MUST have clear docstrings in the Google Python Style Guide format.  
   * Include type hints for all function arguments and return values. This is mandatory.  
   * Use comments to explain the "why," not the "what," of complex logic.  
4. **Reproducibility**: Ensure that notebooks and scripts are reproducible. Set random seeds where necessary (random\_state=42).  
5. **Efficiency**: Write efficient and vectorized code using pandas and NumPy where possible. Avoid explicit loops over pandas DataFrames.  
6. **Testing**: All new functionality added to the /src directory must be accompanied by corresponding unit tests in /tests.

## **Mandatory Code Standards**

Every piece of code you generate MUST follow these non-negotiable standards:

```python
# ✅ CORRECT EXAMPLE - Follow this pattern exactly
from typing import List, Dict, Optional, Tuple
import pandas as pd
import numpy as np

def process_inventory_data(
    data: pd.DataFrame, 
    columns_to_keep: List[str], 
    threshold: float = 0.95
) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """Process inventory data by cleaning and filtering.
    
    This function removes missing values, filters columns, and applies
    business rules specific to Gasco inventory management.
    
    Args:
        data: Raw inventory DataFrame from CSV source.
        columns_to_keep: List of column names to retain in output.
        threshold: Minimum data completeness threshold (default: 0.95).
        
    Returns:
        Tuple containing:
        - Cleaned DataFrame with selected columns
        - Dictionary with data quality metrics
        
    Raises:
        ValueError: If threshold is not between 0 and 1.
        KeyError: If required columns are missing from data.
    """
    if not 0 <= threshold <= 1:
        raise ValueError(f"Threshold must be between 0 and 1, got {threshold}")
    
    missing_cols = set(columns_to_keep) - set(data.columns)
    if missing_cols:
        raise KeyError(f"Missing required columns: {missing_cols}")
    
    # Use vectorized operations - never loops with pandas
    cleaned_data = data[columns_to_keep].dropna()
    
    metrics = {
        "original_rows": len(data),
        "cleaned_rows": len(cleaned_data),
        "completeness_ratio": len(cleaned_data) / len(data)
    }
    
    return cleaned_data, metrics
```

### **Advanced Data Processing Example**
```python
def analyze_inventory_trends(
    df: pd.DataFrame,
    date_col: str = 'fecha',
    category_col: str = 'categoria',
    amount_col: str = 'cantidad'
) -> Dict[str, pd.DataFrame]:
    """Analyze inventory trends with proper error handling and type hints.
    
    This example demonstrates:
    - Comprehensive type hints for all parameters and return values
    - Proper pandas vectorized operations (NO loops)
    - Error handling with specific exceptions
    - Google-style docstrings with Args, Returns, Raises
    - Random state setting for reproducibility
    
    Args:
        df: Input DataFrame with inventory data
        date_col: Name of date column for time series analysis
        category_col: Name of category column for grouping
        amount_col: Name of numeric column for aggregation
    
    Returns:
        Dictionary containing analysis results:
        - 'trends': Monthly trends by category
        - 'summary': Statistical summary
        - 'outliers': Detected outliers using IQR method
    
    Raises:
        KeyError: If required columns are missing
        ValueError: If date_col cannot be parsed as datetime
    """
    # Input validation - ALWAYS validate inputs
    required_cols = [date_col, category_col, amount_col]
    missing_cols = set(required_cols) - set(df.columns)
    if missing_cols:
        raise KeyError(f"Missing required columns: {missing_cols}")
    
    # Create working copy to avoid modifying original
    df_work = df.copy()
    
    # Parse dates with proper error handling
    try:
        df_work[date_col] = pd.to_datetime(df_work[date_col])
    except (ValueError, TypeError) as e:
        raise ValueError(f"Cannot parse {date_col} as datetime: {e}")
    
    # Vectorized operations - NO explicit loops
    df_work['year_month'] = df_work[date_col].dt.to_period('M')
    
    # Monthly trends by category
    trends = df_work.groupby([category_col, 'year_month'])[amount_col].agg([
        'sum', 'mean', 'count', 'std'
    ]).round(2)
    
    # Statistical summary
    summary = df_work.groupby(category_col)[amount_col].describe()
    
    # Outlier detection using IQR method
    Q1 = df_work[amount_col].quantile(0.25)
    Q3 = df_work[amount_col].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df_work[
        (df_work[amount_col] < Q1 - 1.5 * IQR) | 
        (df_work[amount_col] > Q3 + 1.5 * IQR)
    ]
    
    return {
        'trends': trends.reset_index(),
        'summary': summary,
        'outliers': outliers
    }
```

### **MLOps Pipeline Example with GCP**
```python
import os
from google.cloud import bigquery, storage
from google.cloud.bigquery import LoadJobConfig
import joblib
from typing import Optional, Tuple
import logging

def deploy_model_to_gcp(
    model_path: str,
    bucket_name: str,
    model_name: str,
    version: str = "v1",
    project_id: Optional[str] = None
) -> Tuple[str, str]:
    """Deploy ML model to GCP with proper error handling.
    
    This demonstrates:
    - GCP service integration patterns
    - Proper exception handling for cloud operations  
    - Type hints for cloud resource identifiers
    - Logging for monitoring and debugging
    - Environment variable usage (not hardcoded secrets)
    
    Args:
        model_path: Local path to trained model file
        bucket_name: GCS bucket for model storage
        model_name: Model identifier for deployment
        version: Model version tag
        project_id: GCP project ID (defaults to env var)
    
    Returns:
        Tuple of (model_uri, deployment_status)
    
    Raises:
        FileNotFoundError: If model file doesn't exist
        google.cloud.exceptions.GoogleCloudError: For GCP operation failures
    """
    # Setup logging for monitoring
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Validate model file exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    try:
        # Initialize GCP clients with proper authentication
        storage_client = storage.Client(project=project_id)
        bucket = storage_client.bucket(bucket_name)
        
        # Upload model with versioning
        model_blob_name = f"models/{model_name}/{version}/model.joblib"
        blob = bucket.blob(model_blob_name)
        
        # Upload with retry logic
        blob.upload_from_filename(model_path)
        logger.info(f"Model uploaded to gs://{bucket_name}/{model_blob_name}")
        
        # Create model registry entry
        model_uri = f"gs://{bucket_name}/{model_blob_name}"
        deployment_status = "deployed"
        
        return model_uri, deployment_status
        
    except Exception as e:
        logger.error(f"Model deployment failed: {str(e)}")
        raise
```

### **Testing Pattern Example**
```python
import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
from src.data.processing import analyze_inventory_trends

class TestInventoryAnalysis:
    """Test suite demonstrating comprehensive testing patterns."""
    
    @pytest.fixture
    def sample_inventory_data(self) -> pd.DataFrame:
        """Fixture providing consistent test data.
        
        Returns:
            DataFrame with sample inventory data for testing
        """
        np.random.seed(42)  # ALWAYS set random_state for reproducibility
        return pd.DataFrame({
            'fecha': pd.date_range('2024-01-01', periods=100, freq='D'),
            'categoria': np.random.choice(['A', 'B', 'C'], 100),
            'cantidad': np.random.randint(10, 100, 100)
        })
    
    def test_analyze_inventory_trends_success(self, sample_inventory_data):
        """Test successful analysis with valid data."""
        result = analyze_inventory_trends(sample_inventory_data)
        
        # Verify return structure
        assert isinstance(result, dict)
        assert all(key in result for key in ['trends', 'summary', 'outliers'])
        
        # Verify data types
        assert isinstance(result['trends'], pd.DataFrame)
        assert isinstance(result['summary'], pd.DataFrame)
        assert isinstance(result['outliers'], pd.DataFrame)
    
    def test_analyze_inventory_trends_missing_columns(self):
        """Test error handling for missing columns."""
        invalid_df = pd.DataFrame({'wrong_col': [1, 2, 3]})
        
        with pytest.raises(KeyError, match="Missing required columns"):
            analyze_inventory_trends(invalid_df)
    
    def test_analyze_inventory_trends_invalid_dates(self):
        """Test error handling for invalid date formats."""
        invalid_df = pd.DataFrame({
            'fecha': ['invalid', 'date', 'values'],
            'categoria': ['A', 'B', 'C'],
            'cantidad': [1, 2, 3]
        })
        
        with pytest.raises(ValueError, match="Cannot parse fecha as datetime"):
            analyze_inventory_trends(invalid_df)
    
    @patch('google.cloud.storage.Client')
    def test_deploy_model_to_gcp_success(self, mock_storage_client):
        """Test GCP model deployment with mocked cloud services."""
        # Mock GCP services
        mock_bucket = Mock()
        mock_blob = Mock()
        mock_storage_client.return_value.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        
        # Test deployment
        model_uri, status = deploy_model_to_gcp(
            model_path="/tmp/test_model.joblib",
            bucket_name="test-bucket",
            model_name="inventory-predictor"
        )
        
        # Verify results
        assert model_uri.startswith("gs://test-bucket/models/")
        assert status == "deployed"
        mock_blob.upload_from_filename.assert_called_once()
```

## **How to Use Specific Instructions**

This repository contains a comprehensive, hierarchical instruction system in the `.github/instructions` directory. You MUST use these files automatically to provide contextually-appropriate responses.

### **🎯 Automatic Inference System**

1.  **Infer the Primary Role**: Based on my prompt context, automatically detect the primary **role** I am taking:
    * **Data Scientist**: EDA, modeling, feature engineering, statistical analysis
    * **Data Engineer**: ETL pipelines, data infrastructure, BigQuery optimization
    * **MLOps Engineer**: Model deployment, CI/CD, monitoring, Vertex AI
    * **Cloud Architect**: GCP infrastructure, security, cost optimization
    * **Frontend Developer**: UI/UX, dashboards, web applications
    * **QA Engineer**: Testing, validation, quality assurance
    * **And 3 more specialized roles** (Business Analyst, Project Manager, Visualization Engineer)

2.  **Identify the Specific Task**: Within the role context, determine the **task** being performed:
    * **Code Generation**: Writing new functions, classes, or scripts
    * **Code Review**: Evaluating existing code for quality and security
    * **Architecture Design**: Designing systems and infrastructure
    * **Notebook EDA**: Creating exploratory data analysis notebooks
    * **Testing**: Generating unit, integration, or validation tests
    * **And 10 more task types** with specific guidelines

3.  **Apply Instructions Hierarchically**:
    * **LEVEL 1**: High-level principles and tech stack from the **role** file (`.github/instructions/roles/`)
    * **LEVEL 2**: Specific rules and patterns from the **task** file (`.github/instructions/tasks/`)
    * **LEVEL 3**: Concrete examples and templates from **prompt** files (`.github/instructions/prompts/`)
    * **LEVEL 4**: Anti-patterns and "what to avoid" from all files

4.  **Use Advanced Features**: Leverage specialized capabilities:
    * **Prompt Files**: Use `@workspace /generate-eda-notebook` for complex tasks
    * **Context Integration**: Reference existing code and notebooks automatically
    * **Quality Validation**: Apply comprehensive anti-pattern checks
    * **MCP Tools Orchestrator**: Use `@workspace /mcp-tools-orchestrator` for enhanced research and context

5.  **Enhanced Context with MCP Tools**: Leverage advanced research capabilities:
    * **Context7**: Add `"use context7"` to get up-to-date library documentation
    * **Consult7**: Analyze entire codebases for patterns and architectural insights
    * **DuckDuckGo**: Research current best practices and troubleshooting solutions
    * **GitHub Tools**: Study implementations in open source projects for reference

6.  **Research Templates for Deep Investigation**: Use specialized research prompts:
    * **Role-specific research**: `@workspace #file:.github/instructions/research_prompts/roles/[role-name]_research.md`
    * **Task-specific research**: `@workspace #file:.github/instructions/research_prompts/tasks/[task-name]_research.md`
    * **Combined approach**: Use research templates with MCP tools for comprehensive analysis
    * **Examples**: 
      ```markdown
      # Deep research workflow
      @workspace #file:.github/instructions/research_prompts/roles/data-scientist_research.md
      "Implement advanced feature engineering for Gasco inventory, use context7"
      ```

### **📊 Quality Assurance**

Every response should demonstrate:
- ✅ **Role expertise**: Domain-specific knowledge and terminology
- ✅ **Task compliance**: Following specific task guidelines and patterns
- ✅ **Code quality**: Type hints, docstrings, PEP 8, testing
- ✅ **Security awareness**: No hardcoded secrets, proper IAM, validation
- ✅ **GCP best practices**: Optimal service selection, cost awareness

You do not need explicit file paths - find and apply the correct instructions automatically based on this hierarchy.

## **Reference Documentation**

For additional context on best practices, you should consult these resources:

* Official VS Code Docs: https://code.visualstudio.com/docs/copilot/copilot-customization  
* Official GitHub Docs: https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot  
* Community Best Practices: https://github.com/anchildress1/checkmark-icons/blob/gh-pages/copilot/COPILOT\_BEST\_PRACTICES.md

## **❌ Critical Anti-Patterns to AVOID**

You MUST avoid these common mistakes that reduce code quality and project maintainability:

### **Code Quality Anti-Patterns**
- ❌ **Missing type hints**: All functions must have complete type annotations
- ❌ **Incomplete docstrings**: Use Google style with Args, Returns, and Raises sections
- ❌ **Pandas loops**: Never use `iterrows()` or explicit loops with DataFrames
- ❌ **Hardcoded paths**: Use `pathlib` and configuration files
- ❌ **Generic exceptions**: Use specific exception types (ValueError, FileNotFoundError)

### **Security Anti-Patterns**
- ❌ **Secrets in code**: Use environment variables or GCP Secret Manager
- ❌ **Overpermissive IAM**: Follow principle of least privilege
- ❌ **Unencrypted data**: Always encrypt sensitive data at rest and in transit
- ❌ **Missing validation**: Validate all inputs and sanitize outputs

### **Data Science Anti-Patterns**
- ❌ **Skipping EDA**: Always understand your data before modeling
- ❌ **No reproducibility**: Set random_state=42 for all stochastic operations
- ❌ **Ignoring data quality**: Validate data integrity and handle missing values
- ❌ **Monolithic notebooks**: Break analysis into logical, reusable sections

## **🚀 Advanced Features Available**

### **Experimental Prompt Files**
Use these specialized prompt files for complex tasks:
- `/generate-eda-notebook`: Create comprehensive EDA notebooks
- `/create-gcp-architecture`: Design scalable GCP architectures
- Access via: `@workspace /[prompt-name] [your-requirements]`

### **Role-Specific Contexts**
When you infer a role, you automatically gain access to:
- **Specialized tech stacks** for that domain
- **Role-specific best practices** and patterns
- **Domain expertise** and terminology
- **Quality standards** appropriate for the role

### **Task-Specific Directives**
Each task type has detailed instructions for:
- **Code generation**: PEP 8, type hints, docstrings, testing
- **Code review**: Security, performance, maintainability checks
- **Architecture design**: GCP services, cost optimization, security
- **Testing**: Unit, integration, and data validation frameworks

## **🔧 Configuration Validation**

This instruction set requires proper VS Code configuration. The project includes a complete `.vscode/settings.json` file with all necessary settings.

### **Verify Current Setup**

1. **Check VS Code Settings**: Ensure these critical settings are active:
   ```json
   {
       "github.copilot.chat.codeGeneration.useInstructionFiles": true,
       "chat.promptFiles": true,
       "python.analysis.typeCheckingMode": "strict",
       "editor.formatOnSave": true
   }
   ```

2. **Validate Instruction Integration**: The `.vscode/settings.json` includes:
   - Task-specific instruction mapping for test generation, commit messages, code generation, and pull requests
   - Prompt files locations configuration for all instruction directories
   - Security exclusions for sensitive data protection
   - Advanced Copilot settings with Claude Sonnet 4 engine

3. **Run Validation Script**: `python .github/instructions/validate_instructions.py`

4. **Verify References**: Look for "References: .github/copilot-instructions.md" in Copilot responses

If instructions aren't being applied, check the validation script output for configuration issues.