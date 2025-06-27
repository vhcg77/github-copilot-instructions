---
title: "Generate Comprehensive EDA Notebook"
description: "Create a complete exploratory data analysis notebook for a dataset"
mode: "agent"
tools: ["python", "pandas", "plotly", "seaborn", "jupyter"]
role: "data-scientist"
priority: "high"
---

# Generate Comprehensive EDA Notebook

## Objective
Create a comprehensive Jupyter notebook for exploratory data analysis following our established standards and best practices.

## Context
You are a Senior Data Scientist working on a GCP-based data project. The notebook should be production-ready, well-documented, and follow our coding standards.

## Requirements

### 1. Notebook Structure
- Clear title with business objective
- Table of contents with anchor links
- Import statements with proper configuration
- Data loading with error handling
- Step-by-step analysis sections

### 2. Analysis Components
- **Data Quality Assessment**: Missing values, duplicates, data types
- **Descriptive Statistics**: Summary stats for numerical and categorical variables
- **Distribution Analysis**: Histograms, box plots, violin plots
- **Correlation Analysis**: Correlation matrix and pair plots
- **Business Insights**: Key findings and recommendations

### 3. Visualization Standards
- Use Plotly for interactive visualizations
- Consistent color palette and styling
- Proper titles, labels, and legends
- Mobile-responsive layouts

### 4. Code Quality
- Type hints for all functions
- Google-style docstrings
- Error handling and validation
- Vectorized operations (no pandas loops)
- Set `random_state=42` for reproducibility

## Code Patterns and Examples

### Required Function Structure
```python
def analyze_data_quality(df: pd.DataFrame, columns: List[str]) -> Dict[str, Any]:
    """Analyze data quality metrics for specified columns.
    
    Args:
        df: Input DataFrame to analyze
        columns: List of column names to check
        
    Returns:
        Dictionary with data quality metrics including:
        - missing_percentage: Percentage of missing values per column
        - duplicate_count: Number of duplicate rows
        - outlier_counts: Number of outliers per numeric column
        
    Raises:
        ValueError: If specified columns don't exist in DataFrame
    """
    if not all(col in df.columns for col in columns):
        missing_cols = set(columns) - set(df.columns)
        raise ValueError(f"Columns not found: {missing_cols}")
    
    # Use vectorized operations - never loops
    quality_metrics = {
        'missing_percentage': (df[columns].isnull().sum() / len(df) * 100).to_dict(),
        'duplicate_count': df.duplicated().sum(),
        'total_rows': len(df)
    }
    
    return quality_metrics
```

### Visualization Standards
```python
# Interactive plots with consistent styling
fig = px.histogram(
    df, 
    x='column_name',
    title='Distribution of Column Name',
    labels={'column_name': 'Descriptive Label (Units)'},
    template='plotly_white',
    color_discrete_sequence=['#2E86AB']  # Consistent color palette
)
fig.update_layout(
    height=400,
    showlegend=False,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14
)
fig.show()
```

### Context Management Instructions
Before generating the notebook:
1. Have the dataset file open in VS Code for context
2. Open any existing analysis notebooks for reference patterns
3. Check for config files that might contain data schema information
4. Review the data dictionary or README if available

## Expected Output Format

```python
# Standard imports and configuration
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Configuration
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
```

## Prompt Instructions

**Context Setup**: Before using this prompt, ensure you have:
- The target dataset file open in VS Code
- Any existing notebooks or analysis files open for pattern reference
- Data documentation (README, schema files) accessible

**Specific Requirements to Ask**:
1. **Dataset Details**: 
   - File path and format
   - Expected number of rows/columns
   - Key business questions to answer
   
2. **Analysis Scope**:
   - Target variables for analysis
   - Specific relationships to explore
   - Business context and constraints
   
3. **Output Requirements**:
   - Stakeholder audience (technical vs business)
   - Specific visualizations needed
   - Analysis depth (exploratory vs deep-dive)

**Generate Response Pattern**:
```markdown
I'll create a comprehensive EDA notebook following our standards. 

First, let me understand your specific requirements:
- What dataset are we analyzing? (provide file path)
- What are the main business questions you want to answer?
- Are there specific variables or relationships of interest?
- Who is the target audience for this analysis?

Based on your responses, I'll generate a structured notebook with:
1. Data loading with proper error handling
2. Quality assessment with specific metrics
3. Targeted visualizations for your use case
4. Business-focused insights and recommendations
```

Then generate the complete notebook following the above standards and code patterns.
