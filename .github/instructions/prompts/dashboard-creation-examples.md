---
applyTo: ["dashboard", "examples", "visualization", "kpi"]
description: "Dashboard creation prompt examples and templates"
tags: ["dashboard", "streamlit", "plotly", "bigquery", "kpi", "analytics"]
priority: "medium"
---

# Dashboard Creation Prompt Examples

## Prompt: Create Executive KPI Dashboard

**User Input:**
"I need to create an executive dashboard showing key business metrics for our e-commerce platform. The dashboard should show revenue, customer acquisition, conversion rates, and regional performance. It needs to be updated daily and accessible on mobile devices."

**Expected Response Format:**

### Executive KPI Dashboard Implementation

```python
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from google.cloud import bigquery

# Dashboard configuration
st.set_page_config(
    page_title="Executive KPI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

class ExecutiveDashboard:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.client = bigquery.Client(project=project_id)
        
    def load_kpi_data(self, date_range: tuple) -> dict:
        """Load KPI data from BigQuery."""
        start_date, end_date = date_range
        
        queries = {
            'revenue_metrics': f"""
                SELECT 
                    DATE(order_date) as date,
                    SUM(total_amount) as daily_revenue,
                    COUNT(DISTINCT order_id) as daily_orders,
                    COUNT(DISTINCT customer_id) as daily_customers,
                    AVG(total_amount) as avg_order_value
                FROM `{self.project_id}.analytics.orders`
                WHERE DATE(order_date) BETWEEN '{start_date}' AND '{end_date}'
                    AND status = 'completed'
                GROUP BY DATE(order_date)
                ORDER BY date
            """,
            
            'customer_metrics': f"""
                SELECT 
                    DATE(registration_date) as date,
                    COUNT(*) as new_customers,
                    COUNT(DISTINCT CASE WHEN source = 'organic' THEN customer_id END) as organic_customers,
                    COUNT(DISTINCT CASE WHEN source = 'paid' THEN customer_id END) as paid_customers
                FROM `{self.project_id}.analytics.customers`
                WHERE DATE(registration_date) BETWEEN '{start_date}' AND '{end_date}'
                GROUP BY DATE(registration_date)
                ORDER BY date
            """,
            
            'conversion_metrics': f"""
                SELECT 
                    DATE(session_date) as date,
                    COUNT(DISTINCT session_id) as total_sessions,
                    COUNT(DISTINCT CASE WHEN converted = true THEN session_id END) as converted_sessions,
                    SAFE_DIVIDE(
                        COUNT(DISTINCT CASE WHEN converted = true THEN session_id END),
                        COUNT(DISTINCT session_id)
                    ) as conversion_rate
                FROM `{self.project_id}.analytics.sessions`
                WHERE DATE(session_date) BETWEEN '{start_date}' AND '{end_date}'
                GROUP BY DATE(session_date)
                ORDER BY date
            """,
            
            'regional_performance': f"""
                SELECT 
                    region,
                    SUM(total_amount) as total_revenue,
                    COUNT(DISTINCT order_id) as total_orders,
                    COUNT(DISTINCT customer_id) as unique_customers,
                    AVG(total_amount) as avg_order_value
                FROM `{self.project_id}.analytics.orders` o
                JOIN `{self.project_id}.analytics.customers` c ON o.customer_id = c.customer_id
                WHERE DATE(o.order_date) BETWEEN '{start_date}' AND '{end_date}'
                    AND o.status = 'completed'
                GROUP BY region
                ORDER BY total_revenue DESC
            """
        }
        
        data = {}
        for key, query in queries.items():
            data[key] = self.client.query(query).to_dataframe()
        
        return data
    
    def calculate_kpis(self, data: dict) -> dict:
        """Calculate summary KPIs."""
        revenue_df = data['revenue_metrics']
        customer_df = data['customer_metrics']
        conversion_df = data['conversion_metrics']
        
        # Current period metrics
        total_revenue = revenue_df['daily_revenue'].sum()
        total_orders = revenue_df['daily_orders'].sum()
        total_customers = customer_df['new_customers'].sum()
        avg_conversion_rate = conversion_df['conversion_rate'].mean()
        
        # Previous period metrics for comparison
        current_days = len(revenue_df)
        prev_period_revenue = revenue_df.tail(current_days//2)['daily_revenue'].sum() * 2
        prev_period_customers = customer_df.tail(current_days//2)['new_customers'].sum() * 2
        
        # Calculate growth rates
        revenue_growth = ((total_revenue - prev_period_revenue) / prev_period_revenue * 100) if prev_period_revenue > 0 else 0
        customer_growth = ((total_customers - prev_period_customers) / prev_period_customers * 100) if prev_period_customers > 0 else 0
        
        return {
            'total_revenue': total_revenue,
            'revenue_growth': revenue_growth,
            'total_orders': total_orders,
            'total_customers': total_customers,
            'customer_growth': customer_growth,
            'avg_conversion_rate': avg_conversion_rate,
            'avg_order_value': total_revenue / total_orders if total_orders > 0 else 0
        }

def create_kpi_cards(kpis: dict):
    """Create KPI cards with metrics and trends."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Total Revenue",
            value=f"${kpis['total_revenue']:,.0f}",
            delta=f"{kpis['revenue_growth']:.1f}%"
        )
    
    with col2:
        st.metric(
            label="👥 New Customers",
            value=f"{kpis['total_customers']:,}",
            delta=f"{kpis['customer_growth']:.1f}%"
        )
    
    with col3:
        st.metric(
            label="📈 Conversion Rate",
            value=f"{kpis['avg_conversion_rate']:.2%}",
            delta="0.2%" # You would calculate this from previous period
        )
    
    with col4:
        st.metric(
            label="🛒 Avg Order Value",
            value=f"${kpis['avg_order_value']:.2f}",
            delta="5.2%" # You would calculate this from previous period
        )

def create_revenue_trend_chart(revenue_data: pd.DataFrame):
    """Create revenue trend chart."""
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Daily Revenue', 'Daily Orders'),
        vertical_spacing=0.1,
        specs=[[{"secondary_y": False}], [{"secondary_y": False}]]
    )
    
    # Revenue trend
    fig.add_trace(
        go.Scatter(
            x=revenue_data['date'],
            y=revenue_data['daily_revenue'],
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#1f77b4', width=3),
            hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Orders trend
    fig.add_trace(
        go.Scatter(
            x=revenue_data['date'],
            y=revenue_data['daily_orders'],
            mode='lines+markers',
            name='Orders',
            line=dict(color='#ff7f0e', width=3),
            hovertemplate='<b>%{x}</b><br>Orders: %{y:,.0f}<extra></extra>'
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        height=500,
        showlegend=True,
        title_text="Revenue and Orders Trends",
        title_x=0.5
    )
    
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
    fig.update_yaxes(title_text="Orders", row=2, col=1)
    
    return fig

def create_regional_performance_chart(regional_data: pd.DataFrame):
    """Create regional performance visualization."""
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by region - bar chart
        fig_bar = px.bar(
            regional_data,
            x='region',
            y='total_revenue',
            title='Revenue by Region',
            color='total_revenue',
            color_continuous_scale='Blues'
        )
        fig_bar.update_layout(height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Regional metrics - pie chart
        fig_pie = px.pie(
            regional_data,
            values='total_revenue',
            names='region',
            title='Revenue Distribution'
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

def create_conversion_funnel(data: dict):
    """Create conversion funnel visualization."""
    conversion_data = data['conversion_metrics']
    
    # Calculate funnel metrics
    total_sessions = conversion_data['total_sessions'].sum()
    converted_sessions = conversion_data['converted_sessions'].sum()
    
    # Create funnel data
    funnel_data = pd.DataFrame({
        'Stage': ['Website Visits', 'Product Views', 'Add to Cart', 'Checkout', 'Purchase'],
        'Count': [total_sessions, total_sessions * 0.6, total_sessions * 0.3, 
                 total_sessions * 0.15, converted_sessions],
        'Percentage': [100, 60, 30, 15, (converted_sessions/total_sessions)*100]
    })
    
    fig = go.Figure(go.Funnel(
        y=funnel_data['Stage'],
        x=funnel_data['Count'],
        texttemplate='%{label}<br>%{value:,.0f} (%{percentTotal})',
        textfont={"size": 14},
        connector={"line": {"color": "royalblue"}},
        marker={"color": ["deepskyblue", "lightsalmon", "tan", "teal", "silver"]}
    ))
    
    fig.update_layout(
        title="Customer Conversion Funnel",
        height=500
    )
    
    return fig

# Main dashboard application
def main():
    st.title("📊 Executive KPI Dashboard")
    st.markdown("---")
    
    # Sidebar controls
    with st.sidebar:
        st.header("Dashboard Controls")
        
        # Date range selector
        date_range = st.date_input(
            "Select Date Range",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
            max_value=datetime.now()
        )
        
        # Auto-refresh toggle
        auto_refresh = st.checkbox("Auto-refresh (every 5 minutes)")
        
        # Regional filter
        selected_regions = st.multiselect(
            "Filter by Regions",
            options=["North", "South", "East", "West", "International"],
            default=["North", "South", "East", "West", "International"]
        )
        
        # Refresh button
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
    
    # Load dashboard data
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def load_dashboard_data(date_range):
        dashboard = ExecutiveDashboard('your-project-id')
        return dashboard.load_kpi_data(date_range)
    
    # Main dashboard content
    try:
        with st.spinner("Loading dashboard data..."):
            data = load_dashboard_data(date_range)
            dashboard = ExecutiveDashboard('your-project-id')
            kpis = dashboard.calculate_kpis(data)
        
        # KPI Cards
        st.subheader("📈 Key Performance Indicators")
        create_kpi_cards(kpis)
        
        st.markdown("---")
        
        # Revenue trends
        st.subheader("💰 Revenue Trends")
        revenue_chart = create_revenue_trend_chart(data['revenue_metrics'])
        st.plotly_chart(revenue_chart, use_container_width=True)
        
        st.markdown("---")
        
        # Regional performance
        st.subheader("🌍 Regional Performance")
        create_regional_performance_chart(data['regional_performance'])
        
        st.markdown("---")
        
        # Conversion funnel
        st.subheader("🎯 Conversion Funnel")
        funnel_chart = create_conversion_funnel(data)
        st.plotly_chart(funnel_chart, use_container_width=True)
        
        # Data table
        with st.expander("📋 Detailed Regional Data"):
            st.dataframe(
                data['regional_performance'].style.format({
                    'total_revenue': '${:,.0f}',
                    'avg_order_value': '${:.2f}'
                }),
                use_container_width=True
            )
        
        # Last updated timestamp
        st.sidebar.markdown(f"**Last updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
        st.info("Please check your data connections and try again.")

# Custom CSS for mobile responsiveness
st.markdown("""
<style>
    @media (max-width: 768px) {
        .stMetric {
            font-size: 0.8rem;
        }
        .plot-container {
            height: 300px !important;
        }
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .stMetric > label {
        font-size: 14px !important;
        color: #666 !important;
    }
</style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
```

### Deployment Configuration

```dockerfile
# Dockerfile for dashboard deployment
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
COPY dashboard/ .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```yaml
# requirements.txt
streamlit==1.28.0
plotly==5.15.0
pandas==2.0.3
google-cloud-bigquery==3.11.4
google-cloud-secret-manager==2.16.4
```

```yaml
# Cloud Run deployment
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: executive-dashboard
  annotations:
    run.googleapis.com/ingress: all
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/maxScale: "10"
        run.googleapis.com/memory: "2Gi"
        run.googleapis.com/cpu: "1000m"
    spec:
      containers:
      - image: gcr.io/PROJECT_ID/executive-dashboard
        ports:
        - containerPort: 8501
        env:
        - name: GOOGLE_CLOUD_PROJECT
          value: "your-project-id"
        resources:
          limits:
            memory: "2Gi"
            cpu: "1000m"
```

---

## Prompt: Create Real-time Monitoring Dashboard

**User Input:**
"I need a real-time monitoring dashboard for our data pipeline. It should show pipeline status, data quality metrics, processing times, and alert when something goes wrong. The dashboard should update every 30 seconds."

**Expected Response Format:**

### Real-time Pipeline Monitoring Dashboard

```python
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import time
from datetime import datetime, timedelta
import asyncio
from google.cloud import monitoring_v3, bigquery
import json

# Configure page
st.set_page_config(
    page_title="Pipeline Monitor",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

class PipelineMonitor:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.monitoring_client = monitoring_v3.MetricServiceClient()
        self.bq_client = bigquery.Client(project=project_id)
        
    def get_pipeline_status(self) -> pd.DataFrame:
        """Get current status of all pipelines."""
        query = """
        SELECT 
            pipeline_name,
            status,
            start_time,
            end_time,
            duration_minutes,
            records_processed,
            error_message
        FROM `{}.monitoring.pipeline_runs`
        WHERE DATE(start_time) >= CURRENT_DATE()
        ORDER BY start_time DESC
        LIMIT 50
        """.format(self.project_id)
        
        return self.bq_client.query(query).to_dataframe()
    
    def get_quality_metrics(self) -> dict:
        """Get real-time data quality metrics."""
        query = """
        SELECT 
            table_name,
            completeness_score,
            accuracy_score,
            freshness_hours,
            last_updated
        FROM `{}.monitoring.data_quality_metrics`
        WHERE DATE(last_updated) = CURRENT_DATE()
        ORDER BY last_updated DESC
        """.format(self.project_id)
        
        df = self.bq_client.query(query).to_dataframe()
        return df.to_dict('records') if not df.empty else []
    
    def get_system_metrics(self) -> dict:
        """Get system performance metrics from Cloud Monitoring."""
        project_name = f"projects/{self.project_id}"
        
        # Define time range (last hour)
        now = datetime.utcnow()
        interval = monitoring_v3.TimeInterval({
            "end_time": {"seconds": int(now.timestamp())},
            "start_time": {"seconds": int((now - timedelta(hours=1)).timestamp())}
        })
        
        metrics = {}
        
        # CPU utilization
        cpu_filter = 'metric.type="compute.googleapis.com/instance/cpu/utilization"'
        cpu_request = monitoring_v3.ListTimeSeriesRequest(
            name=project_name,
            filter=cpu_filter,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
        )
        
        try:
            cpu_results = self.monitoring_client.list_time_series(request=cpu_request)
            cpu_values = []
            for result in cpu_results:
                for point in result.points:
                    cpu_values.append(point.value.double_value * 100)
            
            metrics['avg_cpu'] = sum(cpu_values) / len(cpu_values) if cpu_values else 0
            metrics['max_cpu'] = max(cpu_values) if cpu_values else 0
        except Exception as e:
            metrics['avg_cpu'] = 0
            metrics['max_cpu'] = 0
        
        return metrics

def create_status_overview(pipeline_data: pd.DataFrame):
    """Create pipeline status overview."""
    if pipeline_data.empty:
        st.warning("No pipeline data available")
        return
    
    # Calculate status counts
    status_counts = pipeline_data['status'].value_counts()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        running_count = status_counts.get('RUNNING', 0)
        st.metric("🔄 Running", running_count)
    
    with col2:
        success_count = status_counts.get('SUCCESS', 0)
        st.metric("✅ Successful", success_count)
    
    with col3:
        failed_count = status_counts.get('FAILED', 0)
        st.metric("❌ Failed", failed_count, delta=None)
    
    with col4:
        avg_duration = pipeline_data['duration_minutes'].mean()
        st.metric("⏱️ Avg Duration", f"{avg_duration:.1f} min")

def create_pipeline_timeline(pipeline_data: pd.DataFrame):
    """Create pipeline execution timeline."""
    if pipeline_data.empty:
        return go.Figure()
    
    # Color mapping for status
    color_map = {
        'SUCCESS': '#28a745',
        'FAILED': '#dc3545',
        'RUNNING': '#ffc107',
        'PENDING': '#6c757d'
    }
    
    fig = px.timeline(
        pipeline_data,
        x_start='start_time',
        x_end='end_time',
        y='pipeline_name',
        color='status',
        color_discrete_map=color_map,
        title="Pipeline Execution Timeline",
        hover_data=['records_processed', 'duration_minutes']
    )
    
    fig.update_layout(
        height=400,
        xaxis_title="Time",
        yaxis_title="Pipeline",
        showlegend=True
    )
    
    return fig

def create_quality_scorecard(quality_metrics: list):
    """Create data quality scorecard."""
    if not quality_metrics:
        st.warning("No quality metrics available")
        return
    
    df = pd.DataFrame(quality_metrics)
    
    # Create quality score gauge charts
    cols = st.columns(len(df))
    
    for i, (_, row) in enumerate(df.iterrows()):
        with cols[i % len(cols)]:
            # Completeness gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=row['completeness_score'] * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': f"{row['table_name']}<br>Completeness"},
                delta={'reference': 95},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 80], 'color': "lightgray"},
                        {'range': [80, 95], 'color': "yellow"},
                        {'range': [95, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 95
                    }
                }
            ))
            
            fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)

def create_real_time_metrics(system_metrics: dict):
    """Create real-time system metrics display."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cpu_color = "normal"
        if system_metrics['avg_cpu'] > 80:
            cpu_color = "inverse"
        elif system_metrics['avg_cpu'] > 60:
            cpu_color = "off"
        
        st.metric(
            "🖥️ Avg CPU Usage",
            f"{system_metrics['avg_cpu']:.1f}%",
            delta=f"Max: {system_metrics['max_cpu']:.1f}%"
        )
    
    with col2:
        # Memory usage (placeholder)
        st.metric("🧠 Memory Usage", "68.3%", delta="2.1%")
    
    with col3:
        # Active connections (placeholder)
        st.metric("🔗 Active Connections", "42", delta="3")

def create_alert_feed():
    """Create live alert feed."""
    st.subheader("🚨 Recent Alerts")
    
    # Sample alerts (in real implementation, fetch from monitoring system)
    alerts = [
        {
            'timestamp': datetime.now() - timedelta(minutes=5),
            'severity': 'HIGH',
            'message': 'Pipeline "customer-etl" failed with error: Connection timeout',
            'source': 'customer-etl'
        },
        {
            'timestamp': datetime.now() - timedelta(minutes=15),
            'severity': 'MEDIUM',
            'message': 'Data quality score dropped below 95% for table "orders"',
            'source': 'data-quality'
        },
        {
            'timestamp': datetime.now() - timedelta(minutes=30),
            'severity': 'LOW',
            'message': 'Pipeline "inventory-sync" completed with warnings',
            'source': 'inventory-sync'
        }
    ]
    
    for alert in alerts:
        severity_color = {
            'HIGH': '🔴',
            'MEDIUM': '🟡',
            'LOW': '🟢'
        }
        
        with st.container():
            col1, col2 = st.columns([1, 8])
            with col1:
                st.write(severity_color[alert['severity']])
            with col2:
                st.write(f"**{alert['timestamp'].strftime('%H:%M:%S')}** - {alert['message']}")
            st.markdown("---")

# Main application with auto-refresh
def main():
    st.title("🔍 Real-time Pipeline Monitor")
    
    # Auto-refresh placeholder
    placeholder = st.empty()
    
    # Sidebar controls
    with st.sidebar:
        st.header("Monitor Controls")
        auto_refresh = st.checkbox("Auto-refresh", value=True)
        refresh_interval = st.slider("Refresh interval (seconds)", 10, 300, 30)
        
        # Manual refresh button
        if st.button("🔄 Refresh Now"):
            st.experimental_rerun()
        
        # Filter controls
        st.subheader("Filters")
        selected_pipelines = st.multiselect(
            "Select Pipelines",
            ["customer-etl", "order-processing", "inventory-sync", "analytics-refresh"],
            default=["customer-etl", "order-processing", "inventory-sync", "analytics-refresh"]
        )
        
        time_range = st.selectbox(
            "Time Range",
            ["Last Hour", "Last 4 Hours", "Last 24 Hours", "Last 7 Days"],
            index=1
        )
    
    # Auto-refresh logic
    if auto_refresh:
        # Create a placeholder for the refresh counter
        refresh_counter = st.sidebar.empty()
        
        # Main refresh loop
        for seconds in range(refresh_interval, 0, -1):
            refresh_counter.text(f"Refreshing in {seconds}s...")
            time.sleep(1)
        
        refresh_counter.text("Refreshing...")
        st.experimental_rerun()
    
    # Load data
    monitor = PipelineMonitor('your-project-id')
    
    try:
        with st.spinner("Loading monitoring data..."):
            pipeline_data = monitor.get_pipeline_status()
            quality_metrics = monitor.get_quality_metrics()
            system_metrics = monitor.get_system_metrics()
        
        # Status overview
        st.subheader("📊 Pipeline Status Overview")
        create_status_overview(pipeline_data)
        
        st.markdown("---")
        
        # Timeline view
        st.subheader("📅 Execution Timeline")
        timeline_chart = create_pipeline_timeline(pipeline_data)
        st.plotly_chart(timeline_chart, use_container_width=True)
        
        st.markdown("---")
        
        # Two column layout for metrics and alerts
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Data quality scorecard
            st.subheader("🎯 Data Quality Metrics")
            create_quality_scorecard(quality_metrics)
            
            # System metrics
            st.subheader("⚡ System Performance")
            create_real_time_metrics(system_metrics)
        
        with col2:
            # Alert feed
            create_alert_feed()
        
        # Detailed pipeline table
        st.subheader("📋 Pipeline Details")
        if not pipeline_data.empty:
            # Format the dataframe for display
            display_df = pipeline_data.copy()
            display_df['start_time'] = display_df['start_time'].dt.strftime('%H:%M:%S')
            display_df['duration_minutes'] = display_df['duration_minutes'].round(2)
            
            st.dataframe(
                display_df[['pipeline_name', 'status', 'start_time', 'duration_minutes', 'records_processed']],
                use_container_width=True
            )
        
        # Status bar
        st.sidebar.markdown(f"**Last updated:** {datetime.now().strftime('%H:%M:%S')}")
        
    except Exception as e:
        st.error(f"Error loading monitoring data: {str(e)}")
        st.info("Please check your data connections and try again.")

# Custom CSS for real-time dashboard
st.markdown("""
<style>
    .stMetric {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #007bff;
    }
    
    .alert-high {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 0.5rem;
        margin: 0.25rem 0;
    }
    
    .alert-medium {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 0.5rem;
        margin: 0.25rem 0;
    }
    
    .alert-low {
        background-color: #d1edff;
        border-left: 4px solid #0dcaf0;
        padding: 0.5rem;
        margin: 0.25rem 0;
    }
</style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
```
