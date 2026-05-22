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
st.subheader("⚡ Top Peak Load Timings")

peak = load.groupby('READ_DTTM')['READS'].max().reset_index()

peak = peak.sort_values(by='READS', ascending=False).head(10)

fig2 = px.bar(
    peak,
    x='READ_DTTM',
    y='READS',
    title='Top Peak Load Events'
)

st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# METER ANALYSIS
# -------------------------
st.subheader("🔌 Meter-wise Consumption")

meter = load.groupby('METER_NUMBER')['READS'].mean().reset_index()

meter = meter.sort_values(by='READS', ascending=False).head(10)

fig3 = px.bar(
    meter,
    x='METER_NUMBER',
    y='READS',
    title='Top Consuming Meters'
)

st.plotly_chart(fig3, use_container_width=True)

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
