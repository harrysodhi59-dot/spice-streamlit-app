import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Real Site Validation", layout="wide")

st.title("📊 Real Site Validation: Real vs Simulated Performance")

# -----------------------------
# Load datasets
# -----------------------------
@st.cache_data
def load_data():
    bissell = pd.read_csv("data/bissell_2025_with_missing_rows.csv")
    visser = pd.read_csv("data/visser_2025_with_missing_rows.csv")
    sim = pd.read_csv("data/St_Augustine_combined_simulated_monthly.csv")
    return bissell, visser, sim

bissell, visser, sim = load_data()

# -----------------------------
# CLEAN & PREP REAL DATA
# -----------------------------
def process_real(df, name):
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month
    df["daily_kwh"] = pd.to_numeric(df["daily_kwh"], errors="coerce")

    monthly = df.groupby("month")["daily_kwh"].sum().reset_index()
    monthly["site"] = name
    return monthly

bissell_m = process_real(bissell, "Bissell")
visser_m = process_real(visser, "Visser")

# -----------------------------
# CLEAN SIM DATA
# -----------------------------
sim["month"] = sim["month"].astype(int)
sim["monthly_kwh"] = pd.to_numeric(sim["monthly_kwh"], errors="coerce")

sim_m = sim.groupby("month")["monthly_kwh"].mean().reset_index()
sim_m.rename(columns={"monthly_kwh": "daily_kwh"}, inplace=True)
sim_m["site"] = "Simulated"

# -----------------------------
# COMBINE ALL
# -----------------------------
df_all = pd.concat([bissell_m, visser_m, sim_m])

# -----------------------------
# REVENUE CALCULATION
# -----------------------------
electricity_rate = 0.12
df_all["revenue"] = df_all["daily_kwh"] * electricity_rate

# -----------------------------
# KPI CALCULATIONS
# -----------------------------
summary = df_all.groupby("site").agg({
    "daily_kwh": "sum",
    "revenue": "sum"
}).reset_index()

# -----------------------------
# KPI DISPLAY
# -----------------------------
st.subheader("🔢 Key Performance Comparison")

col1, col2, col3 = st.columns(3)

for i, row in summary.iterrows():
    with [col1, col2, col3][i]:
        st.metric(
            label=row["site"],
            value=f"{row['daily_kwh']:.0f} kWh",
            delta=f"${row['revenue']:.0f}"
        )

# -----------------------------
# PRODUCTION COMPARISON
# -----------------------------
st.subheader("⚡ Monthly Production Comparison")

fig_prod = px.line(
    df_all,
    x="month",
    y="daily_kwh",
    color="site",
    markers=True
)
fig_prod.update_layout(yaxis_title="Energy (kWh)")
st.plotly_chart(fig_prod, use_container_width=True)

# -----------------------------
# REVENUE COMPARISON
# -----------------------------
st.subheader("💰 Revenue Comparison")

fig_rev = px.bar(
    summary,
    x="site",
    y="revenue",
    color="site",
    text="revenue"
)
fig_rev.update_traces(texttemplate="$%{text:.0f}", textposition="outside")
st.plotly_chart(fig_rev, use_container_width=True)

# -----------------------------
# VALIDATION GAP
# -----------------------------
st.subheader("📉 Model Validation Gap")

real_avg = summary[summary["site"] != "Simulated"]["daily_kwh"].mean()
sim_val = summary[summary["site"] == "Simulated"]["daily_kwh"].values[0]

gap = sim_val - real_avg
gap_percent = (gap / real_avg) * 100

st.metric(
    label="Simulation vs Real Average",
    value=f"{gap:.0f} kWh",
    delta=f"{gap_percent:.1f}%"
)

# -----------------------------
# INSIGHT BOX
# -----------------------------
st.info(f"""
The simulated model produces {abs(gap_percent):.1f}% {'higher' if gap_percent > 0 else 'lower'}
output compared to the average of real sites. 

This indicates that the model {'overestimates' if gap_percent > 0 else 'underestimates'}
real-world solar performance, but still follows a similar seasonal trend.
""")
