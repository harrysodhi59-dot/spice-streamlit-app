from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
IMAGE_DIR = BASE_DIR / "images"
MODEL_DIR = BASE_DIR / "models"

# =========================================================
# Styling
# =========================================================
st.markdown(
    """
<style>
html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

.block-container {
    padding-top: 1.6rem;
    padding-bottom: 2.4rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
    max-width: 100%;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(30,111,92,0.18) 0%, transparent 28%),
        radial-gradient(circle at top right, rgba(253,184,19,0.08) 0%, transparent 18%),
        linear-gradient(180deg, #040816 0%, #07111d 45%, #081423 100%);
    color: #F8FAFC;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141B2D 0%, #182133 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}

section[data-testid="stSidebar"] * {
    color: #E5E7EB !important;
}

.hero-box {
    background: linear-gradient(135deg, rgba(30,111,92,0.96) 0%, rgba(11,60,93,0.96) 100%);
    padding: 2.6rem;
    border-radius: 28px;
    color: white;
    box-shadow: 0 20px 46px rgba(0,0,0,0.34);
    min-height: 320px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    border: 1px solid rgba(255,255,255,0.08);
    position: relative;
    overflow: hidden;
}

.hero-box::after {
    content: "";
    position: absolute;
    top: -30px;
    right: -30px;
    width: 180px;
    height: 180px;
    background: radial-gradient(circle, rgba(253,184,19,0.18) 0%, transparent 70%);
    border-radius: 50%;
}

.hero-label {
    color: #D6EFE6 !important;
    font-size: 0.90rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.7px;
    margin-bottom: 1rem;
    position: relative;
    z-index: 2;
}

.hero-title {
    font-size: 2.85rem;
    font-weight: 900;
    line-height: 1.08;
    margin-bottom: 1rem;
    color: #FFFFFF !important;
    position: relative;
    z-index: 2;
}

.hero-highlight {
    color: #FDB813 !important;
}

.hero-text {
    font-size: 1.03rem;
    line-height: 1.8;
    color: #F3F7F6 !important;
    margin-bottom: 0.75rem;
    position: relative;
    z-index: 2;
}

.hero-badge-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 0.7rem;
    margin-top: 1rem;
    position: relative;
    z-index: 2;
}

.hero-badge {
    display: inline-block;
    background: rgba(253,184,19,0.95);
    color: #111827 !important;
    font-weight: 800;
    padding: 0.58rem 1rem;
    border-radius: 999px;
    box-shadow: 0 8px 18px rgba(0,0,0,0.18);
    font-size: 0.92rem;
}

.hero-chip {
    display: inline-block;
    background: rgba(255,255,255,0.10);
    color: #F8FAFC !important;
    font-weight: 700;
    padding: 0.52rem 0.9rem;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.14);
    font-size: 0.85rem;
}

.section-heading {
    font-size: 2rem;
    font-weight: 850;
    color: #F8FAFC !important;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
}

.section-subtext {
    color: #B6C0CE !important;
    font-size: 1rem;
    line-height: 1.75;
    margin-bottom: 1.3rem;
}

.kpi-card {
    background: linear-gradient(180deg, #F8FAFC 0%, #EEF2F7 100%);
    border-radius: 22px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 12px 26px rgba(0,0,0,0.18);
    border: 1px solid rgba(0,0,0,0.05);
    min-height: 132px;
}

.kpi-title {
    color: #0B3C5D;
    font-size: 0.93rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.kpi-value {
    color: #1E6F5C;
    font-size: 1.65rem;
    font-weight: 850;
    line-height: 1.2;
}

.card {
    background: linear-gradient(180deg, #F8FAFC 0%, #EEF2F7 100%);
    border-radius: 22px;
    padding: 1.3rem;
    box-shadow: 0 10px 24px rgba(0,0,0,0.16);
    margin-bottom: 1rem;
    border: 1px solid rgba(0,0,0,0.05);
}

.card-title {
    color: #0B3C5D;
    font-size: 1.28rem;
    font-weight: 850;
    margin-bottom: 0.45rem;
}

.card-label {
    color: #1E6F5C;
    font-size: 0.88rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.35rem;
}

.small-note {
    color: #334155;
    font-size: 0.95rem;
    line-height: 1.7;
}

.insight-box {
    background: linear-gradient(90deg, rgba(30,111,92,0.18), rgba(11,60,93,0.18));
    border-left: 6px solid #FDB813;
    border-radius: 18px;
    padding: 1.1rem 1.25rem;
    margin-top: 0.9rem;
    margin-bottom: 1.3rem;
    color: #E5F3EE !important;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 10px 24px rgba(0,0,0,0.16);
    font-size: 0.98rem;
    line-height: 1.75;
}

.metric-strip {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 1.15rem 1.2rem;
    margin-bottom: 1rem;
}

.metric-label-dark {
    color: #CBD5E1 !important;
    font-size: 0.90rem;
    margin-bottom: 0.35rem;
}

.metric-value-dark {
    color: #F8FAFC !important;
    font-size: 1.8rem;
    font-weight: 850;
}

.footer-note {
    background: linear-gradient(90deg, rgba(30,111,92,0.18), rgba(11,60,93,0.22));
    border-radius: 18px;
    padding: 1rem 1.2rem;
    color: #E5E7EB !important;
    margin-top: 1rem;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 10px 24px rgba(0,0,0,0.16);
}

.assumption-pill {
    display: inline-block;
    padding: 0.4rem 0.75rem;
    border-radius: 999px;
    background: rgba(30,111,92,0.12);
    color: #0B3C5D;
    font-weight: 700;
    margin: 0.15rem 0.2rem 0.15rem 0;
}

@media (max-width: 900px) {
    .hero-title {
        font-size: 2.15rem;
    }
    .hero-box {
        min-height: auto;
        padding: 2rem;
    }
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# Paths and constants
# =========================================================
BASELINE_FEATURES = ["azimuth", "tilt", "hour_sin", "hour_cos", "doy_sin", "doy_cos"]
CORRECTION_FEATURES = [
    "doy_sin",
    "doy_cos",
    "temperature_c",
    "snow_depth_cm",
    "cloud_cover",
    "wind_speed_m_s",
]
MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def candidate_paths(*names: str) -> list[Path]:
    roots = [MODEL_DIR, DATA_DIR, IMAGE_DIR, BASE_DIR, Path(__file__).resolve().parent]
    out = []
    for root in roots:
        for name in names:
            out.append(root / name)
    return out


@st.cache_resource
def load_models():
    baseline_model = None
    correction_model = None
    baseline_path = None
    correction_path = None

    for path in candidate_paths("baseline_model.pkl", "baseline_model.joblib"):
        if path.exists():
            baseline_model = joblib.load(path)
            baseline_path = path
            break

    for path in candidate_paths("correction_model.pkl", "correction_model.joblib"):
        if path.exists():
            correction_model = joblib.load(path)
            correction_path = path
            break

    return baseline_model, correction_model, baseline_path, correction_path


@st.cache_data
def load_weather_data():
    for path in candidate_paths("edmonton_weather_snow_2018_2025_clean.csv", "edmonton_weather.csv"):
        if path.exists():
            weather = pd.read_csv(path)
            break
    else:
        return None, None

    weather.columns = [str(c).strip() for c in weather.columns]

    if "date" not in weather.columns:
        for alt in ["Date", "datetime", "timestamp"]:
            if alt in weather.columns:
                weather = weather.rename(columns={alt: "date"})
                break

    rename_map = {}
    if "temperature" in weather.columns and "temperature_c" not in weather.columns:
        rename_map["temperature"] = "temperature_c"
    if "wind_speed" in weather.columns and "wind_speed_m_s" not in weather.columns:
        rename_map["wind_speed"] = "wind_speed_m_s"
    weather = weather.rename(columns=rename_map)

    required = ["date", "temperature_c", "snow_depth_cm", "cloud_cover", "wind_speed_m_s"]
    if not all(col in weather.columns for col in required):
        return None, None

    weather["date"] = pd.to_datetime(weather["date"], errors="coerce")
    weather = weather.dropna(subset=["date"]).copy()
    weather["year"] = weather["date"].dt.year
    weather["month"] = weather["date"].dt.month

    monthly_by_year = (
        weather.groupby(["year", "month"], as_index=False)[
            ["temperature_c", "snow_depth_cm", "cloud_cover", "wind_speed_m_s"]
        ]
        .mean()
        .sort_values(["year", "month"])
    )

    climatology = (
        weather.groupby("month", as_index=False)[
            ["temperature_c", "snow_depth_cm", "cloud_cover", "wind_speed_m_s"]
        ]
        .mean()
        .sort_values("month")
    )

    return monthly_by_year, climatology


@st.cache_data
def load_reference_dataset():
    for path in candidate_paths("sample_250000.csv", "sample_250000.xlsx"):
        if path.exists():
            if path.suffix.lower() == ".xlsx":
                df = pd.read_excel(path)
            else:
                df = pd.read_csv(path)
            df.columns = [str(c).strip() for c in df.columns]
            return df, path
    return None, None


@st.cache_data
def build_design_surface(reference_df: pd.DataFrame):
    if reference_df is None:
        return None
    needed = {"tilt", "azimuth", "power_per_kw"}
    if not needed.issubset(reference_df.columns):
        return None
    surface_df = (
        reference_df.groupby(["tilt", "azimuth"], as_index=False)["power_per_kw"]
        .mean()
        .sort_values(["tilt", "azimuth"])
    )
    return surface_df


def apply_plot_style(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.96)",
        font=dict(family="Segoe UI"),
        margin=dict(l=30, r=20, t=50, b=30),
    )
    return fig


@st.cache_data
def build_hourly_frame(sim_year: int) -> pd.DataFrame:
    hours = pd.date_range(start=f"{sim_year}-01-01", end=f"{sim_year}-12-31 23:00", freq="h")
    sim_df = pd.DataFrame({"datetime": hours})
    sim_df["hour"] = sim_df["datetime"].dt.hour
    sim_df["day_of_year"] = sim_df["datetime"].dt.dayofyear
    sim_df["month"] = sim_df["datetime"].dt.month
    sim_df["month_name"] = pd.Categorical(sim_df["datetime"].dt.strftime("%b"), categories=MONTH_ORDER, ordered=True)
    sim_df["quarter"] = sim_df["datetime"].dt.quarter
    sim_df["hour_sin"] = np.sin(2 * np.pi * sim_df["hour"] / 24)
    sim_df["hour_cos"] = np.cos(2 * np.pi * sim_df["hour"] / 24)
    sim_df["doy_sin"] = np.sin(2 * np.pi * sim_df["day_of_year"] / 365)
    sim_df["doy_cos"] = np.cos(2 * np.pi * sim_df["day_of_year"] / 365)
    return sim_df


def merge_weather(sim_df: pd.DataFrame, month_weather: pd.DataFrame) -> pd.DataFrame:
    merged = sim_df.merge(month_weather, on="month", how="left")
    for col in ["temperature_c", "snow_depth_cm", "cloud_cover", "wind_speed_m_s"]:
        if col not in merged.columns:
            merged[col] = 0.0
        merged[col] = pd.to_numeric(merged[col], errors="coerce").fillna(0.0)
    return merged


def simulate_output(
    tilt: float,
    azimuth: float,
    system_size_kw: float,
    sim_year: int,
    baseline_model,
    correction_model,
    climatology: pd.DataFrame | None,
    use_weather_adjustment: bool,
):
    sim_df = build_hourly_frame(sim_year).copy()
    sim_df["tilt"] = tilt
    sim_df["azimuth"] = azimuth

    if baseline_model is None:
        raise ValueError("Baseline model file not found.")

    sim_df["power_per_kw"] = baseline_model.predict(sim_df[BASELINE_FEATURES])
    sim_df["power_per_kw"] = np.clip(sim_df["power_per_kw"], a_min=0, a_max=None)
    sim_df["energy_kwh_baseline"] = (sim_df["power_per_kw"] / 1000.0) * system_size_kw

    if use_weather_adjustment and correction_model is not None and climatology is not None:
        sim_df = merge_weather(sim_df, climatology)
        sim_df["correction_factor"] = correction_model.predict(sim_df[CORRECTION_FEATURES])
        sim_df["correction_factor"] = np.clip(sim_df["correction_factor"], 0, 2)
        sim_df["energy_kwh"] = sim_df["energy_kwh_baseline"] * sim_df["correction_factor"]
        method = "Weather-adjusted model estimate"
    else:
        sim_df["correction_factor"] = 1.0
        sim_df["energy_kwh"] = sim_df["energy_kwh_baseline"]
        method = "Baseline model estimate"

    monthly = (
        sim_df.groupby(["month", "month_name", "quarter"], as_index=False)["energy_kwh"]
        .sum()
        .sort_values("month")
    )
    annual = float(monthly["energy_kwh"].sum())
    normalized = annual / system_size_kw if system_size_kw else 0.0
    return sim_df, monthly, annual, normalized, method


def simulate_weather_scenarios(
    tilt: float,
    azimuth: float,
    system_size_kw: float,
    sim_year: int,
    baseline_model,
    correction_model,
    monthly_weather_by_year: pd.DataFrame | None,
):
    if baseline_model is None or correction_model is None or monthly_weather_by_year is None:
        return None

    results = []
    month_weather_groups = dict(tuple(monthly_weather_by_year.groupby("year")))
    base_frame = build_hourly_frame(sim_year)

    for year_key, weather_year in month_weather_groups.items():
        sim_df = base_frame.copy()
        sim_df["tilt"] = tilt
        sim_df["azimuth"] = azimuth
        sim_df["power_per_kw"] = baseline_model.predict(sim_df[BASELINE_FEATURES])
        sim_df["power_per_kw"] = np.clip(sim_df["power_per_kw"], a_min=0, a_max=None)
        sim_df["energy_kwh_baseline"] = (sim_df["power_per_kw"] / 1000.0) * system_size_kw
        sim_df = merge_weather(sim_df, weather_year[["month", "temperature_c", "snow_depth_cm", "cloud_cover", "wind_speed_m_s"]])
        sim_df["correction_factor"] = correction_model.predict(sim_df[CORRECTION_FEATURES])
        sim_df["correction_factor"] = np.clip(sim_df["correction_factor"], 0, 2)
        sim_df["energy_kwh"] = sim_df["energy_kwh_baseline"] * sim_df["correction_factor"]
        annual = float(sim_df["energy_kwh"].sum())
        results.append({"weather_year": int(year_key), "annual_kwh": annual})

    if not results:
        return None

    dist = pd.DataFrame(results).sort_values("annual_kwh").reset_index(drop=True)
    low = float(dist["annual_kwh"].quantile(0.10))
    mid = float(dist["annual_kwh"].quantile(0.50))
    high = float(dist["annual_kwh"].quantile(0.90))
    return dist, low, mid, high


def fallback_lookup_mode(reference_df: pd.DataFrame, tilt: float, azimuth: float, system_size_kw: float):
    if reference_df is None:
        raise ValueError("No model or fallback dataset was found.")

    df = reference_df.copy()
    if "datetime" not in df.columns:
        raise ValueError("Fallback dataset is missing datetime.")

    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    df = df.dropna(subset=["datetime"]).copy()
    df["month"] = df["datetime"].dt.month
    df["month_name"] = pd.Categorical(df["datetime"].dt.strftime("%b"), categories=MONTH_ORDER, ordered=True)
    df["quarter"] = df["datetime"].dt.quarter

    subset = df[df["tilt"].between(tilt - 5, tilt + 5) & df["azimuth"].between(azimuth - 15, azimuth + 15)].copy()
    if subset.empty:
        subset = df.copy()

    monthly = (
        subset.groupby(["month", "month_name", "quarter"], as_index=False)["power_per_kw"]
        .mean()
        .sort_values("month")
    )
    monthly["energy_kwh"] = (monthly["power_per_kw"] / 1000.0) * system_size_kw * 24 * 30.4
    annual = float(monthly["energy_kwh"].sum())
    normalized = annual / system_size_kw if system_size_kw else 0.0
    return subset, monthly[["month", "month_name", "quarter", "energy_kwh"]], annual, normalized


def summarize_design(best_month, worst_month, annual_kwh, normalized_kwh, comparison_gap, comparison_pct, mode_label):
    direction = "higher" if comparison_gap >= 0 else "lower"
    return (
        f"<strong>Simulation Insight:</strong> This configuration is producing a <strong>{mode_label.lower()}</strong> of "
        f"<strong>{annual_kwh:,.0f} kWh per year</strong>, or about <strong>{normalized_kwh:,.0f} kWh per kW installed</strong>. "
        f"The strongest month is <strong>{best_month}</strong> and the weakest month is <strong>{worst_month}</strong>. "
        f"Compared with the reference design, output is <strong>{abs(comparison_gap):,.0f} kWh</strong> "
        f"(<strong>{abs(comparison_pct):.1f}%</strong>) {direction}."
    )


# =========================================================
# Load assets
# =========================================================
baseline_model, correction_model, baseline_path, correction_path = load_models()
weather_by_year, weather_climatology = load_weather_data()
reference_df, reference_path = load_reference_dataset()
surface_df = build_design_surface(reference_df)

image_path = IMAGE_DIR / "norquest.png"

# =========================================================
# Sidebar controls
# =========================================================
st.sidebar.header("Simulation Controls")

system_size = st.sidebar.slider("System Size (kW)", 1, 500, 10)
tilt = st.sidebar.slider("Tilt (degrees)", 0, 60, 30)
azimuth = st.sidebar.slider("Azimuth (degrees)", -180, 180, 180)
sim_year = st.sidebar.selectbox("Simulation Calendar", [2023, 2024, 2025, 2026], index=0)
use_weather_adjustment = st.sidebar.toggle(
    "Use weather-adjusted estimate",
    value=True,
    help="Applies the weather correction model when the correction model and Edmonton weather data are available.",
)

month_range = st.sidebar.slider("Month Range", 1, 12, (1, 12))
quarter_filter = st.sidebar.multiselect("Quarter Filter", [1, 2, 3, 4], default=[1, 2, 3, 4])
chart_type = st.sidebar.selectbox("Monthly Production Chart", ["Line", "Bar", "Area"])

st.sidebar.markdown("---")
st.sidebar.subheader("Reference Design")
baseline_tilt = st.sidebar.slider("Reference Tilt", 0, 60, 30)
baseline_azimuth = st.sidebar.slider("Reference Azimuth", -180, 180, 180)
show_distribution = st.sidebar.toggle("Show weather-year distribution", value=True)

# =========================================================
# Core simulation
# =========================================================
engine_label = "Fallback lookup estimate"
using_fallback = False
scenario_dist = None

try:
    sim_df, monthly_selected, annual_selected, normalized_selected, engine_label = simulate_output(
        tilt=tilt,
        azimuth=azimuth,
        system_size_kw=system_size,
        sim_year=sim_year,
        baseline_model=baseline_model,
        correction_model=correction_model,
        climatology=weather_climatology,
        use_weather_adjustment=use_weather_adjustment,
    )

    _, monthly_baseline, annual_baseline, normalized_baseline, _ = simulate_output(
        tilt=baseline_tilt,
        azimuth=baseline_azimuth,
        system_size_kw=system_size,
        sim_year=sim_year,
        baseline_model=baseline_model,
        correction_model=correction_model,
        climatology=weather_climatology,
        use_weather_adjustment=use_weather_adjustment,
    )

    if use_weather_adjustment and show_distribution:
        scenario_pack = simulate_weather_scenarios(
            tilt=tilt,
            azimuth=azimuth,
            system_size_kw=system_size,
            sim_year=sim_year,
            baseline_model=baseline_model,
            correction_model=correction_model,
            monthly_weather_by_year=weather_by_year,
        )
        if scenario_pack is not None:
            scenario_dist, low_energy, avg_energy, high_energy = scenario_pack
        else:
            low_energy = annual_selected * 0.90
            avg_energy = annual_selected
            high_energy = annual_selected * 1.10
    else:
        low_energy = annual_selected * 0.90
        avg_energy = annual_selected
        high_energy = annual_selected * 1.10

except Exception:
    using_fallback = True
    sim_df, monthly_selected, annual_selected, normalized_selected = fallback_lookup_mode(
        reference_df=reference_df,
        tilt=tilt,
        azimuth=azimuth,
        system_size_kw=system_size,
    )
    _, monthly_baseline, annual_baseline, normalized_baseline = fallback_lookup_mode(
        reference_df=reference_df,
        tilt=baseline_tilt,
        azimuth=baseline_azimuth,
        system_size_kw=system_size,
    )
    low_energy = annual_selected * 0.85
    avg_energy = annual_selected
    high_energy = annual_selected * 1.15

monthly_selected = monthly_selected[
    monthly_selected["month"].between(month_range[0], month_range[1])
    & monthly_selected["quarter"].isin(quarter_filter)
].copy()
monthly_baseline = monthly_baseline[
    monthly_baseline["month"].between(month_range[0], month_range[1])
    & monthly_baseline["quarter"].isin(quarter_filter)
].copy()

annual_selected_filtered = float(monthly_selected["energy_kwh"].sum())
annual_baseline_filtered = float(monthly_baseline["energy_kwh"].sum())
comparison_gap = annual_selected_filtered - annual_baseline_filtered
comparison_pct = (comparison_gap / annual_baseline_filtered * 100) if annual_baseline_filtered else 0.0
normalized_selected_filtered = annual_selected_filtered / system_size if system_size else 0.0
normalized_baseline_filtered = annual_baseline_filtered / system_size if system_size else 0.0

best_month = monthly_selected.loc[monthly_selected["energy_kwh"].idxmax(), "month_name"] if not monthly_selected.empty else "N/A"
worst_month = monthly_selected.loc[monthly_selected["energy_kwh"].idxmin(), "month_name"] if not monthly_selected.empty else "N/A"

insight_html = summarize_design(
    best_month=best_month,
    worst_month=worst_month,
    annual_kwh=annual_selected_filtered,
    normalized_kwh=normalized_selected_filtered,
    comparison_gap=comparison_gap,
    comparison_pct=comparison_pct,
    mode_label=engine_label,
)

# =========================================================
# Hero
# =========================================================
hero_left, hero_right = st.columns([1.4, 1], gap="large")

with hero_left:
    st.markdown(
        f"""
    <div class="hero-box">
        <div class="hero-label">Model-Based Solar Planning</div>
        <div class="hero-title">
            Solar <span class="hero-highlight">Simulation+</span>
        </div>
        <div class="hero-text">
            This page estimates annual and monthly production using the modelling workflow from the notebook rather than only averaging nearby design rows.
        </div>
        <div class="hero-text">
            Users can compare a selected design against a reference design, switch weather adjustment on or off, and review both total output and normalized output per kW installed.
        </div>
        <div class="hero-badge-wrap">
            <div class="hero-badge">{engine_label}</div>
            <div class="hero-chip">System Size</div>
            <div class="hero-chip">Tilt</div>
            <div class="hero-chip">Azimuth</div>
            <div class="hero-chip">kWh per kW</div>
            <div class="hero-chip">Reference Comparison</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with hero_right:
    if image_path.exists():
        st.image(str(image_path), use_container_width=True)
    else:
        st.info("Add norquest.png beside this page file to show the hero image.")

# =========================================================
# System status / assumptions
# =========================================================
status_cols = st.columns([1, 1], gap="large")
with status_cols[0]:
    if using_fallback:
        st.warning("Model files were not found, so this page is using the fallback lookup method from the dataset.")
    else:
        st.success("Model files detected. This page is using the notebook-aligned simulation flow.")

with status_cols[1]:
    details = []
    if baseline_path:
        details.append(f"Baseline model: {baseline_path.name}")
    if correction_path:
        details.append(f"Correction model: {correction_path.name}")
    if reference_path:
        details.append(f"Reference dataset: {reference_path.name}")
    if weather_by_year is not None:
        details.append(f"Weather years: {weather_by_year['year'].min()}–{weather_by_year['year'].max()}")
    st.caption(" | ".join(details) if details else "No supporting files were detected yet.")

# =========================================================
# KPI row
# =========================================================
st.markdown('<div class="section-heading">Simulation Summary</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">A quick summary of the current configuration, model method, and reference comparison.</div>',
    unsafe_allow_html=True,
)

k1, k2, k3, k4, k5, k6 = st.columns(6, gap="large")

with k1:
    st.markdown(
        f"""
    <div class="kpi-card">
        <div class="kpi-title">Method</div>
        <div class="kpi-value" style="font-size:1.0rem;">{engine_label}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with k2:
    st.markdown(
        f"""
    <div class="kpi-card">
        <div class="kpi-title">System Size</div>
        <div class="kpi-value">{system_size} kW</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with k3:
    st.markdown(
        f"""
    <div class="kpi-card">
        <div class="kpi-title">Tilt / Azimuth</div>
        <div class="kpi-value" style="font-size:1.15rem;">{tilt}° / {azimuth}°</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with k4:
    st.markdown(
        f"""
    <div class="kpi-card">
        <div class="kpi-title">Annual Output</div>
        <div class="kpi-value">{annual_selected_filtered:,.0f} kWh</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with k5:
    st.markdown(
        f"""
    <div class="kpi-card">
        <div class="kpi-title">Normalized Output</div>
        <div class="kpi-value">{normalized_selected_filtered:,.0f}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with k6:
    st.markdown(
        f"""
    <div class="kpi-card">
        <div class="kpi-title">Vs Reference</div>
        <div class="kpi-value" style="font-size:1.15rem;">{comparison_pct:+.1f}%</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.caption("Normalized output is shown as annual kWh per kW installed.")

# =========================================================
# Dynamic insight
# =========================================================
st.markdown(
    f"""
<div class="insight-box">
    {insight_html}
</div>
""",
    unsafe_allow_html=True,
)

# =========================================================
# Production range
# =========================================================
st.markdown('<div class="section-heading">Scenario Range</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4, gap="large")
with m1:
    st.markdown(
        f"""
    <div class="metric-strip">
        <div class="metric-label-dark">Low Scenario</div>
        <div class="metric-value-dark">{low_energy:,.0f} kWh</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
with m2:
    st.markdown(
        f"""
    <div class="metric-strip">
        <div class="metric-label-dark">Expected Scenario</div>
        <div class="metric-value-dark">{avg_energy:,.0f} kWh</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
with m3:
    st.markdown(
        f"""
    <div class="metric-strip">
        <div class="metric-label-dark">High Scenario</div>
        <div class="metric-value-dark">{high_energy:,.0f} kWh</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
with m4:
    st.markdown(
        f"""
    <div class="metric-strip">
        <div class="metric-label-dark">Peak Month</div>
        <div class="metric-value-dark">{best_month}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

if scenario_dist is not None:
    st.caption("Scenario range is based on historical Edmonton weather years passed through the weather-correction model.")
else:
    st.caption("Scenario range is using a simple spread because multi-year weather-model simulation files were not available.")

# =========================================================
# Production charts
# =========================================================
st.markdown('<div class="section-heading">Production Performance</div>', unsafe_allow_html=True)
left, right = st.columns(2, gap="large")

with left:
    st.markdown(
        """
    <div class="card">
        <div class="card-label">Monthly Output</div>
        <div class="card-title">Selected Design by Month</div>
    """,
        unsafe_allow_html=True,
    )

    monthly_chart_df = (
        monthly_selected.groupby("month", as_index=False, observed=True)["energy_kwh"]
        .sum()
    )

    # Force a clean 12-month structure
    monthly_chart_df = pd.DataFrame({"month": list(range(1, 13))}).merge(
        monthly_chart_df,
        on="month",
        how="left"
    )

    monthly_chart_df["energy_kwh"] = monthly_chart_df["energy_kwh"].fillna(0)

    monthly_chart_df["month_name"] = pd.Categorical(
        monthly_chart_df["month"].map({
            1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
            5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
            9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
        }),
        categories=MONTH_ORDER,
        ordered=True
    )

    if chart_type == "Line":
        fig_monthly = px.line(monthly_chart_df, x="month_name", y="energy_kwh", markers=True)
    elif chart_type == "Bar":
        fig_monthly = px.bar(monthly_chart_df, x="month_name", y="energy_kwh")
    else:
        fig_monthly = px.area(monthly_chart_df, x="month_name", y="energy_kwh")

    fig_monthly.update_layout(
        xaxis_title="Month",
        yaxis_title="Estimated Energy (kWh)"
    )
    fig_monthly.update_xaxes(categoryorder="array", categoryarray=MONTH_ORDER)

    apply_plot_style(fig_monthly)
    st.plotly_chart(fig_monthly, use_container_width=True)
    fig_monthly.update_layout(height=400)

    st.markdown(
        """
        <p class="small-note">
            This view shows monthly output from the selected model method, so design changes update the simulated production profile rather than only filtering nearby rows.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        """
    <div class="card">
        <div class="card-label">Reference Comparison</div>
        <div class="card-title">Selected vs Reference by Month</div>
    """,
        unsafe_allow_html=True,
    )

    # Clean monthly totals for selected design
    selected_compare = (
        monthly_selected.groupby("month", as_index=False, observed=True)["energy_kwh"]
        .sum()
        .rename(columns={"energy_kwh": "Selected Design"})
    )

    # Clean monthly totals for reference design
    baseline_compare = (
        monthly_baseline.groupby("month", as_index=False, observed=True)["energy_kwh"]
        .sum()
        .rename(columns={"energy_kwh": "Reference Design"})
    )

    # Build a clean 12-month calendar so the chart always has one row per month
    compare_monthly = pd.DataFrame({"month": list(range(1, 13))})

    compare_monthly = compare_monthly.merge(selected_compare, on="month", how="left")
    compare_monthly = compare_monthly.merge(baseline_compare, on="month", how="left")

    compare_monthly["Selected Design"] = compare_monthly["Selected Design"].fillna(0)
    compare_monthly["Reference Design"] = compare_monthly["Reference Design"].fillna(0)

    compare_monthly["month_name"] = pd.Categorical(
        compare_monthly["month"].map({
            1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
            5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
            9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
        }),
        categories=MONTH_ORDER,
        ordered=True
    )

    compare_long = compare_monthly.melt(
        id_vars=["month", "month_name"],
        value_vars=["Selected Design", "Reference Design"],
        var_name="Design",
        value_name="energy_kwh"
    )

    fig_compare_month = px.line(
        compare_long,
        x="month_name",
        y="energy_kwh",
        color="Design",
        markers=True
    )

    fig_compare_month.update_layout(
        xaxis_title="Month",
        yaxis_title="Estimated Energy (kWh)"
    )
    fig_compare_month.update_xaxes(categoryorder="array", categoryarray=MONTH_ORDER)

    apply_plot_style(fig_compare_month)
    st.plotly_chart(fig_compare_month, use_container_width=True)

    st.markdown(
        f"""
        <p class="small-note">
            The selected design is compared against a reference design of <strong>{baseline_tilt}° tilt</strong> and <strong>{baseline_azimuth}° azimuth</strong>.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )
# =========================================================
# Quarterly and distribution
# =========================================================
q1, q2 = st.columns(2, gap="large")

with q1:
    st.markdown(
        """
    <div class="card">
        <div class="card-label">Quarterly Output</div>
        <div class="card-title">Quarterly Production Summary</div>
    """,
        unsafe_allow_html=True,
    )

    q_selected = (
        monthly_selected.groupby("quarter", as_index=False, observed=True)["energy_kwh"]
        .sum()
        .sort_values("quarter")
    )
    q_selected["quarter_label"] = "Q" + q_selected["quarter"].astype(str)

    fig_quarter = px.bar(
        q_selected,
        x="quarter_label",
        y="energy_kwh",
        text="energy_kwh"
    )
    fig_quarter.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig_quarter.update_layout(
        xaxis_title="Quarter",
        yaxis_title="Estimated Energy (kWh)"
    )
    apply_plot_style(fig_quarter)
    st.plotly_chart(fig_quarter, use_container_width=True)

    st.markdown(
        """
        <p class="small-note">
            Quarterly output gives stakeholders a simpler seasonal summary without forcing them to read hourly or technical model detail.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with q2:
    st.markdown(
        """
    <div class="card">
        <div class="card-label">Weather-Year Spread</div>
        <div class="card-title">Annual Output Across Historical Weather Years</div>
    """,
        unsafe_allow_html=True,
    )

    if scenario_dist is not None and not scenario_dist.empty:
        fig_dist = px.bar(
            scenario_dist,
            x="weather_year",
            y="annual_kwh",
            text="annual_kwh"
        )
        fig_dist.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig_dist.update_layout(
            xaxis_title="Historical Weather Year",
            yaxis_title="Annual Energy (kWh)"
        )
        apply_plot_style(fig_dist)
        st.plotly_chart(fig_dist, use_container_width=True)

        st.markdown(
            """
            <p class="small-note">
                This distribution is a data-driven planning range built by running the same system design through different historical Edmonton weather patterns.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.info("Historical weather-year distribution is not available with the current files.")
        st.markdown(
            """
            <p class="small-note">
                Add the weather correction model and monthly weather history file to unlock the data-driven scenario distribution.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

# =========================================================
# Annual + normalized comparison
# =========================================================
st.markdown('<div class="section-heading">System Evaluation</div>', unsafe_allow_html=True)
a1, a2 = st.columns(2, gap="large")

with a1:
    st.markdown(
        """
    <div class="card">
        <div class="card-label">Annual Output</div>
        <div class="card-title">Total and Normalized Performance</div>
    """,
        unsafe_allow_html=True,
    )
    annual_df = pd.DataFrame(
        {
            "Metric": ["Annual kWh", "kWh per kW"],
            "Value": [annual_selected_filtered, normalized_selected_filtered],
        }
    )
    fig_annual = px.bar(annual_df, x="Metric", y="Value", text="Value")
    fig_annual.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig_annual.update_layout(xaxis_title="", yaxis_title="Value")
    apply_plot_style(fig_annual)
    st.plotly_chart(fig_annual, use_container_width=True)
    st.markdown(
        f"""
        <p class="small-note">
            The selected system is estimated to produce <strong>{annual_selected_filtered:,.0f} kWh</strong> annually, which equals <strong>{normalized_selected_filtered:,.0f} kWh per kW installed</strong>.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with a2:
    st.markdown(
        """
    <div class="card">
        <div class="card-label">Design Comparison</div>
        <div class="card-title">Selected vs Reference Annual Output</div>
    """,
        unsafe_allow_html=True,
    )
    compare_df = pd.DataFrame(
        {
            "Design": ["Selected Design", "Reference Design"],
            "Annual Energy (kWh)": [annual_selected_filtered, annual_baseline_filtered],
            "kWh per kW": [normalized_selected_filtered, normalized_baseline_filtered],
        }
    )
    fig_compare = px.bar(compare_df, x="Design", y="Annual Energy (kWh)", text="Annual Energy (kWh)", color="Design")
    fig_compare.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig_compare.update_layout(xaxis_title="", yaxis_title="Annual Energy (kWh)", showlegend=False)
    apply_plot_style(fig_compare)
    st.plotly_chart(fig_compare, use_container_width=True)
    st.markdown(
        f"""
        <p class="small-note">
            Annual output changes by <strong>{comparison_gap:,.0f} kWh</strong> versus the reference design, which is a relative change of <strong>{comparison_pct:+.1f}%</strong>.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# =========================================================
# Heatmap + tilt response
# =========================================================
st.markdown('<div class="section-heading">Design Patterns</div>', unsafe_allow_html=True)
h1, h2 = st.columns(2, gap="large")

with h1:
    st.markdown(
        """
    <div class="card">
        <div class="card-label">Design Surface</div>
        <div class="card-title">Tilt and Azimuth Performance Pattern</div>
    """,
        unsafe_allow_html=True,
    )
    if surface_df is not None and not surface_df.empty:
        heat_surface = surface_df.copy()
        heat_surface["annual_kwh_est"] = (heat_surface["power_per_kw"] / 1000.0) * system_size * 24 * 365
        pivot_df = heat_surface.pivot(index="tilt", columns="azimuth", values="annual_kwh_est")
        fig_heatmap = px.imshow(pivot_df, aspect="auto", labels=dict(x="Azimuth (degrees)", y="Tilt (degrees)", color="Annual kWh"))
        apply_plot_style(fig_heatmap)
        st.plotly_chart(fig_heatmap, use_container_width=True)
        st.markdown(
            """
            <p class="small-note">
                This surface helps explain where stronger and weaker design combinations tend to sit across the available simulated design space.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.info("A reference simulation dataset is needed to draw the tilt-azimuth surface.")
        st.markdown("</div>", unsafe_allow_html=True)

with h2:
    st.markdown(
        """
    <div class="card">
        <div class="card-label">Tilt Response</div>
        <div class="card-title">Annual Output by Tilt at Similar Azimuth</div>
    """,
        unsafe_allow_html=True,
    )
    if surface_df is not None and not surface_df.empty:
        tilt_df = surface_df[surface_df["azimuth"].between(azimuth - 15, azimuth + 15)].copy()
        tilt_df["annual_kwh_est"] = (tilt_df["power_per_kw"] / 1000.0) * system_size * 24 * 365
        tilt_summary = tilt_df.groupby("tilt", as_index=False)["annual_kwh_est"].mean().sort_values("tilt")
        fig_tilt = px.line(tilt_summary, x="tilt", y="annual_kwh_est", markers=True)
        fig_tilt.update_layout(xaxis_title="Tilt (degrees)", yaxis_title="Estimated Annual Energy (kWh)")
        apply_plot_style(fig_tilt)
        st.plotly_chart(fig_tilt, use_container_width=True)
        if not tilt_summary.empty:
            best_tilt = float(tilt_summary.loc[tilt_summary["annual_kwh_est"].idxmax(), "tilt"])
            best_energy = float(tilt_summary["annual_kwh_est"].max())
            st.markdown(
                f"""
                <p class="small-note">
                    Within the selected azimuth window, the strongest tilt in the reference design space is approximately <strong>{best_tilt:.0f}°</strong>, at about <strong>{best_energy:,.0f} kWh</strong> annually.
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("A reference simulation dataset is needed for tilt-response analysis.")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# Assumptions box (replaces data preview)
# =========================================================
st.markdown('<div class="section-heading">Planning Assumptions</div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="card">
    <div class="card-label">Assumptions Summary</div>
    <div class="card-title">How to Read This Page</div>
    <p class="small-note">
        This page is designed for planning and stakeholder discussion rather than engineering-grade site design. It compares design choices using a baseline production model, optionally applies a weather-correction layer, and then summarizes the result in monthly, quarterly, annual, and normalized forms.
    </p>
""",
    unsafe_allow_html=True,
)

assumptions = [
    f"Simulation calendar: {sim_year}",
    f"Selected design: {tilt}° tilt, {azimuth}° azimuth",
    f"Reference design: {baseline_tilt}° tilt, {baseline_azimuth}° azimuth",
    f"System size: {system_size} kW",
    f"Method: {engine_label}",
    "Normalized KPI: annual kWh per kW installed",
]
for item in assumptions:
    st.markdown(f'<span class="assumption-pill">{item}</span>', unsafe_allow_html=True)

st.markdown(
    """
    <p class="small-note" style="margin-top:1rem;">
        For the financial page, the most important outputs from this page are annual energy, monthly profile, normalized performance, and change versus the reference design.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# =========================================================
# Footer
# =========================================================
st.markdown(
    """
<div class="footer-note">
    <strong>Next step:</strong> Pass annual energy, normalized performance, and reference-design comparison into the Financial Impact page so stakeholders can connect output differences to savings and ROI.
</div>
""",
    unsafe_allow_html=True,
)
