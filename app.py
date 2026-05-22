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
# -------------------------
# TOP PEAK LOADS
# -------------------------

# -------------------------
# TOP PEAK LOADS
# -------------------------

# -------------------------------
# PEAK HOUR ANALYSIS
# -------------------------------

st.subheader("⏰ Peak Hour Analysis")

# Extract hour
load['Hour'] = load['READ_DTTM'].dt.hour

# Average load by hour
hourly = load.groupby('Hour')['READS'].mean().reset_index()

# Create chart
fig_hour = px.line(
    hourly,
    x='Hour',
    y='READS',
    markers=True,
    title='Average Load by Hour of Day'
)

fig_hour.update_layout(
    xaxis_title='Hour of Day',
    yaxis_title='Average Load',
)

st.plotly_chart(fig_hour, use_container_width=True)

# Find peak hour
peak_hour = hourly.loc[hourly['READS'].idxmax()]

st.success(
    f"Highest electricity usage occurs around {int(peak_hour['Hour'])}:00 hours "
    f"with average load of {round(peak_hour['READS'],2)}"
)

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
