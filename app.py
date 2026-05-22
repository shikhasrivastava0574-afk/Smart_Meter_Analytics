import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Smart Meter Analytics",
    layout="wide"
)

st.title("⚡ Smart Meter Analytics Dashboard")

# -------------------------
# LOAD DATA
# -------------------------
file = "Daily_Billing_Load Profile.xlsx"

daily = pd.read_excel(file, sheet_name='Daily_profile')
billing = pd.read_excel(file, sheet_name='Billing_profile')
load = pd.read_excel(file, sheet_name='Load_profile')

# -------------------------
# DATE CONVERSION
# -------------------------
daily['READ_DTTM'] = pd.to_datetime(
    daily['READ_DTTM'],
    format='mixed',
    dayfirst=True,
    errors='coerce'
)

billing['START_DTTM'] = pd.to_datetime(
    billing['START_DTTM'],
    format='mixed',
    dayfirst=True,
    errors='coerce'
)

load['READ_DTTM'] = pd.to_datetime(
    load['READ_DTTM'],
    format='mixed',
    dayfirst=True,
    errors='coerce'
)

# -------------------------
# KPI CARDS
# -------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Meters", daily['METER_NUMBER'].nunique())

col2.metric("Total Readings", len(load))

col3.metric("Peak Load", round(load['READS'].max(),2))

col4.metric("Average Load", round(load['READS'].mean(),2))

# -------------------------
# LOAD OVER TIME
# -------------------------
st.subheader("📈 Load Trend Over Time")

trend = load.groupby('READ_DTTM')['READS'].mean().reset_index()

fig1 = px.line(
    trend,
    x='READ_DTTM',
    y='READS',
    title='Average Load Over Time'
)

st.plotly_chart(fig1, use_container_width=True)

# -------------------------
# TOP PEAK LOADS
# -------------------------
# -------------------------------
# PEAK HOUR ANALYSIS
# -------------------------------

st.subheader("⏰ Peak Hour Analysis")

# Extract hour from datetime
load['Hour'] = load['READ_DTTM'].dt.hour

# Average load for each hour
hourly = load.groupby('Hour')['READS'].mean().reset_index()

# Find peak hour
peak_hour = hourly.loc[hourly['READS'].idxmax()]

# Create chart
fig_hour = px.line(
    hourly,
    x='Hour',
    y='READS',
    markers=True,
    title='Average Load by Hour of Day'
)

# Improve chart design
fig_hour.update_layout(
    xaxis_title='Hour of Day (0 = 12 AM, 23 = 11 PM)',
    yaxis_title='Average Electricity Load',
    template='plotly_dark'
)

# Highlight peak point
fig_hour.add_scatter(
    x=[peak_hour['Hour']],
    y=[peak_hour['READS']],
    mode='markers+text',
    text=['Peak Load'],
    textposition='top center',
    marker=dict(size=15, color='red'),
    name='Peak Hour'
)

# Show chart
st.plotly_chart(fig_hour, use_container_width=True)

# Smart Insight
st.success(
    f"""
    🔥 Highest electricity consumption occurs around 
    {int(peak_hour['Hour'])}:00 hours 
    with an average load of 
    {round(peak_hour['READS'],2)} units.
    
    This time period can be considered a PEAK LOAD WINDOW 
    where dynamic pricing can help utility companies 
    increase revenue and reduce overload demand.
    """
)

# -------------------------
# METER ANALYSIS
# -------------------------
# -------------------------------
# METER-WISE CONSUMPTION ANALYSIS
# -------------------------------

st.subheader("🔌 Meter-wise Consumption Analysis")

# Total consumption by meter
meter = load.groupby('METER_NUMBER')['READS'].sum().reset_index()

# Sort descending
meter = meter.sort_values(by='READS', ascending=False).head(10)

# Create colorful chart
fig3 = px.bar(
    meter,
    x='METER_NUMBER',
    y='READS',
    color='READS',
    text='READS',
    title='Top Energy Consuming Meters'
)

# Improve design
fig3.update_layout(
    xaxis_title='Meter Number',
    yaxis_title='Total Energy Consumption',
    xaxis_tickangle=-45,
    template='plotly_dark'
)

# Show values
fig3.update_traces(
    texttemplate='%{text:.2f}',
    textposition='outside'
)

# Display graph
st.plotly_chart(fig3, use_container_width=True)

# Smart insight
top_meter = meter.iloc[0]

st.warning(
    f"""
    ⚠️ Meter {top_meter['METER_NUMBER']} recorded the highest electricity usage 
    with total consumption of {round(top_meter['READS'],2)} units.

    This meter may belong to a high-demand consumer or commercial load 
    and can be monitored for dynamic pricing or anomaly detection.
    """
)

# -------------------------
# AI/ML USE CASE SECTION
# -------------------------
st.subheader("🤖 AI/ML Use Cases")

st.markdown("""
- Dynamic Electricity Pricing
- Peak Load Prediction
- Energy Theft Detection
- Smart Demand Forecasting
- Personalized Energy Recommendations
- Predictive Maintenance
- Real-time Smart Meter Monitoring
""")
