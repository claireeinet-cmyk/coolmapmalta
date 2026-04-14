"""Tourist-facing Heat Map page — UTCI layer + POIs over Valletta/Sliema."""

import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium

from coolmap_branding import apply_branding, hero_banner, footer, UTCI_COLORS
from coolmap_data import tourist_pois, hotspot_grid, POI_CATEGORIES, VALLETTA


st.set_page_config(page_title="Heat Map · CoolMap Malta", page_icon="🗺️", layout="wide")
apply_branding()
hero_banner(
    "Malta Heat Comfort Map",
    "Pedestrian-level thermal comfort · live POI layer · ready for VisitMalta+",
    "UTCI at 10 m · calibrated against ASHRAE-55 surveys · refreshed hourly",
)

# ─── Controls ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.subheader("Layer controls")
    time_of_day = st.select_slider(
        "Time of day",
        options=["06:00", "09:00", "12:00", "15:00", "18:00", "21:00"],
        value="15:00",
    )
    scenario = st.radio("Heat scenario", ["Normal summer", "Heatwave (+4 °C)", "Autumn"], index=0)
    show_heat = st.checkbox("🔥 Thermal comfort heat layer", True)
    show_coolspots = st.checkbox("❄️ Consistent coldspots (bottom 5 % UTCI)", True)
    show_hotspots = st.checkbox("🌡️ Consistent hotspots (top 5 % UTCI)", True)

    st.divider()
    st.subheader("Tourist POIs")
    cats_on = {}
    for key, meta in POI_CATEGORIES.items():
        cats_on[key] = st.checkbox(f"{meta['icon']}  {meta['label']}", value=True, key=f"poi_{key}")

# ─── Map ─────────────────────────────────────────────────────────────────────
m = folium.Map(location=list(VALLETTA), zoom_start=14, tiles="cartodbpositron")

grid = hotspot_grid()
# scenario shifts
offset = {"Normal summer": 0.0, "Heatwave (+4 °C)": 4.0, "Autumn": -6.0}[scenario]
tod_offset = {"06:00": -9, "09:00": -3, "12:00": 2, "15:00": 4, "18:00": -1, "21:00": -6}[time_of_day]
grid = grid.copy()
grid["utci_c"] = grid["utci_c"] + offset + tod_offset

if show_heat:
    heat_data = [[r.lat, r.lon, max(0, r.utci_c - 20)] for r in grid.itertuples()]
    HeatMap(
        heat_data,
        radius=14,
        blur=22,
        min_opacity=0.35,
        gradient={0.0: "#2166AC", 0.35: "#FDDBC7", 0.6: "#F4A582", 0.85: "#D6604D", 1.0: "#67001F"},
    ).add_to(m)

if show_hotspots:
    for r in grid[grid["tier"] == "hotspot"].itertuples():
        folium.CircleMarker(
            location=[r.lat, r.lon], radius=4, color="#B2182B", weight=1,
            fill=True, fill_color="#B2182B", fill_opacity=0.6,
            popup=f"Hotspot · UTCI {r.utci_c:.1f} °C",
        ).add_to(m)

if show_coolspots:
    for r in grid[grid["tier"] == "coldspot"].itertuples():
        folium.CircleMarker(
            location=[r.lat, r.lon], radius=4, color="#2166AC", weight=1,
            fill=True, fill_color="#2166AC", fill_opacity=0.6,
            popup=f"Coldspot (protect) · UTCI {r.utci_c:.1f} °C",
        ).add_to(m)

pois = tourist_pois()
cluster = MarkerCluster(name="Tourist POIs").add_to(m)
for r in pois.itertuples():
    if not cats_on.get(r.category, True):
        continue
    folium.Marker(
        location=[r.lat, r.lon],
        popup=folium.Popup(
            f"<b>{r.icon} {r.name}</b><br/>"
            f"<span style='color:#555'>{r.label}</span><br/>"
            f"<span style='font-size:0.85em'>{r.note}</span>",
            max_width=280,
        ),
        tooltip=f"{r.icon} {r.name}",
        icon=folium.DivIcon(html=f"""
<div style="background:{r.color};color:#fff;border-radius:50%;width:30px;height:30px;
            display:flex;align-items:center;justify-content:center;font-size:15px;
            box-shadow:0 2px 6px rgba(0,0,0,0.25);">{r.icon}</div>
"""),
    ).add_to(cluster)

folium.LayerControl(collapsed=False).add_to(m)
st_folium(m, width=None, height=560, returned_objects=[])

# ─── Legend + summary ────────────────────────────────────────────────────────
c1, c2 = st.columns([2, 1], gap="large")
with c1:
    st.subheader("UTCI comfort classes on the map")
    cols = st.columns(len(UTCI_COLORS))
    for (name, color), col in zip(UTCI_COLORS.items(), cols):
        col.markdown(
            f"<div style='background:{color};color:#fff;border-radius:6px;"
            f"padding:6px 4px;text-align:center;font-size:0.78rem;'>{name}</div>",
            unsafe_allow_html=True,
        )
    st.caption("Scale per UTCI physiological equivalent temperature stress categories (Błażejczyk et al., 2013).")

with c2:
    pct_hot = (grid["tier"] == "hotspot").mean() * 100
    pct_cold = (grid["tier"] == "coldspot").mean() * 100
    st.metric("Area in consistent hotspots", f"{pct_hot:.1f} %", help="Top 5 % UTCI — greening / shade priority zones")
    st.metric("Area in consistent coldspots", f"{pct_cold:.1f} %", help="Bottom 5 % UTCI — protect and expand")
    st.metric("POIs in layer", int(sum(cats_on.values()) * 3))

st.divider()
st.markdown(
    "**Integration-ready.** The same tile layer publishes to any tourism app via the "
    "CoolMap REST API. The VisitMalta+ integration concept by K³ KlimaKarten (prototype: "
    "[cool-malta.lovable.app](https://cool-malta.lovable.app/)) consumes this feed as a "
    "heat-safety layer with water/shade/mist/AC/first-aid POIs."
)

footer()
