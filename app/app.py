import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import plotly.express as px
import plotly.graph_objects as go
import requests

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Rainfall Analysis & Crop Recommendation",
    page_icon="🌧️",
    layout="wide"
)

# ── Title ──────────────────────────────────────────────────────────────────────
st.title("🌧️ Rainfall Analysis & Crop Recommendation System")
st.markdown("---")

st.markdown(
    """
    <style>
    .summary-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 20px;
        margin-top: 16px;
    }
    .summary-card {
        background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 18px;
        padding: 26px 24px;
        color: #ffffff;
        box-shadow: 0 20px 40px rgba(15, 23, 42, 0.22);
        min-height: 170px;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    .summary-card h3 {
        margin: 0 0 10px;
        font-size: 1.05rem;
        color: #9ca3af;
        font-weight: 700;
    }
    .summary-card p {
        margin: 0;
        font-size: 2.4rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        line-height: 1.05;
    }
    .summary-card .card-note {
        margin-top: 12px;
        color: #cbd5e1;
        font-size: 0.95rem;
        line-height: 1.4;
    }
    .summary-crops-card {
        background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
        border: 1px solid rgba(249, 115, 22, 0.25);
        border-radius: 24px;
        padding: 22px 26px;
        color: #e2e8f0;
        box-shadow: 0 24px 48px rgba(15, 23, 42, 0.18);
        margin-top: 18px;
        line-height: 1.6;
    }
    .summary-crops-card strong {
        display: block;
        color: #cbd5e1;
        margin-bottom: 10px;
        font-size: 1rem;
        letter-spacing: 0.01em;
    }
    .summary-crops-card code {
        background: rgba(229, 231, 235, 0.08);
        color: #a7f3d0;
        padding: 10px 14px;
        border-radius: 14px;
        font-size: 0.98rem;
        display: inline-block;
        white-space: normal;
        line-height: 1.8;
    }
    .map-card {
        background: #0f172a;
        border: 1px solid rgba(148, 163, 184, 0.16);
        border-radius: 20px;
        padding: 16px;
        box-shadow: 0 20px 40px rgba(15, 23, 42, 0.16);
        margin-top: 120px;
    }
    .map-card h4 {
        color: #f8fafc;
        margin: 0 0 10px;
        font-size: 1rem;
        letter-spacing: 0.01em;
    }
    .map-spacer {
        height: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Load data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    crop_df = pd.read_csv(os.path.join(base_dir, "step8_v2_final.csv"))
    rainfall_df = pd.read_csv(os.path.join(base_dir, "rainfall_long.csv"))
    return crop_df, rainfall_df

crop_df, rainfall_df = load_data()

# Correct month ordering
MONTH_ORDER = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
               "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

# ── Sidebar — State Selection ──────────────────────────────────────────────────
st.sidebar.header("🗺️ Select a State")
states      = sorted(crop_df["STATE"].unique())
selected    = st.sidebar.selectbox("Choose State", states)

st.sidebar.markdown("---")
st.sidebar.info(
    "**ℹ️ About CV (Coefficient of Variation)**\n\n"
    "High CV indicates **unpredictable rainfall** and higher agricultural risk. "
    "States with CV > 40 are classified as High Risk, making reliable "
    "rain-fed farming difficult."
)

# ── Get selected state data ────────────────────────────────────────────────────
state_row  = crop_df[crop_df["STATE"] == selected].iloc[0]
mean_rain  = state_row["MEAN_RAINFALL"]
cv         = state_row["CV"]
risk       = state_row["RISK_LEVEL"]
crops      = state_row["SUITABLE_CROPS"]
crop_count = int(state_row["CROP_COUNT"])

# Risk badge color
risk_color = {"Low Risk": "🟢", "Moderate Risk": "🟠", "High Risk": "🔴"}
risk_icon  = risk_color.get(risk, "⚪")

# ── India state boundary map data ──────────────────────────────────────────────
@st.cache_data
def load_india_geojson():
    url = "https://raw.githubusercontent.com/geohacker/india/master/state/india_state.geojson"
    return requests.get(url).json()

GEOJSON = load_india_geojson()

STATE_NAME_MAP = {
    "ANDAMAN & NICOBAR ISLANDS": "Andaman and Nicobar",
    "ARUNACHAL PRADESH": "Arunachal Pradesh",
    "ASSAM & MEGHALAYA": "Assam",
    "BIHAR": "Bihar",
    "CHHATTISGARH": "Chhattisgarh",
    "COASTAL ANDHRA PRADESH": "Andhra Pradesh",
    "COASTAL KARNATAKA": "Karnataka",
    "EAST MADHYA PRADESH": "Madhya Pradesh",
    "EAST RAJASTHAN": "Rajasthan",
    "EAST UTTAR PRADESH": "Uttar Pradesh",
    "GANGETIC WEST BENGAL": "West Bengal",
    "GUJARAT REGION": "Gujarat",
    "HARYANA DELHI & CHANDIGARH": "Haryana",
    "HIMACHAL PRADESH": "Himachal Pradesh",
    "JAMMU & KASHMIR": "Jammu and Kashmir",
    "JHARKHAND": "Jharkhand",
    "KERALA": "Kerala",
    "KONKAN & GOA": "Goa",
    "LAKSHADWEEP": "Lakshadweep",
    "MADHYA MAHARASHTRA": "Maharashtra",
    "MARATHWADA": "Maharashtra",
    "NAGA MANI MIZO TRIPURA": "Tripura",
    "NORTH INTERIOR KARNATAKA": "Karnataka",
    "ORISSA": "Odisha",
    "PUNJAB": "Punjab",
    "RAYALSEEMA": "Andhra Pradesh",
    "SAURASHTRA & KUTCH": "Gujarat",
    "SOUTH INTERIOR KARNATAKA": "Karnataka",
    "SUB HIMALAYAN WEST BENGAL & SIKKIM": "West Bengal",
    "TAMIL NADU": "Tamil Nadu",
    "TELANGANA": "Telangana",
    "UTTARAKHAND": "Uttarakhand",
    "VIDARBHA": "Maharashtra",
    "WEST MADHYA PRADESH": "Madhya Pradesh",
    "WEST RAJASTHAN": "Rajasthan",
    "WEST UTTAR PRADESH": "Uttar Pradesh",
}

map_df = crop_df.copy()
map_df["FEATURE_NAME"] = map_df["STATE"].map(STATE_NAME_MAP)
map_df = map_df.dropna(subset=["FEATURE_NAME"]).drop_duplicates(subset=["FEATURE_NAME"], keep="first")


def simplify_coords(coords, max_points=35):
    if isinstance(coords[0][0], (int, float)):
        if len(coords) <= max_points:
            return coords
        step = max(1, len(coords) // max_points)
        simplified = coords[::step]
        if simplified[-1] != coords[-1]:
            simplified.append(coords[-1])
        return simplified
    return [simplify_coords(c, max_points) for c in coords]


def simplify_geojson(geojson, max_points=35):
    simplified = {"type": geojson["type"], "features": []}
    for feature in geojson["features"]:
        simplified["features"].append({
            "type": feature["type"],
            "properties": feature["properties"],
            "geometry": {
                "type": feature["geometry"]["type"],
                "coordinates": simplify_coords(feature["geometry"]["coordinates"], max_points),
            },
        })
    return simplified

SIMPLIFIED_GEOJSON = simplify_geojson(GEOJSON, max_points=25)
map_df["MAP_FILL"] = "India"

fig_map = px.choropleth(
    map_df,
    geojson=SIMPLIFIED_GEOJSON,
    locations="FEATURE_NAME",
    featureidkey="properties.NAME_1",
    color="MAP_FILL",
    color_discrete_map={"India": "#ffffff"},
    labels={"FEATURE_NAME": "State"},
)
fig_map.update_traces(marker_line_width=0.8, marker_line_color="#999999", selector=dict(type="choropleth"))
selected_feature = STATE_NAME_MAP.get(selected)
if selected_feature:
    fig_map.add_trace(
        go.Choropleth(
            geojson=SIMPLIFIED_GEOJSON,
            locations=[selected_feature],
            z=[1],
            featureidkey="properties.NAME_1",
            showscale=False,
            colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"],],
            marker_line_color="black",
            marker_line_width=3,
            hoverinfo="skip",
            showlegend=False,
        )
    )
fig_map.update_geos(
    fitbounds="locations",
    visible=False,
)
fig_map.update_layout(
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    geo=dict(bgcolor="#ffffff"),
    margin=dict(l=0, r=0, t=0, b=0),
    height=300,
    autosize=True,
    showlegend=False,
)
main_left, main_right = st.columns([2.4, 1])
with main_left:
    st.subheader(f"📍 Selected State — {selected}")
    st.write("Explore rainfall patterns and crop suitability for the selected state.")

    st.markdown(
        f"""
        <div class='summary-grid'>
            <div class='summary-card'>
                <h3>💧 Mean Rainfall</h3>
                <p>{mean_rain:.1f} mm</p>
            </div>
            <div class='summary-card'>
                <h3>📊 CV (%)</h3>
                <p>{cv:.2f}%</p>
            </div>
            <div class='summary-card'>
                <h3>⚠️ Risk Level</h3>
                <p>{risk_icon} {risk}</p>
            </div>
            <div class='summary-card'>
                <h3>🌾 Crop Count</h3>
                <p>{crop_count}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class='summary-crops-card'>
            <strong>Suitable Crops:</strong>
            <code>{crops}</code>
        </div>
        """,
        unsafe_allow_html=True,
    )

with main_right:
    st.markdown(
        """
        <div class='map-card'>
            <h4>State Map</h4>
        </div>
        <div class='map-spacer'></div>
        """,
        unsafe_allow_html=True,
    )
    st.plotly_chart(fig_map, use_container_width=True, height=420)

st.markdown("---")

# ── Section 2: Monthly Rainfall Chart ─────────────────────────────────────────
st.subheader(f"📅 Average Monthly Rainfall — {selected}")

state_monthly = rainfall_df[rainfall_df["STATE"] == selected].copy()
monthly_avg   = (
    state_monthly.groupby("MONTH")["RAINFALL"]
    .mean()
    .reindex(MONTH_ORDER)
    .reset_index()
)
monthly_avg.columns = ["MONTH", "AVG_RAINFALL"]

fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(monthly_avg["MONTH"], monthly_avg["AVG_RAINFALL"],
         color="#1565C0", linewidth=2.5, marker="o", markersize=6)
ax1.fill_between(monthly_avg["MONTH"], monthly_avg["AVG_RAINFALL"],
                 alpha=0.15, color="#1565C0")
ax1.set_title(f"Average Monthly Rainfall — {selected}", fontsize=13, fontweight="bold")
ax1.set_xlabel("Month", fontsize=11)
ax1.set_ylabel("Average Rainfall (mm)", fontsize=11)
ax1.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
st.pyplot(fig1)
plt.close()

st.markdown("---")

# ── Section 3 & 4: Side-by-side comparison charts ────────────────────────────
st.subheader("📊 State Comparison Charts")

col_left, col_right = st.columns(2)

# ── Chart A: Mean Rainfall — highlight selected state ─────────────────────────
with col_left:
    st.markdown("**Mean Annual Rainfall by State**")

    bar_colors_rain = [
        "#1565C0" if s == selected else "#CFD8DC"
        for s in crop_df["STATE"]
    ]

    fig2, ax2 = plt.subplots(figsize=(10, 5), constrained_layout=True)
    ax2.bar(crop_df["STATE"], crop_df["MEAN_RAINFALL"],
            color=bar_colors_rain, edgecolor="white", linewidth=0.5)
    ax2.set_title("Average Rainfall by State", fontsize=12, fontweight="bold")
    ax2.set_xlabel("State", fontsize=10)
    ax2.set_ylabel("Mean Rainfall (mm)", fontsize=10)
    ax2.tick_params(axis="x", rotation=90, labelsize=7)

    # Custom legend
    legend_handles = [
        mpatches.Patch(facecolor="#1565C0", label=f"Selected: {selected}"),
        mpatches.Patch(facecolor="#CFD8DC", label="Other States"),
    ]
    ax2.legend(handles=legend_handles, fontsize=9, loc="upper right")
    st.pyplot(fig2)
    plt.close()

# ── Chart B: Crop Count — colored by risk level ───────────────────────────────
with col_right:
    st.markdown("**Number of Suitable Crops by State**")

    risk_palette = {
        "Low Risk":      "#4CAF50",
        "Moderate Risk": "#FFA726",
        "High Risk":     "#EF5350",
    }

    crop_order = crop_df.sort_values("CROP_COUNT", ascending=True).reset_index(drop=True)
    bar_colors_crop = crop_order["RISK_LEVEL"].map(risk_palette)

    fig3, ax3 = plt.subplots(figsize=(10, 5), constrained_layout=True)
    bars = ax3.bar(crop_order["STATE"], crop_order["CROP_COUNT"],
                   color=bar_colors_crop, edgecolor="white", linewidth=0.5)

    # Highlight the selected state border
    if selected in crop_order["STATE"].values:
        selected_idx = int(crop_order[crop_order["STATE"] == selected].index[0])
        bars[selected_idx].set_edgecolor("#000000")
        bars[selected_idx].set_linewidth(1.2)

    # Count label on each bar
    for bar, count in zip(bars, crop_order["CROP_COUNT"]):
        ax3.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.08,
                 str(count), ha="center", va="bottom", fontsize=7)

    ax3.set_title(
        "Number of Suitable Crops per State (16 Crops | Colored by Risk Level)",
        fontsize=12, fontweight="bold"
    )
    ax3.set_xlabel("State", fontsize=10)
    ax3.set_ylabel("Number of Suitable Crops", fontsize=10)
    ax3.set_xticks(range(len(crop_order)))
    ax3.set_xticklabels(crop_order["STATE"], rotation=90, fontsize=7)
    ax3.set_ylim(0, int(crop_order["CROP_COUNT"].max()) + 1.0)
    ax3.set_yticks(range(0, int(crop_order["CROP_COUNT"].max()) + 2))
    ax3.margins(y=0)

    legend_patches = [
        mpatches.Patch(facecolor="#4CAF50", label="Low Risk  (CV < 20)"),
        mpatches.Patch(facecolor="#FFA726", label="Moderate Risk  (20–40)"),
        mpatches.Patch(facecolor="#EF5350", label="High Risk  (CV > 40)"),
    ]
    ax3.legend(handles=legend_patches, fontsize=9, loc="upper left")
    st.pyplot(fig3)
    plt.close()

st.markdown("---")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.caption(
    "📚 Crop water requirements sourced from FAO Irrigation & Drainage Papers "
    "No. 24 (1977), No. 33 (1979), and No. 56 (1998). "
    "Rainfall data covers Indian states from 1901 onwards."
)