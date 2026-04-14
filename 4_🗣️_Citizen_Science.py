"""Citizen Science — ASHRAE-55 surveys calibrate the Malta Tourism Climate Index."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from coolmap_branding import apply_branding, hero_banner, footer, COOLMAP_BLUE, COOLMAP_TEAL
from coolmap_data import survey_responses, THERMAL_SENSATION


st.set_page_config(page_title="Citizen Science · CoolMap Malta", page_icon="🗣️", layout="wide")
apply_branding()
hero_banner(
    "Citizen-Science Calibration",
    "Tourists and residents rate thermal comfort on location — training a Malta Tourism Climate Index",
    "ASHRAE-55 survey protocol · multilingual (EN · MT · IT · DE · FR) · ≥300 responses per pilot site",
)

st.markdown(
    """
The scientific difference between a generic UTCI map and **CoolMap Malta** is that
we calibrate the map against **real human thermal votes** from the people who
actually walk the streets — both **tourists** and **locals**.

- Protocol: ASHRAE-55 — 7-point thermal sensation (−3 Cold … +3 Hot), comfort vote, acceptability, preference.
- Deployed via a QR-landing micro-survey on site, multilingual, ~90 seconds to complete.
- Linked to the mobile-sensor UTCI reading at the exact time and place of the response.
- Responses weight the tourism-specific Tourism Climate Index lookup — closing the
  loop between physical sensor data and subjective human experience.
    """
)

st.divider()

# ─── Live survey mock ────────────────────────────────────────────────────────
st.subheader("Try the on-site micro-survey")

with st.form("survey_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        site = st.selectbox("Where are you?", [
            "Valletta — Republic St", "Sliema — Tower Rd", "St Julian's — Spinola Bay",
            "Valletta — Upper Barrakka", "Mdina — main gate"])
    with c2:
        role = st.selectbox("You are a…", ["Tourist", "Resident", "Outdoor worker", "Student", "Tour guide"])
    with c3:
        lang = st.selectbox("Language", ["EN", "MT", "IT", "DE", "FR"])

    st.markdown("**How does the temperature feel right now?** (ASHRAE-55 thermal sensation)")
    sensation = st.select_slider("",
        options=[-3, -2, -1, 0, 1, 2, 3],
        value=2,
        format_func=lambda v: f"{v:+d}  {THERMAL_SENSATION[v]}",
    )

    comfort = st.select_slider("How comfortable are you?",
        options=[-3, -2, -1, 0, 1, 2, 3],
        value=-1,
        format_func=lambda v: {
            -3: "Very uncomfortable", -2: "Uncomfortable", -1: "Slightly uncomfortable",
             0: "Neutral", 1: "Slightly comfortable", 2: "Comfortable", 3: "Very comfortable"
        }[v],
    )

    shade_adequacy = st.slider("How adequate is the shade here? (1–5)", 1, 5, 2)
    avoid = st.checkbox("I would avoid this spot during peak sun")

    submitted = st.form_submit_button("Submit response", type="primary")
    if submitted:
        st.success(
            f"Thanks! Response logged at **{site}** (role: {role}, lang: {lang}). "
            f"Thermal sensation {sensation:+d} · shade {shade_adequacy}/5. "
            "It will be joined to the matching UTCI sensor reading and feed the "
            "CoolMap Malta TCI calibration."
        )

st.divider()

# ─── Aggregated data ─────────────────────────────────────────────────────────
st.subheader("Aggregated responses — 220-respondent pilot simulation")

df = survey_responses()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Responses", f"{len(df)}")
k2.metric("Tourist share", f"{(df['role']=='Tourist').mean()*100:.0f} %")
k3.metric("Mean thermal sensation", f"{df['thermal_sensation'].mean():+.2f}")
k4.metric("Would-avoid rate", f"{df['would_avoid_again'].mean()*100:.0f} %")

c1, c2 = st.columns(2, gap="large")

with c1:
    counts = df.groupby(["site", "thermal_sensation_label"]).size().reset_index(name="n")
    order = ["Cold", "Cool", "Slightly cool", "Neutral", "Slightly warm", "Warm", "Hot"]
    counts["thermal_sensation_label"] = pd.Categorical(
        counts["thermal_sensation_label"], categories=order, ordered=True)
    fig = px.bar(counts, x="site", y="n", color="thermal_sensation_label",
                 category_orders={"thermal_sensation_label": order},
                 labels={"n": "Responses", "site": ""},
                 color_discrete_sequence=px.colors.diverging.RdBu_r[:7])
    fig.update_layout(title="Thermal sensation by site", height=380, margin=dict(t=50, b=30))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.scatter(df, x="utci_c", y="thermal_sensation", color="role",
                     opacity=0.7, trendline="lowess",
                     labels={"utci_c": "Measured UTCI (°C)",
                             "thermal_sensation": "Thermal sensation vote"})
    fig.update_layout(title="UTCI ↔ thermal-sensation calibration", height=380, margin=dict(t=50, b=30))
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ─── TCI calibration insight ─────────────────────────────────────────────────
st.subheader("Why this matters: Tourism Climate Index calibration")

a, b = st.columns([1.3, 1], gap="large")
with a:
    # delta between residents and tourists at the same UTCI
    by_role = df.groupby("role")["thermal_sensation"].mean().sort_values(ascending=False)
    st.markdown(
        "Residents and tourists **feel the same UTCI differently** — tourists, with "
        "less acclimatisation, report higher thermal-sensation votes at the same "
        "physical UTCI."
    )
    fig = px.bar(
        by_role.reset_index(),
        x="role", y="thermal_sensation",
        color="thermal_sensation", color_continuous_scale="RdBu_r",
        labels={"thermal_sensation": "Mean thermal sensation"},
    )
    fig.update_layout(height=320, margin=dict(t=30, b=30), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with b:
    st.markdown(
        """
**Malta Tourism Climate Index (Malta-TCI)**

By linking sensor UTCI to tourist-specific ASHRAE-55 votes, we produce a
tourism-native thermal comfort index:

- Scales *visitor discomfort* at a given UTCI ↑
- Down-weights residents' acclimatisation to hot conditions
- Feeds the Cool Route cost function directly
- Produces a destination-ready KPI: **"heat-comfort hours available to visitors"**
        """
    )
    st.info(
        "First-of-kind calibrated Tourism Climate Index for a Mediterranean island "
        "destination — defensible science with direct MTA uptake.",
        icon="🏆",
    )

footer()
