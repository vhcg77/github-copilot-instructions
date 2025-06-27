---
applyTo: ["eda", "notebook", "analysis", "exploration"]
description: "Instructions for Exploratory Data Analysis in Jupyter notebooks"
priority: "high"
---

# **Task: Exploratory Data Analysis (EDA) in Notebooks**

When performing EDA in Jupyter notebooks, follow these structured guidelines to ensure comprehensive and reproducible analysis.

## **Notebook Structure**

### **1. Header and Introduction**
- Clear title with date and objective
- Table of contents with anchor links
- Dataset description and context
- Business questions to be answered

### **2. Data Loading and Initial Inspection**
- Import necessary libraries with proper configuration
- Load dataset with error handling
- Display basic info: shape, memory usage, column types
- Show first/last few rows

### **3. Data Quality Assessment**
- Missing values analysis (count and percentage)
- Duplicate detection and handling
- Data type validation and correction
- Basic statistics for numerical and categorical variables

### **4. Descriptive Analysis**
- Summary statistics for numerical variables
- Value counts for categorical variables
- Distribution analysis with visualizations
- Correlation analysis between variables

### **5. Visual Exploration**
- Histograms and box plots for distributions
- Bar charts for categorical data
- Correlation heatmaps
- Geographic analysis if applicable

### **6. Insights and Patterns**
- Identify trends and patterns
- Highlight anomalies or outliers
- Document business-relevant findings
- Statistical significance testing when appropriate

## **Code Standards for EDA Notebooks**

```python
# Required imports at the top
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import warnings
from typing import Tuple, List, Dict

# Standard configuration
warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('viridis')
plt.rcParams['figure.figsize'] = (12, 8)
pd.set_option('display.max_columns', None)

# Set random seed for reproducibility
np.random.seed(42)
```

## **Visualization Guidelines**

1. **Every plot must have**:
   - Clear title describing what it shows
   - Labeled axes with units when applicable
   - Legends when multiple series are shown
   - Appropriate color scheme (accessible)

2. **Use consistent styling**:
   - Same color palette throughout the notebook
   - Consistent figure sizes
   - Professional formatting

3. **Interactive plots** (with Plotly) for:
   - Large datasets requiring filtering
   - Geographic data
   - Time series with zoom capabilities

## **Documentation Requirements**

- **Markdown cells** before each analysis section explaining the purpose
- **Comments** in code explaining complex logic
- **Conclusions** after each major analysis with bullet points
- **Summary section** at the end with key findings and recommendations

## **File Naming Convention**

- `eda_descriptive_[dataset_name]_[date].ipynb`
- `eda_diagnostic_[dataset_name]_[date].ipynb`
- `eda_inferential_[dataset_name]_[date].ipynb`
- `eda_prescriptive_[dataset_name]_[date].ipynb`

## **EDA Types: Specific Instructions**

### **1. Descriptive EDA (`eda_descriptive_*`)**
**Purpose**: Basic data understanding and summarization

**Required Sections**:
- Data overview (shape, types, memory usage)
- Univariate analysis (distributions, central tendency)
- Summary statistics (mean, median, mode, std)
- Missing values analysis
- Basic visualizations (histograms, bar charts)

**Example Structure**:
<VSCode.Cell language="markdown">
# Descriptive EDA: [Dataset Name]
## Objective
Understand the basic characteristics and structure of the dataset.
</VSCode.Cell>

<VSCode.Cell language="python">
# 1. Data Overview
print("Dataset Shape:", df.shape)
print("\nColumn Types:")
print(df.dtypes)
print("\nMemory Usage:")
print(df.memory_usage(deep=True).sum() / 1024**2, "MB")
</VSCode.Cell>

<VSCode.Cell language="python">
# 2. Summary Statistics
df.describe(include='all')
</VSCode.Cell>

### **2. Diagnostic EDA (`eda_diagnostic_*`)**
**Purpose**: Identify data quality issues and anomalies

**Required Sections**:
- Data quality assessment (missing, duplicates, outliers)
- Anomaly detection and investigation
- Data consistency checks
- Validation against business rules
- Data profiling reports

**Example Structure**:
<VSCode.Cell language="markdown">
# Diagnostic EDA: [Dataset Name]
## Objective
Identify and diagnose data quality issues, outliers, and inconsistencies.
</VSCode.Cell>

<VSCode.Cell language="python">
# 1. Missing Values Analysis
missing_analysis = pd.DataFrame({
    'Column': df.columns,
    'Missing_Count': df.isnull().sum(),
    'Missing_Percentage': (df.isnull().sum() / len(df)) * 100
})
missing_analysis[missing_analysis['Missing_Count'] > 0].sort_values('Missing_Percentage', ascending=False)
</VSCode.Cell>

<VSCode.Cell language="python">
# 2. Outlier Detection
from scipy import stats
import numpy as np

def detect_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] < lower_bound) | (df[column] > upper_bound)]

# Apply to numerical columns
for col in df.select_dtypes(include=[np.number]).columns:
    outliers = detect_outliers_iqr(df, col)
    print(f"{col}: {len(outliers)} outliers ({len(outliers)/len(df)*100:.2f}%)")
</VSCode.Cell>

### **3. Inferential EDA (`eda_inferential_*`)**
**Purpose**: Statistical inference and hypothesis testing

**Required Sections**:
- Correlation analysis and significance testing
- Hypothesis formulation and testing
- Statistical relationships between variables
- Confidence intervals and p-values
- Causal inference exploration

**Example Structure**:
<VSCode.Cell language="markdown">
# Inferential EDA: [Dataset Name]
## Objective
Explore statistical relationships and test hypotheses about the data.
</VSCode.Cell>

<VSCode.Cell language="python">
# 1. Correlation Analysis with Significance Testing
from scipy.stats import pearsonr, spearmanr
import seaborn as sns

# Correlation matrix
correlation_matrix = df.select_dtypes(include=[np.number]).corr()

# Plot correlation heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
            square=True, fmt='.2f')
plt.title('Correlation Matrix')
plt.show()
</VSCode.Cell>

<VSCode.Cell language="python">
# 2. Statistical Hypothesis Testing
from scipy.stats import ttest_ind, chi2_contingency

# Example: T-test for comparing groups
def compare_groups(df, group_col, value_col):
    groups = df[group_col].unique()
    if len(groups) == 2:
        group1 = df[df[group_col] == groups[0]][value_col]
        group2 = df[df[group_col] == groups[1]][value_col]
        t_stat, p_value = ttest_ind(group1, group2)
        print(f"T-test between {groups[0]} and {groups[1]}:")
        print(f"T-statistic: {t_stat:.4f}, P-value: {p_value:.4f}")
        print(f"Significant difference: {'Yes' if p_value < 0.05 else 'No'}")

# Apply to relevant columns
# compare_groups(df, 'category_column', 'numeric_column')
</VSCode.Cell>

### **4. Prescriptive EDA (`eda_prescriptive_*`)**
**Purpose**: Actionable insights and recommendations

**Required Sections**:
- Business impact analysis
- Actionable insights extraction
- Recommendations for data improvement
- Strategic conclusions for decision-making
- Next steps and modeling preparation

**Example Structure**:
<VSCode.Cell language="markdown">
# Prescriptive EDA: [Dataset Name]
## Objective
Generate actionable insights and recommendations for business decisions and next steps.
</VSCode.Cell>

<VSCode.Cell language="markdown">
## Key Business Questions to Address
1. What are the main drivers of [target variable]?
2. Which segments show the highest potential?
3. What data quality improvements are needed?
4. What features should be prioritized for modeling?
5. What business actions are recommended?
</VSCode.Cell>

<VSCode.Cell language="python">
# 1. Feature Importance Analysis
def calculate_feature_importance(df, target_column):
    """Calculate correlation-based feature importance"""
    numerical_features = df.select_dtypes(include=[np.number]).columns
    feature_importance = {}
    
    for feature in numerical_features:
        if feature != target_column:
            correlation = df[feature].corr(df[target_column])
            feature_importance[feature] = abs(correlation)
    
    # Sort by importance
    sorted_features = sorted(feature_importance.items(), 
                           key=lambda x: x[1], reverse=True)
    
    print("Feature Importance (based on correlation):")
    for feature, importance in sorted_features[:10]:
        print(f"{feature}: {importance:.3f}")
    
    return sorted_features

# Apply if target variable exists
# feature_ranking = calculate_feature_importance(df, 'target_column')
</VSCode.Cell>

<VSCode.Cell language="markdown">
## Business Recommendations

### Data Quality Improvements
- [Specific recommendations based on diagnostic analysis]
- [Data collection improvements]
- [Data processing recommendations]

### Strategic Insights
- [Key business insights discovered]
- [Market opportunities identified]
- [Risk factors to monitor]

### Next Steps
- [Modeling approach recommendations]
- [Additional data needs]
- [Business process improvements]
</VSCode.Cell>

## **Cross-Type Analysis Guidelines**

When combining multiple EDA types in a single notebook:
1. **Start with Descriptive** - establish baseline understanding
2. **Apply Diagnostic** - identify and address quality issues
3. **Proceed to Inferential** - test hypotheses and relationships
4. **Conclude with Prescriptive** - extract actionable insights

## **Output Requirements**

- All cells should be executed before saving
- Clear the output of any cells with sensitive data
- Export key findings to summary markdown file if requested
- Save processed datasets to `/data/processed/` with clear naming

## 🔬 Research Templates

For specialized investigation of this task, use:
`@workspace #file:.github/instructions/research_prompts/tasks/notebook-eda_research.md`

This template provides:
- 📋 **Best practices** for notebook EDA
- 🚫 **Anti-patterns** that reduce analysis effectiveness
- 🚀 **Optimization recommendations** for better exploration
- 💼 **Context-specific guidance** for inventory analysis

### Usage with MCP Tools

Combine research prompts with MCP tools for enhanced EDA:

```markdown
# Complete EDA research workflow
@workspace #file:.github/instructions/research_prompts/tasks/notebook-eda_research.md

"Create comprehensive EDA for Gasco inventory dataset, use context7"
```

### Automatic Application
- When **creating notebooks** → Research template applied
- When performing **EDA tasks** → Best practices included
- When working with **inventory data** → Domain-specific patterns followed
