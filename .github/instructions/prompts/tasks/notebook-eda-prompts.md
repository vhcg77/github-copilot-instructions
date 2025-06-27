---
applyTo: ["eda", "notebooks", "analysis"]
task: "notebook-eda"
description: "Prompt examples for EDA notebook tasks"
tags: ["eda", "notebook", "pandas", "matplotlib", "seaborn", "plotly", "analysis"]
priority: "high"
---

# **Task: Notebook EDA Prompts**

## **1. Comprehensive EDA for New Dataset**

### **Prompt**

"I have a new dataset `df` loaded from a CSV file with various columns including numerical and categorical variables. Generate a complete EDA notebook following the structured approach. The notebook should include:

1. **Introduction section** with clear objectives and dataset description
2. **Data loading and initial inspection** with shape, memory usage, and basic info
3. **Data quality assessment** including missing values, duplicates, and data types
4. **Descriptive statistics** for both numerical and categorical variables
5. **Comprehensive visualizations** including distributions, correlations, and geographic analysis if applicable
6. **Key insights and patterns** with business-relevant interpretations
7. **Summary and recommendations** section

Use professional formatting with clear markdown sections, proper plot titles, and consistent styling throughout."

---

## **2. Geographic Data Analysis**

### **Prompt**

"I have a dataset with location/geographic information in columns like 'Location', 'Region', or 'City'. Create an EDA section focused on geographic analysis that includes:

1. **Location distribution analysis** with counts and percentages
2. **Regional grouping** and classification (e.g., US, Europe, Asia)
3. **Geographic heatmaps** showing resource distribution by location
4. **Cross-analysis** between location and other categorical variables
5. **Top locations visualization** with bar charts and pie charts
6. **Geographic diversity metrics** and insights

Include both static (matplotlib/seaborn) and interactive (plotly) visualizations."

---

## **3. Time Series EDA**

### **Prompt**

"I have a dataset with datetime columns (e.g., 'created_date', 'modified_date', 'timestamp'). Generate EDA code for temporal analysis including:

1. **Date parsing** and datetime feature extraction (year, month, day, weekday)
2. **Temporal distributions** showing patterns over time
3. **Seasonality analysis** with monthly/quarterly aggregations  
4. **Trend analysis** with time series plots
5. **Peak activity identification** (busiest days, months, etc.)
6. **Temporal correlations** with other variables

Use appropriate time series visualization techniques and statistical analysis."

---

## **4. Missing Data Analysis**

### **Prompt**

"Generate a comprehensive missing data analysis for my dataset including:

1. **Missing value heatmap** showing patterns across all columns
2. **Missing data statistics** with counts and percentages
3. **Missing data patterns** analysis (MCAR, MAR, MNAR assessment)
4. **Correlation between missing values** across different columns
5. **Impact assessment** of missing data on key variables
6. **Imputation strategy recommendations** based on the analysis

Include both visual and statistical approaches to understand the missing data patterns."

---

## **5. Categorical Data Deep Dive**

### **Prompt**

"I need a detailed analysis of categorical variables in my dataset. Create EDA code that includes:

1. **Categorical summary statistics** with unique counts and value frequencies
2. **Cross-tabulation analysis** between categorical variables
3. **Chi-square tests** for independence between categorical variables
4. **Categorical distribution visualizations** with bar charts and pie charts
5. **Rare category identification** and analysis
6. **Category grouping recommendations** for machine learning

Focus on finding meaningful patterns and relationships between categorical variables."

---

## **6. Business Metrics Dashboard**

### **Prompt**

"Create an executive-level EDA summary that focuses on business metrics and KPIs. The analysis should include:

1. **Key business metrics** extracted from the data
2. **Performance indicators** and their distributions
3. **Comparative analysis** across different business dimensions
4. **Outlier detection** for unusual business patterns
5. **Business health indicators** and red flags
6. **Actionable insights** with specific recommendations

Present findings in a clear, business-friendly format with executive summary and detailed analysis sections."

---

## **7. Descriptive EDA (eda_descriptive_*)**

### **Prompt**

"Generate a descriptive EDA notebook that provides a comprehensive overview of the dataset structure and basic characteristics. Include:

1. **Dataset overview** with shape, column types, and memory usage
2. **Univariate analysis** for each variable type (numerical and categorical)
3. **Summary statistics** with central tendency and variability measures
4. **Missing values assessment** with counts and percentages
5. **Data type validation** and recommendations for corrections
6. **Basic distribution visualizations** (histograms, bar charts, box plots)

Focus on understanding 'what the data looks like' rather than relationships or patterns."

---

## **8. Diagnostic EDA (eda_diagnostic_*)**

### **Prompt**

"Create a diagnostic EDA notebook focused on data quality assessment and anomaly detection. Include:

1. **Comprehensive missing data analysis** with patterns and impact assessment
2. **Duplicate detection** and analysis of duplicate patterns
3. **Outlier identification** using multiple methods (IQR, Z-score, isolation forest)
4. **Data consistency checks** across related columns
5. **Business rule validation** (e.g., dates, ranges, formats)
6. **Data profiling report** with quality scores and recommendations

Generate actionable recommendations for data cleaning and quality improvement."

---

## **9. Inferential EDA (eda_inferential_*)**

### **Prompt**

"Develop an inferential EDA notebook that explores statistical relationships and tests hypotheses. Include:

1. **Correlation analysis** with significance testing and confidence intervals
2. **Hypothesis formulation** based on business questions
3. **Statistical tests** (t-tests, chi-square, ANOVA) with proper interpretation
4. **Confidence intervals** for key metrics and differences
5. **Effect size calculations** and practical significance assessment
6. **Causal inference exploration** with confounding variable analysis

Focus on statistical rigor and proper interpretation of p-values and effect sizes."

---

## **10. Prescriptive EDA (eda_prescriptive_*)**

### **Prompt**

"Generate a prescriptive EDA notebook that translates analytical findings into actionable business recommendations. Include:

1. **Business impact analysis** linking statistical findings to business outcomes
2. **Feature importance ranking** for future modeling efforts
3. **Segment identification** and characterization for targeted strategies
4. **Risk assessment** and opportunity identification
5. **Data-driven recommendations** for business process improvements
6. **Next steps roadmap** including modeling approach and additional data needs

Present findings in executive-friendly format with clear action items and expected business value."
