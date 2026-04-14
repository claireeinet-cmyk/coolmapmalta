"""CoolMap Malta — shared branding helpers."""

import streamlit as st


# Brand palette — Malta Mediterranean
COOLMAP_BLUE = "#0B6E99"          # Deep Mediterranean
COOLMAP_TEAL = "#14A5A5"          # Cool water
COOLMAP_SAND = "#F4E3C6"          # Limestone
COOLMAP_CORAL = "#E8704E"         # Heat / warning
COOLMAP_SHADE = "#2E4756"         # Deep shade / text
COOLMAP_LEAF = "#4A9A62"          # Urban greening

UTCI_COLORS = {
    "Strong cold":      "#053061",
    "Moderate cold":    "#2166AC",
    "Slight cold":      "#67A9CF",
    "No stress":        "#92C5DE",
    "Moderate heat":    "#FDDBC7",
    "Strong heat":      "#F4A582",
    "Very strong heat": "#D6604D",
    "Extreme heat":     "#B2182B",
}


def logo_svg() -> str:
    """Inline SVG logo — a sun half-sheltered by a palm/leaf."""
    return f"""
<svg viewBox="0 0 64 64" width="46" height="46" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{COOLMAP_BLUE}"/>
      <stop offset="100%" stop-color="{COOLMAP_TEAL}"/>
    </linearGradient>
  </defs>
  <circle cx="32" cy="32" r="30" fill="url(#sky)"/>
  <circle cx="42" cy="26" r="10" fill="#FFD66B"/>
  <path d="M8 44 Q20 30 32 44 T56 44 L56 56 L8 56 Z" fill="{COOLMAP_SAND}"/>
  <path d="M22 44 C 22 32, 32 28, 42 30 C 34 32, 28 38, 26 44 Z" fill="{COOLMAP_LEAF}"/>
  <path d="M14 44 C 14 36, 22 34, 30 36 C 22 38, 18 42, 18 44 Z" fill="{COOLMAP_LEAF}" opacity="0.8"/>
</svg>
""".strip()


def apply_branding():
    """Inject global styles."""
    st.markdown(
        f"""
<style>
:root {{
  --cm-blue: {COOLMAP_BLUE};
  --cm-teal: {COOLMAP_TEAL};
  --cm-sand: {COOLMAP_SAND};
  --cm-coral: {COOLMAP_CORAL};
  --cm-shade: {COOLMAP_SHADE};
  --cm-leaf: {COOLMAP_LEAF};
}}

/* headings */
h1, h2, h3 {{
  color: var(--cm-shade) !important;
  font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
}}
h1 {{ letter-spacing: -0.02em; }}

/* metrics */
[data-testid="stMetricValue"] {{
  color: var(--cm-blue) !important;
  font-weight: 700;
}}

/* primary buttons */
.stButton > button[kind="primary"],
.stDownloadButton > button[kind="primary"] {{
  background: var(--cm-blue);
  border-color: var(--cm-blue);
}}

/* sidebar tint */
section[data-testid="stSidebar"] {{
  background: linear-gradient(180deg, #F7FBFC 0%, #EAF3F5 100%);
}}

/* hero banner styles */
.cm-hero {{
  background: linear-gradient(135deg, {COOLMAP_BLUE} 0%, {COOLMAP_TEAL} 100%);
  color: #fff;
  padding: 1.6rem 1.8rem;
  border-radius: 14px;
  margin-bottom: 1.4rem;
  box-shadow: 0 10px 30px rgba(11, 110, 153, 0.18);
  display: flex;
  align-items: center;
  gap: 1.2rem;
}}
.cm-hero h1 {{
  color: #fff !important;
  margin: 0 0 .25rem 0 !important;
  font-size: 1.9rem !important;
}}
.cm-hero p {{
  color: #E8F4F7;
  margin: 0;
  font-size: 1.02rem;
}}
.cm-hero .cm-tagline {{
  margin-top: .45rem;
  font-size: 0.88rem;
  color: #CFE7EC;
  letter-spacing: 0.01em;
}}

/* pill */
.cm-pill {{
  display: inline-block;
  background: var(--cm-sand);
  color: var(--cm-shade);
  border-radius: 999px;
  padding: 3px 12px;
  font-size: 0.78rem;
  margin-right: 6px;
  font-weight: 600;
}}

/* info card */
.cm-card {{
  background: #fff;
  border: 1px solid #E3E9EC;
  border-left: 4px solid var(--cm-teal);
  border-radius: 10px;
  padding: 1rem 1.1rem;
  margin: .5rem 0;
}}

.cm-footer {{
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #E3E9EC;
  color: #7C8A91;
  font-size: 0.82rem;
  text-align: center;
}}
</style>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar header
    with st.sidebar:
        st.markdown(
            f"""
<div style="display:flex; align-items:center; gap:.6rem; padding:.3rem 0 .8rem 0;">
  {logo_svg()}
  <div>
    <div style="font-weight:700; font-size:1.1rem; color:{COOLMAP_SHADE};">CoolMap Malta</div>
    <div style="font-size:0.75rem; color:#5B6A71;">Thermal comfort intelligence</div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
<div style="font-size:0.78rem; color:#5B6A71; line-height:1.45;">
  Hosted by <b>K³ KlimaKarten</b><br/>
  Scientific lead: <b>Claire Gallacher</b><br/>
  <span style="color:#95A4AB;">Leibniz IÖR Dresden · Gallacher &amp; Boehnke, 2024</span>
</div>
""",
            unsafe_allow_html=True,
        )
        st.divider()


def hero_banner(title: str, subtitle: str, tagline: str = ""):
    st.markdown(
        f"""
<div class="cm-hero">
  <div>{logo_svg().replace('width="46" height="46"', 'width="72" height="72"')}</div>
  <div>
    <h1>{title}</h1>
    <p>{subtitle}</p>
    {f'<div class="cm-tagline">{tagline}</div>' if tagline else ''}
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )


def pill(text: str) -> str:
    return f'<span class="cm-pill">{text}</span>'


def footer():
    st.markdown(
        """
<div class="cm-footer">
  CoolMap Malta · Hosted by K³ KlimaKarten · F6S Application v6 · April 2026<br/>
  Category C — Technology and Digital Innovation for Urban Climate Adaptation ·
  Based on Gallacher &amp; Boehnke (2024), <i>Int. J. of Biometeorology</i>
</div>
        """,
        unsafe_allow_html=True,
    )


def utci_category(utci_c: float) -> str:
    """Map a UTCI value (°C) to a stress category per ISB/UTCI standard."""
    if utci_c < -13:
        return "Strong cold"
    if utci_c < 0:
        return "Moderate cold"
    if utci_c < 9:
        return "Slight cold"
    if utci_c <= 26:
        return "No stress"
    if utci_c <= 32:
        return "Moderate heat"
    if utci_c <= 38:
        return "Strong heat"
    if utci_c <= 46:
        return "Very strong heat"
    return "Extreme heat"
