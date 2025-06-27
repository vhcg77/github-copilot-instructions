---
applyTo: ["code", "generation", "scripting"]
description: "Instructions for generating new code"
priority: "high"
---

# Task: Python Code Generation

When I ask you to write a Python function, class, or script, you MUST adhere to the following rules.

## Pre-Generation Research Phase

Before generating code, leverage MCP tools for comprehensive context:

1. **Context7 Research**: Use `"use context7"` to get current documentation for relevant libraries
   * Example: `"Creating pandas DataFrame validation, use context7"`
   * Ensures you're using latest APIs and best practices

2. **Existing Patterns Analysis**: Use Consult7 to analyze similar implementations in the codebase
   * Review `/src/` directory for existing patterns and conventions
   * Identify reusable utilities and established architectural patterns

3. **Best Practices Research**: Use DuckDuckGo for current development practices
   * Search for latest patterns specific to your use case
   * Example: "Python data validation patterns 2025"

4. **Reference Implementations**: Use GitHub tools to study similar implementations
   * Find examples of production-ready code for your specific requirements
   * Analyze documentation and testing patterns

## Code Generation Rules

## Rules
1.  **PEP 8 Compliance**: All code must be formatted according to the PEP 8 style guide.
2.  **Type Hinting is Mandatory**: Use Python's `typing` module to add type hints for all function arguments, variables, and return values.
3.  **Docstrings are Mandatory**: Every function, method, and class must have a docstring written in the Google Python Style Guide format.
    ```python
    def example_function(arg1: int, arg2: str) -> bool:
        """This is a summary of the function.

        This is a more detailed description of what the function does
        and how it does it.

        Args:
            arg1 (int): A description of the first argument.
            arg2 (str): A description of the second argument.

        Returns:
            bool: A description of the return value.

        Raises:
            ValueError: If arg1 is negative.
        """
        if arg1 < 0:
            raise ValueError("arg1 cannot be negative")
        return len(arg2) > arg1
    ```
4.  **Modularity**: Write small, single-responsibility functions. If a function is becoming too long or complex, break it down into smaller helper functions.
5.  **Error Handling**: Use try-except blocks to handle potential exceptions gracefully. Raise specific, informative exceptions (e.g., `ValueError`, `FileNotFoundError`) instead of generic ones.
6.  **Efficiency**: Use vectorized operations with `numpy` and `pandas` instead of loops whenever possible.

## ❌ **Code Generation Anti-Patterns**

### **Type Hinting Violations**
```python
# ❌ DON'T: Missing type hints
def process_data(data, columns):
    return data[columns].dropna()

# ✅ DO: Complete type hints
def process_data(data: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Process data by selecting columns and removing missing values."""
    return data[columns].dropna()
```

### **Docstring Violations**
```python
# ❌ DON'T: Missing or incomplete docstrings
def calculate_metrics(df, col):
    return df[col].mean(), df[col].std()

# ✅ DO: Complete Google-style docstrings
def calculate_metrics(df: pd.DataFrame, col: str) -> Tuple[float, float]:
    """Calculate mean and standard deviation for a column.
    
    Args:
        df: Input DataFrame containing the data.
        col: Name of the column to calculate metrics for.
        
    Returns:
        Tuple of (mean, standard_deviation) for the specified column.
        
    Raises:
        KeyError: If the specified column doesn't exist in the DataFrame.
    """
    if col not in df.columns:
        raise KeyError(f"Column '{col}' not found in DataFrame")
    return df[col].mean(), df[col].std()
```

### **Performance Anti-Patterns**
```python
# ❌ DON'T: Use loops with pandas DataFrames
def apply_discount(df: pd.DataFrame) -> pd.DataFrame:
    for i in range(len(df)):
        if df.iloc[i]['amount'] > 100:
            df.iloc[i, df.columns.get_loc('final_amount')] = df.iloc[i]['amount'] * 0.9
    return df

# ✅ DO: Use vectorized operations
def apply_discount(df: pd.DataFrame) -> pd.DataFrame:
    """Apply 10% discount to orders over $100."""
    df['final_amount'] = np.where(df['amount'] > 100, df['amount'] * 0.9, df['amount'])
    return df
```

### **Error Handling Anti-Patterns**
```python
# ❌ DON'T: Generic exception handling
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except:
        return None

# ✅ DO: Specific exception handling with logging
def load_data(file_path: str) -> pd.DataFrame:
    """Load data from CSV file with proper error handling."""
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found: {file_path}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"Data file is empty: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Failed to load data from {file_path}: {str(e)}")
```

### **Common Mistakes to Avoid**
- ❌ **Don't hardcode file paths**: Use config files or environment variables
- ❌ **Don't ignore data validation**: Always validate inputs and outputs
- ❌ **Don't use mutable default arguments**: Use `None` and create inside function
- ❌ **Don't mix business logic with I/O**: Separate data loading from processing
- ❌ **Don't skip unit tests**: Every function in `/src/` needs tests
- ❌ **Don't use global variables**: Pass dependencies explicitly

## **Specific Code Patterns to Follow**

### **Data Processing Functions**
```python
def clean_and_validate_data(
    df: pd.DataFrame, 
    required_columns: List[str],
    numeric_columns: Optional[List[str]] = None,
    date_columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """Clean and validate input DataFrame according to data quality standards.
    
    Args:
        df: Raw input DataFrame
        required_columns: Columns that must be present
        numeric_columns: Columns that should be numeric (will be converted)
        date_columns: Columns that should be datetime (will be parsed)
        
    Returns:
        Cleaned and validated DataFrame
        
    Raises:
        ValueError: If required columns are missing or data types are invalid
    """
    # Validation: Check required columns exist
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Create a copy to avoid modifying original
    df_clean = df.copy()
    
    # Convert numeric columns with error handling
    if numeric_columns:
        for col in numeric_columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    # Parse date columns with error handling
    if date_columns:
        for col in date_columns:
            df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
    
    # Log data quality metrics
    logger.info(f"Data cleaning completed: {len(df_clean)} rows processed")
    
    return df_clean
```

### **Analysis Functions with Proper Error Handling**
```python
def calculate_summary_statistics(
    df: pd.DataFrame, 
    group_by: str,
    value_column: str,
    aggregations: List[str] = ['mean', 'median', 'std']
) -> pd.DataFrame:
    """Calculate summary statistics grouped by a categorical variable.
    
    Args:
        df: Input DataFrame
        group_by: Column name to group by
        value_column: Numeric column to calculate statistics for
        aggregations: List of aggregation functions to apply
        
    Returns:
        DataFrame with summary statistics
        
    Raises:
        ValueError: If columns don't exist or value_column is not numeric
    """
    # Input validation
    if group_by not in df.columns:
        raise ValueError(f"Group column '{group_by}' not found")
    if value_column not in df.columns:
        raise ValueError(f"Value column '{value_column}' not found")
    if not pd.api.types.is_numeric_dtype(df[value_column]):
        raise ValueError(f"Column '{value_column}' must be numeric")
    
    # Vectorized aggregation
    summary = df.groupby(group_by)[value_column].agg(aggregations).round(2)
    
    # Add row count for context
    summary['count'] = df.groupby(group_by)[value_column].count()
    
    return summary.reset_index()
```

### **Visualization Functions with Consistent Styling**
```python
def create_distribution_plot(
    df: pd.DataFrame,
    column: str,
    title: Optional[str] = None,
    bins: int = 30,
    show_stats: bool = True
) -> go.Figure:
    """Create standardized distribution plot with statistics overlay.
    
    Args:
        df: Input DataFrame
        column: Column name to plot
        title: Plot title (auto-generated if None)
        bins: Number of histogram bins
        show_stats: Whether to show mean/median lines
        
    Returns:
        Plotly Figure object ready for display
    """
    # Validation
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    # Auto-generate title if not provided
    if title is None:
        title = f"Distribution of {column.replace('_', ' ').title()}"
    
    # Create histogram
    fig = px.histogram(
        df,
        x=column,
        nbins=bins,
        title=title,
        template='plotly_white',
        color_discrete_sequence=['#2E86AB']
    )
    
    # Add statistics if requested
    if show_stats:
        mean_val = df[column].mean()
        median_val = df[column].median()
        
        fig.add_vline(
            x=mean_val, 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"Mean: {mean_val:.2f}"
        )
        fig.add_vline(
            x=median_val, 
            line_dash="dot", 
            line_color="green",
            annotation_text=f"Median: {median_val:.2f}"
        )
    
    # Consistent styling
    fig.update_layout(
        height=400,
        xaxis_title_font_size=12,
        yaxis_title_font_size=12,
        showlegend=False
    )
    
    return fig
```

## **Context Management Best Practices**

### **Before Writing Code**
1. **Open Related Files**: Have relevant modules, configs, and data files open in VS Code
2. **Review Existing Patterns**: Check similar functions in the codebase for consistency
3. **Understand Dependencies**: Review imports and available utilities in the project

### **File Organization Patterns**
```python
# Standard file structure for data processing modules
"""
src/
├── data/
│   ├── __init__.py
│   ├── loading.py      # Data loading functions
│   ├── cleaning.py     # Data cleaning and validation
│   ├── validation.py   # Data quality checks
│   └── transforms.py   # Data transformations
├── analysis/
│   ├── __init__.py
│   ├── descriptive.py  # Summary statistics
│   ├── visualization.py # Plotting functions
│   └── modeling.py     # ML model utilities
└── utils/
    ├── __init__.py
    ├── config.py       # Configuration management
    ├── logging.py      # Logging utilities
    └── helpers.py      # General utility functions
"""
```

### **Import Organization**
```python
# Standard import order and aliases
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Local imports
from src.utils.config import get_config
from src.utils.logging import setup_logger

# Setup
logger = setup_logger(__name__)
config = get_config()
```

## 🔬 Research Templates

For specialized investigation of this task, use:
`@workspace #file:.github/instructions/research_prompts/tasks/code-generation_research.md`

This template provides:
- 📋 **Best practices** for code generation
- 🚫 **Anti-patterns** that reduce effectiveness
- 🚀 **Optimization recommendations** for better code
- 💼 **Context-specific guidance** for GCP applications

### Usage with MCP Tools

Combine research prompts with MCP tools for enhanced code generation:

```markdown
# Complete code generation research
@workspace #file:.github/instructions/research_prompts/tasks/code-generation_research.md

"Generate data validation function for Gasco inventory, use context7"
```

### Automatic Application
- When **generating Python code** → Research template applied
- When using **MCP tools** → Best practices context included
- When working with **data science** → Specialized patterns followed
