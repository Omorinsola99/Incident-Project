import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Incident Performance Dashboard", layout="wide")

# ------------------ GLOBAL STREAMLIT STYLE ------------------
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    h1, h2, h3 {
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    div[data-testid="metric-container"] {
        background-color: #1A1F2B;
        border-radius: 12px;
        padding: 12px;
        border: 1px solid #2A2F3A;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ GLOBAL PLOTLY THEME ------------------
pio.templates["custom_dark"] = pio.templates["plotly_dark"]
pio.templates["custom_dark"].layout.update({
    "paper_bgcolor": "#0E1117",
    "plot_bgcolor": "#0E1117",
    "font": {"color": "#FFFFFF", "family": "Arial"},
    "title": {"x": 0.02, "xanchor": "left"},
    "margin": {"l": 20, "r": 20, "t": 50, "b": 20},
    "hovermode": "x unified"
})
pio.templates.default = "custom_dark"

st.title("📊 Incident Performance Dashboard")
st.markdown("Operational insights based on incident data across states and time")

# ------------------ LOAD DATA -------------------
df = pd.read_csv("morin.csv")

# ------------------ DATA PREP ------------------
df['Start date'] = pd.to_datetime(df['Start date'])
df['End date'] = pd.to_datetime(df['End date'])
df['Duration'] = (df['End date'] - df['Start date']).dt.days

# ------------------ KPI ------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Incidents", len(df))
c2.metric("Avg Resolution Time", f"{df['Duration'].mean():.1f} days")
c3.metric("Max Resolution Time", f"{df['Duration'].max()} days")
c4.metric("States Covered", df['State'].nunique())

st.divider()

# =========================================================
# 1. INCIDENT DISTRIBUTION BY STATE
# =========================================================
st.subheader("Which states experience the highest number of incidents?")

state_counts = df['State'].value_counts().reset_index()
state_counts.columns = ['State', 'Count']

fig1 = px.bar(state_counts, x='State', y='Count', color='Count',
              title="Incident Distribution by State")
st.plotly_chart(fig1, use_container_width=True)

st.caption("States with the highest incident volumes represent operational hotspots. These regions should be prioritized for resource allocation and preventive interventions.")

# =========================================================
# 2. INCIDENT TREND OVER TIME
# =========================================================
st.subheader("What is the trend of incidents over time?")

df['Month'] = df['Start date'].dt.to_period('M').astype(str)
trend = df.groupby('Month').size().reset_index(name='Count')

fig2 = px.line(trend, x='Month', y='Count', markers=True,
               title="Monthly Incident Trend")
st.plotly_chart(fig2, use_container_width=True)

st.caption("The trend highlights seasonality and spikes. Sudden increases may indicate system failures, environmental factors, or operational disruptions.")

# =========================================================
# 3. STATE-LEVEL RESOLUTION PERFORMANCE
# =========================================================
st.subheader("Which states have the longest average resolution time?")

duration_state = df.groupby('State')['Duration'].mean().reset_index()

fig5 = px.bar(duration_state, x='State', y='Duration', color='Duration',
              title="Average Resolution Time by State")
st.plotly_chart(fig5, use_container_width=True)

st.caption("States with higher average resolution times indicate operational bottlenecks, resource constraints, or process inefficiencies.")

# =========================================================
# 4. INCIDENTS BY DAY OF WEEK
# =========================================================
st.subheader("How do incident volumes vary by day of the week?")

df['Day'] = df['Start date'].dt.day_name()
day_counts = df['Day'].value_counts().reset_index()
day_counts.columns = ['Day', 'Count']

fig6 = px.bar(day_counts, x='Day', y='Count', color='Count',
              title="Incidents by Day of Week")
st.plotly_chart(fig6, use_container_width=True)

st.caption("The chart shows which days experience higher incident loads, helping identify peak operational periods and staffing needs.")

# =========================================================
# 5. TOP 5 STATES BY INCIDENT VOLUME
# =========================================================
st.subheader("What are the top 5 states contributing to incidents?")

top_states = df['State'].value_counts().nlargest(5).reset_index()
top_states.columns = ['State', 'Count']

fig9 = px.bar(top_states, x='State', y='Count', color='Count',
              title="Top 5 States by Incident Volume")
st.plotly_chart(fig9, use_container_width=True)

st.caption("The chart isolates the highest contributing states, allowing focused intervention where impact will be greatest.")

# =========================================================
# 6. YEARLY AVERAGE RESOLUTION TIME
# =========================================================
st.subheader("What is the yearly average resolution time?")

monthly_duration = df.groupby(df['Start date'].dt.to_period('M'))['Duration'].mean().reset_index()
monthly_duration['Start date'] = monthly_duration['Start date'].astype(str)

fig12 = px.line(monthly_duration, x='Start date', y='Duration',
                title="Yearly Average Resolution Time")
st.plotly_chart(fig12, use_container_width=True)

st.caption("This trend shows whether operational efficiency is improving or deteriorating over time.")

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("Designed with a focus on operational intelligence, performance monitoring, and data-driven decision making.")
