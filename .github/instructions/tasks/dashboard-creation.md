---
applyTo: ["dashboard", "visualization", "analytics", "bi"]
description: "Interactive dashboard development instructions"
priority: "high"
---

# Dashboard Creation Instructions

## Objective
Design and implement interactive, insightful dashboards that communicate data stories effectively to stakeholders, using modern visualization tools and best practices for data presentation.

## Design Principles

### 1. User-Centered Design
- **Audience Analysis**: Understand user roles, needs, and technical expertise
- **Information Hierarchy**: Present most important metrics prominently
- **Progressive Disclosure**: Layer detailed information behind high-level summaries
- **Responsive Design**: Ensure usability across devices and screen sizes

### 2. Visual Design Best Practices
- **Color Theory**: Use consistent color palettes with accessibility in mind
- **Typography**: Clear, readable fonts with appropriate sizing
- **White Space**: Avoid clutter, allow elements to breathe
- **Consistency**: Maintain uniform styling across all components

## Dashboard Architecture

### 1. Data Layer
```python
# Data connection and preparation
class DashboardDataSource:
    def __init__(self, connection_string):
        self.connection = connection_string
    
    def get_kpi_data(self, date_range):
        """Fetch KPI data for specified date range."""
        query = """
        SELECT 
            date,
            total_revenue,
            customer_count,
            conversion_rate
        FROM analytics.daily_kpis
        WHERE date BETWEEN %s AND %s
        """
        return pd.read_sql(query, self.connection, params=date_range)
```

### 2. Visualization Components
- **KPI Cards**: High-level metrics with trend indicators
- **Time Series Charts**: Trend analysis over time
- **Comparison Charts**: Bar charts, pie charts for categorical data
- **Geographic Maps**: Spatial data visualization
- **Interactive Tables**: Detailed data exploration

### 3. Interactivity Features
- **Filters**: Date ranges, categories, geographic regions
- **Drill-down**: Click to explore detailed views
- **Cross-filtering**: Selection in one chart affects others
- **Real-time Updates**: Live data refresh capabilities

## Technology Stack

### 1. Python-Based Solutions
```python
# Streamlit dashboard example
import streamlit as st
import plotly.express as px
import pandas as pd

def create_revenue_dashboard():
    st.title("Revenue Analytics Dashboard")
    
    # Sidebar filters
    date_range = st.date_input("Select Date Range")
    region = st.selectbox("Select Region", options=['All', 'North', 'South'])
    
    # Load and filter data
    data = load_revenue_data(date_range, region)
    
    # KPI metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Revenue", f"${data['revenue'].sum():,.0f}")
    with col2:
        st.metric("Growth Rate", f"{data['growth_rate'].mean():.1f}%")
    with col3:
        st.metric("Active Customers", f"{data['customers'].sum():,}")
    
    # Charts
    fig = px.line(data, x='date', y='revenue', title='Revenue Trend')
    st.plotly_chart(fig, use_container_width=True)
```

### 2. Business Intelligence Tools
- **Tableau**: Enterprise-grade analytics platform
- **Power BI**: Microsoft's business intelligence solution
- **Looker**: Google Cloud's BI and data platform
- **Grafana**: Open-source monitoring and observability

### 3. Web-Based Frameworks
- **Streamlit**: Rapid Python web app development
- **Dash**: Python framework for analytical web applications
- **Plotly**: Interactive visualization library
- **D3.js**: JavaScript library for custom visualizations

## Dashboard Types

### 1. Executive Dashboard
- High-level KPIs and summary metrics
- Trend indicators and performance against targets
- Exception reporting and alerts
- Monthly/quarterly business reviews

### 2. Operational Dashboard
- Real-time monitoring of key processes
- Performance metrics and SLA tracking
- Alerting for threshold breaches
- Detailed drill-down capabilities

### 3. Analytical Dashboard
- Exploratory data analysis tools
- Interactive filtering and segmentation
- Statistical analysis and correlation views
- Hypothesis testing and A/B test results

## Best Practices

### 1. Performance Optimization
- **Data Aggregation**: Pre-compute summary statistics
- **Caching**: Implement intelligent data caching strategies
- **Progressive Loading**: Load critical data first
- **Query Optimization**: Efficient database queries

### 2. Accessibility Standards
```css
/* Color accessibility example */
.high-priority {
    background-color: #d32f2f; /* Red with sufficient contrast */
    color: #ffffff;
}

.medium-priority {
    background-color: #f57c00; /* Orange with sufficient contrast */
    color: #000000;
}
```

### 3. Mobile Responsiveness
- Touch-friendly interface elements
- Simplified layouts for small screens
- Swipe gestures for navigation
- Optimized loading for mobile networks

## Quality Assurance

### 1. Data Accuracy Testing
- Validate calculations and aggregations
- Cross-reference with source systems
- Test edge cases and data anomalies
- Verify filtering and drill-down accuracy

### 2. User Experience Testing
- Usability testing with target users
- Performance testing under load
- Cross-browser compatibility
- Mobile device testing

### 3. Security Considerations
- Authentication and authorization
- Data sensitivity and access controls
- Secure data transmission
- Audit logging and monitoring

## Documentation Standards

### 1. Technical Documentation
- Data source specifications
- Calculation methodologies
- Architecture diagrams
- Deployment procedures

### 2. User Documentation
- Dashboard user guides
- Feature tutorials
- FAQ and troubleshooting
- Training materials

### 3. Maintenance Documentation
- Update procedures
- Monitoring and alerting setup
- Performance optimization guide
- Disaster recovery plans

## Deployment and Monitoring

### 1. Deployment Strategy
```yaml
# Docker deployment example
FROM python:3.9-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY dashboard/ /app/
WORKDIR /app

EXPOSE 8501
CMD ["streamlit", "run", "main.py"]
```

### 2. Monitoring and Alerts
- Dashboard usage analytics
- Performance metrics tracking
- Error monitoring and alerting
- User feedback collection

### 3. Continuous Improvement
- Regular user feedback sessions
- Performance optimization cycles
- Feature enhancement planning
- Technology stack updates
