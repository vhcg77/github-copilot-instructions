---
title: "Enhanced Data Science Analysis"
description: "Comprehensive data analysis using MCP tools for enhanced context and methodology"
mode: "agent"
tools: ["context7", "consult7", "duckduckgo", "github", "pandas", "plotly", "scikit-learn"]
role: "data-scientist"
priority: "high"
---

# Enhanced Data Science Analysis

## Objective
Perform comprehensive data science analysis leveraging MCP tools for current methodologies, pattern analysis, and enhanced decision-making.

## Enhanced Analysis Workflow

### Phase 1: Research and Context Gathering
```
1. Library Documentation Research:
   "pandas data manipulation and analysis patterns, use context7"
   "scikit-learn model selection and evaluation, use context7"
   "plotly interactive visualization techniques, use context7"

2. Existing Analysis Pattern Review:
   Use Consult7 to analyze current notebooks in /notebooks/ directory
   Identify established EDA patterns and modeling approaches
   Review feature engineering techniques used in the project

3. Methodology Research:
   Use DuckDuckGo: "data science best practices inventory analysis 2025"
   Use DuckDuckGo: "feature engineering techniques supply chain analytics"

4. Reference Implementations:
   Use GitHub Tools: Find similar inventory analysis projects
   Study data science workflows in comparable business domains
```

### Phase 2: Enhanced Data Analysis Implementation

## Example MCP-Enhanced Analysis Request

```
"Perform comprehensive analysis of Gasco inventory dataset that includes:

1. Advanced data quality assessment with statistical validation
2. Business-focused exploratory data analysis for inventory optimization
3. Feature engineering for inventory forecasting models
4. Statistical analysis of inventory patterns and trends
5. Interactive visualizations for stakeholder presentation
6. Model development for inventory level prediction

Enhanced Research:
- use context7 for pandas, plotly, and scikit-learn latest patterns
- Use consult7 to analyze existing analysis patterns in /notebooks/
- Search with duckduckgo: 'inventory optimization data science techniques 2025'
- Find reference implementations in GitHub for supply chain analytics"
```

## Expected Output Structure

### 1. Enhanced Data Loading and Validation
```python
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from typing import Dict, List, Tuple, Optional
import logging
from pathlib import Path

# Setup logging for analysis tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_and_validate_inventory_data(
    file_path: str, 
    expected_columns: List[str]
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Load inventory data with comprehensive validation.
    
    Enhanced with Context7 research on pandas best practices for data loading
    and validation patterns.
    
    Args:
        file_path: Path to the inventory CSV file
        expected_columns: List of required columns
        
    Returns:
        Tuple of (cleaned_dataframe, validation_report)
        
    Raises:
        FileNotFoundError: If the data file doesn't exist
        ValueError: If required columns are missing
    """
    try:
        # Load data with optimized dtypes (Context7 best practice)
        df = pd.read_csv(file_path, parse_dates=['updated_at'], low_memory=False)
        logger.info(f"Loaded data: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # Validate required columns
        missing_cols = set(expected_columns) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Advanced data quality assessment
        validation_report = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'missing_values': df.isnull().sum().to_dict(),
            'duplicate_rows': df.duplicated().sum(),
            'data_types': df.dtypes.to_dict(),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2
        }
        
        logger.info(f"Data validation completed: {validation_report}")
        return df, validation_report
        
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise
```

### 2. Business-Focused Exploratory Data Analysis
```python
def perform_enhanced_inventory_eda(
    df: pd.DataFrame
) -> Dict[str, go.Figure]:
    """Comprehensive EDA focused on inventory business insights.
    
    Enhanced with Consult7 analysis of existing EDA patterns and
    DuckDuckGo research on inventory analysis best practices.
    
    Args:
        df: Inventory DataFrame
        
    Returns:
        Dictionary of Plotly figures for interactive analysis
    """
    figures = {}
    
    # 1. Inventory Distribution Analysis
    fig_distribution = make_subplots(
        rows=2, cols=2,
        subplot_titles=['Quantity Distribution', 'Location Analysis', 
                       'Temporal Patterns', 'Product Categories'],
        specs=[[{"secondary_y": False}, {"type": "bar"}],
               [{"type": "scatter"}, {"type": "pie"}]]
    )
    
    # Enhanced histogram with statistical overlays
    fig_distribution.add_trace(
        go.Histogram(
            x=df['quantity'],
            nbinsx=50,
            name='Quantity Distribution',
            marker_color='lightblue'
        ),
        row=1, col=1
    )
    
    # Add statistical markers (Context7 research: latest plotly features)
    mean_qty = df['quantity'].mean()
    median_qty = df['quantity'].median()
    
    fig_distribution.add_vline(
        x=mean_qty, 
        line_dash="dash", 
        line_color="red",
        annotation_text=f"Mean: {mean_qty:.1f}",
        row=1, col=1
    )
    
    # 2. Location-based Analysis
    location_summary = df.groupby('location').agg({
        'quantity': ['sum', 'mean', 'count'],
        'product_id': 'nunique'
    }).round(2)
    
    fig_distribution.add_trace(
        go.Bar(
            x=location_summary.index,
            y=location_summary[('quantity', 'sum')],
            name='Total Inventory by Location',
            marker_color='green'
        ),
        row=1, col=2
    )
    
    figures['distribution_analysis'] = fig_distribution
    
    # 3. Advanced Correlation Analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 1:
        correlation_matrix = df[numeric_cols].corr()
        
        fig_corr = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale='RdBu',
            zmid=0
        ))
        
        fig_corr.update_layout(
            title='Feature Correlation Matrix',
            height=500,
            width=500
        )
        
        figures['correlation_analysis'] = fig_corr
    
    return figures
```

### 3. Advanced Feature Engineering
```python
def create_advanced_inventory_features(
    df: pd.DataFrame
) -> pd.DataFrame:
    """Create advanced features for inventory analysis and modeling.
    
    Enhanced with GitHub research on feature engineering patterns
    and DuckDuckGo research on inventory forecasting techniques.
    
    Args:
        df: Base inventory DataFrame
        
    Returns:
        DataFrame with engineered features
    """
    df_enhanced = df.copy()
    
    # Temporal features (enhanced with Context7 pandas datetime research)
    df_enhanced['year'] = df_enhanced['updated_at'].dt.year
    df_enhanced['month'] = df_enhanced['updated_at'].dt.month
    df_enhanced['day_of_week'] = df_enhanced['updated_at'].dt.dayofweek
    df_enhanced['is_weekend'] = df_enhanced['day_of_week'].isin([5, 6]).astype(int)
    df_enhanced['quarter'] = df_enhanced['updated_at'].dt.quarter
    
    # Inventory level categorization (business insight from DuckDuckGo research)
    df_enhanced['inventory_level'] = pd.cut(
        df_enhanced['quantity'], 
        bins=[0, 50, 100, 200, float('inf')], 
        labels=['Low', 'Medium', 'High', 'Excess']
    )
    
    # Location-based features (pattern from Consult7 analysis)
    location_stats = df.groupby('location')['quantity'].agg(['mean', 'std']).add_prefix('location_')
    df_enhanced = df_enhanced.merge(
        location_stats, 
        left_on='location', 
        right_index=True, 
        how='left'
    )
    
    # Product category features (if product_id follows pattern)
    df_enhanced['product_category'] = df_enhanced['product_id'].str[:2]
    df_enhanced['product_number'] = df_enhanced['product_id'].str[2:].astype(int)
    
    # Anomaly detection features
    df_enhanced['quantity_zscore'] = np.abs(
        (df_enhanced['quantity'] - df_enhanced['quantity'].mean()) / df_enhanced['quantity'].std()
    )
    df_enhanced['is_outlier'] = (df_enhanced['quantity_zscore'] > 3).astype(int)
    
    logger.info(f"Created {len(df_enhanced.columns) - len(df.columns)} new features")
    return df_enhanced
```

### 4. Statistical Analysis and Insights
```python
def perform_statistical_analysis(
    df: pd.DataFrame
) -> Dict[str, Any]:
    """Comprehensive statistical analysis for business insights.
    
    Enhanced with scikit-learn statistical methods and business intelligence
    patterns from DuckDuckGo research.
    
    Args:
        df: Enhanced inventory DataFrame
        
    Returns:
        Dictionary containing statistical insights and recommendations
    """
    insights = {}
    
    # Descriptive statistics by category
    insights['location_analysis'] = df.groupby('location').agg({
        'quantity': ['count', 'mean', 'std', 'min', 'max'],
        'product_id': 'nunique'
    }).round(2)
    
    # Inventory level distribution
    insights['inventory_distribution'] = df['inventory_level'].value_counts(normalize=True)
    
    # Outlier analysis
    outlier_summary = df[df['is_outlier'] == 1].groupby('location').size()
    insights['outlier_analysis'] = {
        'total_outliers': df['is_outlier'].sum(),
        'outlier_percentage': (df['is_outlier'].mean() * 100).round(2),
        'outliers_by_location': outlier_summary.to_dict()
    }
    
    # Business recommendations based on analysis
    insights['recommendations'] = {
        'restock_alerts': df[df['inventory_level'] == 'Low']['location'].value_counts().to_dict(),
        'excess_inventory': df[df['inventory_level'] == 'Excess']['location'].value_counts().to_dict(),
        'optimization_opportunities': {
            'high_variance_locations': df.groupby('location')['quantity'].std().nlargest(3).index.tolist(),
            'low_diversity_locations': insights['location_analysis'][('product_id', 'nunique')].nsmallest(3).index.tolist()
        }
    }
    
    return insights
```

### 5. Predictive Modeling
```python
def build_inventory_prediction_model(
    df: pd.DataFrame,
    target_column: str = 'quantity'
) -> Dict[str, Any]:
    """Build predictive model for inventory forecasting.
    
    Enhanced with scikit-learn latest patterns from Context7 and
    modeling techniques from GitHub research.
    
    Args:
        df: Enhanced DataFrame with features
        target_column: Column to predict
        
    Returns:
        Dictionary containing model results and evaluation
    """
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    
    # Prepare features (enhanced preprocessing)
    feature_columns = [
        'month', 'day_of_week', 'is_weekend', 'quarter',
        'location_mean', 'location_std', 'product_number'
    ]
    
    # Encode categorical variables
    df_model = df.copy()
    le_location = LabelEncoder()
    df_model['location_encoded'] = le_location.fit_transform(df_model['location'])
    feature_columns.append('location_encoded')
    
    # Prepare data
    X = df_model[feature_columns].fillna(0)
    y = df_model[target_column]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model (enhanced with Context7 hyperparameter research)
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Evaluate model
    train_pred = model.predict(X_train_scaled)
    test_pred = model.predict(X_test_scaled)
    
    results = {
        'train_mae': mean_absolute_error(y_train, train_pred),
        'test_mae': mean_absolute_error(y_test, test_pred),
        'train_r2': r2_score(y_train, train_pred),
        'test_r2': r2_score(y_test, test_pred),
        'feature_importance': dict(zip(feature_columns, model.feature_importances_)),
        'cross_val_scores': cross_val_score(model, X_train_scaled, y_train, cv=5)
    }
    
    return {
        'model': model,
        'scaler': scaler,
        'results': results,
        'feature_columns': feature_columns
    }
```

## Quality Validation Checklist

### ✅ Analysis Completeness
- [ ] Data quality assessment completed
- [ ] Business-focused EDA performed
- [ ] Advanced feature engineering implemented
- [ ] Statistical analysis with actionable insights
- [ ] Predictive modeling with proper validation
- [ ] Interactive visualizations created

### ✅ Code Quality Standards
- [ ] Type hints for all functions
- [ ] Google-style docstrings with business context
- [ ] Proper error handling and logging
- [ ] Vectorized operations used throughout
- [ ] Reproducible analysis (random_state=42)

### ✅ MCP Tool Integration Verification
- [ ] Context7 provided current pandas/scikit-learn patterns
- [ ] Consult7 analyzed existing notebook patterns for consistency
- [ ] DuckDuckGo research informed analysis methodology
- [ ] GitHub references provided implementation examples

## Usage Example

```python
# Complete enhanced analysis workflow
file_path = "data/output/inventario_recursos_gasco_2025_06_25.csv"
required_columns = ['product_id', 'quantity', 'location', 'updated_at']

# Load and validate data
df, validation_report = load_and_validate_inventory_data(file_path, required_columns)

# Perform EDA
eda_figures = perform_enhanced_inventory_eda(df)

# Feature engineering
df_enhanced = create_advanced_inventory_features(df)

# Statistical analysis
insights = perform_statistical_analysis(df_enhanced)

# Predictive modeling
model_results = build_inventory_prediction_model(df_enhanced)

# Display results
print("=== INVENTORY ANALYSIS INSIGHTS ===")
for key, value in insights['recommendations'].items():
    print(f"{key}: {value}")
```

---

**Note**: This enhanced analysis leverages MCP tools to ensure current best practices, analyze existing patterns, and implement proven methodologies from the data science community.
