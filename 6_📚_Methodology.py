"""Methodology — the scientific pipeline, with citations."""

import streamlit as st
from coolmap_branding import apply_branding, hero_banner, footer


st.set_page_config(page_title="Methodology · CoolMap Malta", page_icon="📚", layout="wide")
apply_branding()
hero_banner(
    "Methodology",
    "Peer-reviewed · reproducible · open — sensor → survey → map",
    "Gallacher & Boehnke (2024), Int. J. of Biometeorology · open data on Zenodo · open code on GitHub",
)

st.markdown(
    """
CoolMap Malta implements the scientific pipeline published in:

> **Gallacher, C. & Boehnke, D. (2024).** *Pedestrian thermal comfort mapping for
> evidence-based urban planning.* International Journal of Biometeorology.

The methodology has five stages, each implemented in the open `urban-heat-adapt`
codebase and transferred to Malta in this mockup.
    """
)

st.divider()

stages = [
    {
        "n": "1",
        "title": "Satellite & open-data baseline",
        "body": """
Copernicus **land surface temperature**, Sentinel-2 **NDVI** (vegetation),
**OSM** POIs, **building footprints**, and a **digital elevation model** define
the physical baseline at 10 m resolution. This is the layer most existing
"urban heat" tools stop at — for us it is only the input.
        """,
    },
    {
        "n": "2",
        "title": "Mobile UTCI sensor campaigns",
        "body": """
Claire Gallacher's **<€500 open-hardware UTCI device** measures air temperature,
globe temperature, humidity and wind at pedestrian level along fixed transects.
Campaigns run at **morning / midday / afternoon / evening** on clear-sky days —
the standard protocol from Gallacher & Boehnke (2024). For Malta, the device
is calibrated to local limestone surfaces, sea-breeze corridors and high solar
angles.
        """,
    },
    {
        "n": "3",
        "title": "Citizen-science ASHRAE-55 surveys",
        "body": """
At each transect waypoint, tourists and residents complete a short
**ASHRAE-55 thermal-comfort questionnaire** (7-point thermal sensation,
comfort, acceptability, preference) via a multilingual QR survey. The
subjective votes are joined to the sensor UTCI reading at the same
place and time.
        """,
    },
    {
        "n": "4",
        "title": "Malta Tourism Climate Index calibration",
        "body": """
The joint dataset (sensor UTCI × ASHRAE-55 votes) fits a **Malta-specific
Tourism Climate Index** that reflects how visitors — with less local
acclimatisation — actually feel thermal stress at a given UTCI. This is the
scientific innovation on top of the Dresden methodology: a tourism-native
thermal-comfort index, calibrated per destination.
        """,
    },
    {
        "n": "5",
        "title": "Hotspot / coldspot publication + cool routes",
        "body": """
The calibrated UTCI raster is classified into **top 5 % hotspots** (intervention
targets) and **bottom 5 % coldspots** (protection targets), surfaced via the
K³ KlimaKarten planner dashboard for councils and MTA. In parallel, the raster
becomes an edge-weight for **pedestrian routing** — producing Cool Routes for
the tourist-facing WebGIS and VisitMalta+ integration.
        """,
    },
]

for s in stages:
    st.markdown(
        f"""
<div class="cm-card">
  <div style="display:flex; align-items:baseline; gap:.8rem;">
    <div style="background:#0B6E99;color:#fff;border-radius:50%;
                width:36px;height:36px;display:flex;align-items:center;
                justify-content:center;font-weight:700;">{s['n']}</div>
    <h3 style="margin:0;">{s['title']}</h3>
  </div>
  <div style="margin-top:.4rem; color:#2E4756;">{s['body']}</div>
</div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

st.subheader("What Malta gets specifically")

c1, c2 = st.columns(2, gap="large")
with c1:
    st.markdown(
        """
**Mediterranean-calibrated UTCI layer**
- Accounts for limestone albedo and heat-retention
- Accounts for sea-breeze ventilation corridors
- High-solar-angle adjustments vs. Central European baseline
- Validated against Maltese ASHRAE-55 responses (tourist & resident)
        """
    )
with c2:
    st.markdown(
        """
**Transferable to other Mediterranean destinations**
- Cyprus · Sicily · the Balearics · Crete · Canary Islands · coastal Portugal
- Same methodology, localised calibration only
- Interreg Euro-MED and EU LIFE Adaptation fit
- Proven scale path from Dresden (Claire) → NRW 7 municipalities (K³) → Malta
        """
    )

st.divider()

st.subheader("Citations & open resources")

st.markdown(
    """
- **Gallacher, C. & Boehnke, D. (2024).** *Pedestrian thermal comfort mapping for
  evidence-based urban planning.* International Journal of Biometeorology.
- **Błażejczyk, K. et al. (2013).** *Comparison of UTCI to selected thermal indices.*
  International Journal of Biometeorology 56: 515–535.
- **ASHRAE Standard 55-2023.** *Thermal Environmental Conditions for Human Occupancy.*
- **Gallacher, C. et al.** *Entwicklung von Planungshilfen für Klimaschutz und
  Klimaanpassung in der räumlichen Gesamtplanung mittels Fernerkundung —
  Abschlussbericht* (Hessen Ministry).
- **Gallacher, C. et al.** *A collaborative approach for the identification of
  thermal hot-spots: from remote sensing data to urban planning interventions.*
- **urban-heat-adapt** open-source codebase:
  [github.com/claireeinet-cmyk/urban-heat-adapt](https://github.com/claireeinet-cmyk/urban-heat-adapt)
- **Dresden case-study dataset** — open-access on Zenodo (ground-truth transect + survey data).
- **Open-hardware <€500 UTCI device** — Zenodo hardware documentation, CERN-OHL licence.
    """
)

footer()
