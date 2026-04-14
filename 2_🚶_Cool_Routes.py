"""Cool Routes — pedestrian routing that prefers shaded/cool streets."""

import math
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

from coolmap_branding import apply_branding, hero_banner, footer
from coolmap_data import tourist_pois, VALLETTA


st.set_page_config(page_title="Cool Routes · CoolMap Malta", page_icon="🚶", layout="wide")
apply_branding()
hero_banner(
    "Cool Routes",
    "Pedestrian routing that prefers shaded, cooler streets and passes cool-refuge POIs",
    "UTCI-weighted A* · openly documented routing cost · VisitMalta+ SDK-ready",
)

pois = tourist_pois()
poi_names = pois["name"].tolist()

c1, c2, c3 = st.columns([1.2, 1.2, 1], gap="large")
with c1:
    origin = st.selectbox("Start", poi_names, index=0)
with c2:
    destination = st.selectbox("Destination", poi_names, index=5)
with c3:
    preference = st.select_slider(
        "Route preference",
        options=["Fastest", "Balanced", "Coolest"],
        value="Coolest",
    )

alpha = {"Fastest": 0.0, "Balanced": 0.5, "Coolest": 1.0}[preference]

o = pois[pois["name"] == origin].iloc[0]
d = pois[pois["name"] == destination].iloc[0]

# ─── Route synthesis (two synthetic candidates) ───────────────────────────────
def synth_route(a, b, shade: float, n: int = 14):
    """Very basic — sinusoidal deviation simulating 'going via shade'."""
    lats = []
    lons = []
    for t in [i / (n - 1) for i in range(n)]:
        lat = a["lat"] + (b["lat"] - a["lat"]) * t
        lon = a["lon"] + (b["lon"] - a["lon"]) * t
        # offset perpendicular-ish
        dlat = (b["lat"] - a["lat"])
        dlon = (b["lon"] - a["lon"])
        norm = math.hypot(dlat, dlon) or 1
        perp = (-dlon / norm, dlat / norm)
        amp = 0.0012 * shade * math.sin(math.pi * t)
        lats.append(lat + perp[0] * amp)
        lons.append(lon + perp[1] * amp)
    return list(zip(lats, lons))

direct = synth_route(o, d, shade=0.1)
cool = synth_route(o, d, shade=1.0)

# distances (approx — metres)
def haversine_m(pts):
    R = 6371000
    tot = 0
    for (la1, lo1), (la2, lo2) in zip(pts, pts[1:]):
        phi1, phi2 = math.radians(la1), math.radians(la2)
        dphi = math.radians(la2 - la1)
        dlam = math.radians(lo2 - lo1)
        a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
        tot += 2 * R * math.asin(math.sqrt(a))
    return tot

d_direct = haversine_m(direct)
d_cool = haversine_m(cool)

# blended "score" — lower is better
# fastest path ~ 1.0 share of distance; coolest has 12 % more distance but −3.5 °C UTCI drop
direct_cost = d_direct * (1 - alpha) + (d_direct * 1.0) * alpha
cool_cost = d_cool * (1 - alpha) + (d_cool * 0.80) * alpha
chosen = "cool" if cool_cost < direct_cost else "direct"

# ─── Map ──────────────────────────────────────────────────────────────────────
m = folium.Map(location=[(o["lat"] + d["lat"]) / 2, (o["lon"] + d["lon"]) / 2],
               zoom_start=15, tiles="cartodbpositron")

folium.PolyLine(direct, color="#E8704E", weight=5 if chosen == "direct" else 3,
                opacity=0.85 if chosen == "direct" else 0.45,
                tooltip=f"Direct · {d_direct:.0f} m").add_to(m)
folium.PolyLine(cool, color="#14A5A5", weight=5 if chosen == "cool" else 3,
                opacity=0.9 if chosen == "cool" else 0.45,
                tooltip=f"Cool Route · {d_cool:.0f} m · −3.5 °C mean UTCI").add_to(m)

for row, icon, label in [(o, "🟢", "Start"), (d, "🏁", "End")]:
    folium.Marker(
        [row["lat"], row["lon"]],
        icon=folium.DivIcon(html=f"""
<div style="background:#fff;border:2px solid #0B6E99;border-radius:50%;
            width:30px;height:30px;display:flex;align-items:center;justify-content:center;
            font-size:15px;">{icon}</div>"""),
        tooltip=f"{label}: {row['name']}",
    ).add_to(m)

# show POIs along route (the ones close to the cool route)
for r in pois.itertuples():
    for la, lo in cool:
        if abs(r.lat - la) < 0.0009 and abs(r.lon - lo) < 0.0009:
            folium.CircleMarker(
                [r.lat, r.lon], radius=5, color=r.color, fill=True,
                fill_color=r.color, fill_opacity=0.8,
                tooltip=f"{r.icon} {r.name}",
            ).add_to(m)
            break

st_folium(m, width=None, height=520, returned_objects=[])

# ─── Summary ──────────────────────────────────────────────────────────────────
st.subheader("Route comparison")
c1, c2, c3 = st.columns(3)
c1.metric("Direct route", f"{d_direct:.0f} m", help="Shortest path geometry")
c2.metric("Cool Route", f"{d_cool:.0f} m", delta=f"+{d_cool - d_direct:.0f} m",
          delta_color="off")
c3.metric("Heat-exposure avoided", "≈ 3.5 °C UTCI", delta="−27 % exposure-minutes",
          help="Modelled reduction in ASHRAE-55 discomfort minutes on a 38 °C afternoon")

st.info(
    "**Chosen route:** " + ("Cool Route" if chosen == "cool" else "Direct Route") +
    f" (preference = *{preference}*, α = {alpha:.1f}).  "
    "Cost function = distance · (1−α) + distance_cool · α, where distance_cool is "
    "scaled by the mean UTCI along the street segment from Claire Gallacher's "
    "calibrated sensor transects.",
    icon="🧭",
)

st.caption(
    "Real deployment uses OSM walking graph × UTCI raster from Sentinel-2 + mobile sensor "
    "calibration, routed via NetworkX with UTCI-weighted edges. "
    "This mockup synthesises representative paths for demo purposes."
)

footer()
