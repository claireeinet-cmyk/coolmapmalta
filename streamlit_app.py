"""
CoolMap Malta — Streamlit mockup
================================
Hyperlocal pedestrian-level thermal comfort intelligence for Malta.
Hosted by K³ KlimaKarten · Scientific lead: Claire Gallacher (Leibniz IÖR Dresden)
Based on Gallacher & Boehnke (2024) · UTCI + Tourism Climate Index + Citizen Science

This is a vibe-coded mockup extending the `urban-heat-adapt` methodology
to the Malta context for the UN Tourism National Innovation Challenge.
"""

import streamlit as st
from coolmap_branding import apply_branding, hero_banner, footer, logo_svg


st.set_page_config(
    page_title="CoolMap Malta",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_branding()

# ────────────────────────────────────────────────────────────────────────────
# Hero
# ────────────────────────────────────────────────────────────────────────────
hero_banner(
    title="CoolMap Malta",
    subtitle="Hyperlocal thermal comfort intelligence for a climate-resilient island destination",
    tagline="Peer-reviewed science · Mobile sensors · Citizen calibration · Tourist-ready WebGIS",
)

st.markdown(
    """
Welcome to the **CoolMap Malta** preview — a green-technology intelligence layer
for urban heat mitigation, built for the **UN Tourism National Innovation Challenge · Malta**.

We turn open geospatial data, a **<€500 mobile UTCI sensor kit**, and **citizen-science surveys**
into **street-level thermal comfort intelligence** — calibrated to Malta's limestone, sea-breeze
and tourism context, and ready to plug into **VisitMalta+** and council planning workflows.
    """
)

# ────────────────────────────────────────────────────────────────────────────
# Three-up pitch
# ────────────────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("#### 🧭 For Visitors")
    st.markdown(
        "- **Cool Routes** between attractions\n"
        "- **Water dispensers**, shaded spots, mist stations\n"
        "- **AC bus stops** & first-aid points\n"
        "- **Heat-risk alerts** during heatwaves\n"
        "- VisitMalta+ integration layer"
    )

with col2:
    st.markdown("#### 🏛️ For Councils & MTA")
    st.markdown(
        "- **Hotspot / coldspot** prioritisation\n"
        "- Evidence-based **greening decisions**\n"
        "- **Shade & cooling** infrastructure siting\n"
        "- **KPI dashboards** aligned with SDG 3/11/13\n"
        "- K³ planner platform — proven across 7 German municipalities"
    )

with col3:
    st.markdown("#### 🔬 For Science")
    st.markdown(
        "- Peer-reviewed **UTCI methodology** (Gallacher & Boehnke, 2024)\n"
        "- Open-hardware **<€500 mobile sensor**\n"
        "- **ASHRAE-55** citizen-science surveys\n"
        "- **Malta-specific TCI** calibration\n"
        "- Open data on Zenodo, open code on GitHub"
    )

st.divider()

# ────────────────────────────────────────────────────────────────────────────
# What's different
# ────────────────────────────────────────────────────────────────────────────
st.subheader("What makes CoolMap Malta different?")

a, b = st.columns([1, 1], gap="large")
with a:
    st.markdown(
        """
**Most urban-heat tools stop at land-surface temperature.**
Satellite LST is easy to compute but has almost nothing to do with what a tourist
on a Valletta pavement actually feels at midday.
        """
    )
    st.markdown(
        """
**CoolMap Malta closes that gap with three ingredients the market does not deliver together:**

1. **Peer-reviewed UTCI methodology** (Gallacher & Boehnke, 2024) — pedestrian-level
   Universal Thermal Climate Index mapping validated against 300+ ASHRAE-55 responses
   in Dresden.
2. **Open-hardware mobile sensor kit** (<€500/unit) — Mediterranean-calibrated for
   Malta's limestone surfaces, sea-breeze corridors and high solar angles.
3. **Citizen-science calibration** — tourists *and* residents rate thermal comfort on
   location, training a **Malta-specific Tourism Climate Index** that reflects real
   human experience, not just meteorological averages.
        """
    )

with b:
    st.info(
        "**The wedge:** hyperlocal UTCI + routing granularity + participatory validation — "
        "built on a published, reproducible scientific foundation and a proven municipal "
        "delivery platform (K³ × LANUK NRW, 7 pilots).",
        icon="🎯",
    )
    st.markdown(
        """
**Category C fit (Terms of Reference):**

> *"Smart sensors to monitor temperature and humidity in real time, digital platforms
> for urban planning, data-driven tools to design cooler tourism routes."*

CoolMap Malta delivers all three — directly.
        """
    )

st.divider()

# ────────────────────────────────────────────────────────────────────────────
# Navigation hint
# ────────────────────────────────────────────────────────────────────────────
st.subheader("Explore the mockup")

n1, n2, n3 = st.columns(3, gap="large")
with n1:
    st.markdown(
        "**🗺️  Heat Map** — live thermal comfort layer for Valletta & Sliema with "
        "tourist POIs (water, shade, mist, AC bus, first-aid)."
    )
    st.markdown(
        "**🚶  Cool Routes** — pedestrian routing that prefers shaded, cooler streets."
    )
with n2:
    st.markdown(
        "**📡  Mobile Sensors** — live view of the <€500 UTCI device: transects, "
        "calibration curves, benchmarking against reference instruments."
    )
    st.markdown(
        "**🗣️  Citizen Science** — ASHRAE-55 tourist & resident surveys feeding the "
        "Malta Tourism Climate Index calibration."
    )
with n3:
    st.markdown(
        "**📊  Planner Dashboard** — top/bottom 5% UTCI hotspots, greening "
        "prioritisation, SDG KPIs for councils and MTA."
    )
    st.markdown(
        "**📚  Methodology** — the full scientific pipeline from sensor → survey → "
        "map, with citations."
    )

st.caption("👉 Use the sidebar to navigate between pages.")

footer()
