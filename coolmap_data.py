"""CoolMap Malta — mock data generators for the prototype.

All data here is synthetic but structured exactly like the real pipeline:
  - Tourist POIs (water, shade, mist, AC bus, first-aid, cool refuge)
  - Mobile UTCI sensor transects (morning/midday/afternoon/evening)
  - ASHRAE-55 citizen-science responses
  - Hotspot / coldspot tiles (top/bottom 5% UTCI)

When pipelines are wired into Copernicus, Sentinel-2 and OSM, these loaders
are replaced 1:1 with real data sources.
"""

from __future__ import annotations
import math
import numpy as np
import pandas as pd


VALLETTA = (35.8989, 14.5146)
SLIEMA = (35.9121, 14.5028)
ST_JULIANS = (35.9177, 14.4825)
MDINA = (35.8856, 14.4025)


# ---------------------------------------------------------------------------
# Tourist POIs
# ---------------------------------------------------------------------------
POI_CATEGORIES = {
    "water":     {"label": "Water dispenser",   "icon": "💧", "color": "#0B6E99"},
    "shade":     {"label": "Shaded refuge",     "icon": "🌳", "color": "#4A9A62"},
    "mist":      {"label": "Mist station",      "icon": "💨", "color": "#14A5A5"},
    "ac_bus":    {"label": "AC bus stop",       "icon": "🚌", "color": "#7753C3"},
    "first_aid": {"label": "First-aid point",   "icon": "➕", "color": "#C73A3A"},
    "refuge":    {"label": "Cool indoor refuge","icon": "🏛️", "color": "#B47636"},
}


def tourist_pois() -> pd.DataFrame:
    """Synthetic but believable tourist POIs across Valletta, Sliema, St Julian's."""
    rows = [
        # VALLETTA ------------------------------------------------------------
        ("water",     "Triton Fountain",            35.8985, 14.5109, "City Gate — drinking fountain, refilled hourly"),
        ("water",     "Upper Barrakka Gardens",     35.8951, 14.5136, "Shaded public fountain with harbour views"),
        ("shade",     "Hastings Gardens",           35.8999, 14.5088, "Dense ficus canopy — top-decile cool refuge"),
        ("shade",     "St John's Co-Cathedral Sq.", 35.8978, 14.5122, "Colonnaded arcade — deep afternoon shade"),
        ("mist",      "Republic Square",            35.8982, 14.5139, "Solar-powered mist arch — pilot install"),
        ("ac_bus",    "Valletta Terminus A12",      35.8968, 14.5104, "Air-conditioned waiting hall + shaded benches"),
        ("first_aid", "Blue Light Pharmacy Station",35.8975, 14.5128, "Public first-aid point — heatwave SOP trained"),
        ("refuge",    "National Library",           35.8979, 14.5129, "Cool indoor refuge — free entry on code-red days"),
        ("refuge",    "St. James Cavalier",         35.8954, 14.5115, "AC cultural centre — designated cooling hub"),

        # SLIEMA --------------------------------------------------------------
        ("water",     "Sliema Ferries Fountain",    35.9138, 14.5047, "Promenade water point, 24/7"),
        ("water",     "Tigné Point Square",         35.9152, 14.5105, "Refill station near MTA kiosk"),
        ("shade",     "Independence Gardens",       35.9173, 14.4998, "Mature pines — verified coldspot in 2025 transects"),
        ("shade",     "Tower Road Pergola",         35.9129, 14.5058, "Pergola with vines — micro-shade corridor"),
        ("mist",      "Exiles Promenade Mist Arch", 35.9146, 14.4976, "Pilot mist installation, solar-run"),
        ("ac_bus",    "Ferries Interchange",        35.9132, 14.5041, "AC waiting hall, shaded queue"),
        ("first_aid", "Sliema Police Station",      35.9129, 14.5022, "Heat SOS point during peak hours"),
        ("refuge",    "Tigné Point Mall",           35.9160, 14.5113, "Shaded atrium — AC public access"),

        # ST JULIAN'S ---------------------------------------------------------
        ("water",     "Spinola Bay Fountain",       35.9199, 14.4875, "Public fountain, lit evenings"),
        ("shade",     "Balluta Square Trees",       35.9155, 14.4948, "Palm corridor — partial shade on west side"),
        ("mist",      "Paceville Cool Point",       35.9235, 14.4903, "Evening-only mist installation"),
        ("ac_bus",    "St Julian's Post Office",    35.9186, 14.4894, "AC waiting, screen with CoolMap layer"),
        ("first_aid", "Paceville Health Post",      35.9226, 14.4901, "Weekend + heatwave first aid"),
    ]
    df = pd.DataFrame(rows, columns=["category", "name", "lat", "lon", "note"])
    df["icon"] = df["category"].map(lambda c: POI_CATEGORIES[c]["icon"])
    df["color"] = df["category"].map(lambda c: POI_CATEGORIES[c]["color"])
    df["label"] = df["category"].map(lambda c: POI_CATEGORIES[c]["label"])
    return df


# ---------------------------------------------------------------------------
# Mobile UTCI sensor transect (synthetic)
# ---------------------------------------------------------------------------
def sensor_transect(time_of_day: str = "midday", seed: int = 42) -> pd.DataFrame:
    """A Valletta pedestrian transect of the <€500 mobile UTCI device.

    time_of_day ∈ {"morning","midday","afternoon","evening"}.
    """
    rng = np.random.default_rng(seed + hash(time_of_day) % 1000)

    # path: Triton Fountain → Republic Street → Barrakka → back to St Julian's
    waypoints = [
        (35.8985, 14.5109),  # Triton
        (35.8982, 14.5138),  # Republic Sq
        (35.8974, 14.5138),  # mid Republic St
        (35.8963, 14.5129),  # Lower Republic
        (35.8951, 14.5136),  # Upper Barrakka
        (35.8960, 14.5105),  # waterfront promenade
        (35.8995, 14.5085),  # Hastings Gardens
    ]
    pts = []
    for i in range(len(waypoints) - 1):
        a, b = waypoints[i], waypoints[i + 1]
        for t in np.linspace(0, 1, 18):
            pts.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))

    lats, lons = zip(*pts)
    n = len(lats)

    base = {"morning": 24.0, "midday": 36.5, "afternoon": 41.0, "evening": 29.5}[time_of_day]
    amp = {"morning": 4.0, "midday": 7.5, "afternoon": 8.5, "evening": 5.0}[time_of_day]

    # simulate shade/open variation along the path
    structure = amp * np.sin(np.linspace(0, 3 * math.pi, n) + rng.uniform(0, 0.8))
    noise = rng.normal(0, 0.7, n)
    utci = base + structure + noise

    # air temp, mrt, wind, rh
    t_air = base - 2.5 + 0.4 * structure + rng.normal(0, 0.4, n)
    t_mrt = utci + 6 + rng.normal(0, 1.5, n)
    wind = np.clip(1.5 + 0.8 * rng.standard_normal(n), 0.2, 6.0)
    rh = np.clip(55 + 10 * rng.standard_normal(n), 28, 85)

    df = pd.DataFrame({
        "seq": np.arange(n),
        "lat": lats,
        "lon": lons,
        "t_air_c": t_air.round(2),
        "t_mrt_c": t_mrt.round(2),
        "wind_ms": wind.round(2),
        "rh_pct": rh.round(1),
        "utci_c": utci.round(2),
        "time_of_day": time_of_day,
    })
    return df


def all_transects() -> pd.DataFrame:
    parts = [sensor_transect(t, seed=s) for s, t in enumerate(
        ["morning", "midday", "afternoon", "evening"], start=1)]
    return pd.concat(parts, ignore_index=True)


# ---------------------------------------------------------------------------
# Citizen-science survey data (ASHRAE-55 style)
# ---------------------------------------------------------------------------
THERMAL_SENSATION = {
    -3: "Cold",
    -2: "Cool",
    -1: "Slightly cool",
     0: "Neutral",
     1: "Slightly warm",
     2: "Warm",
     3: "Hot",
}


def survey_responses(n: int = 220, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    sites = ["Valletta — Republic St", "Sliema — Tower Rd", "St Julian's — Spinola Bay",
             "Valletta — Upper Barrakka", "Mdina — main gate"]
    roles = ["Tourist", "Resident", "Outdoor worker", "Student", "Tour guide"]
    rows = []
    for _ in range(n):
        site = rng.choice(sites)
        role = rng.choice(roles, p=[0.48, 0.30, 0.08, 0.09, 0.05])
        # physiological UTCI "ground-truth" at site+time
        base_u = rng.normal(35, 4)
        sensation_score = int(np.clip(np.round((base_u - 22) / 3.2 + rng.normal(0, 0.6)), -3, 3))
        comfort = int(np.clip(-abs(sensation_score) + rng.integers(-1, 2), -3, 3))
        rows.append({
            "site": site,
            "role": role,
            "age_group": rng.choice(["<25", "25–40", "40–60", "60+"], p=[0.25, 0.40, 0.25, 0.10]),
            "utci_c": round(base_u, 1),
            "thermal_sensation": sensation_score,
            "thermal_sensation_label": THERMAL_SENSATION[sensation_score],
            "comfort_vote": comfort,
            "perceived_shade_adequacy": int(rng.integers(1, 6)),  # 1–5
            "would_avoid_again": rng.choice([True, False], p=[0.42, 0.58]),
            "language": rng.choice(["EN", "MT", "IT", "DE", "FR"], p=[0.55, 0.18, 0.1, 0.1, 0.07]),
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Hotspot / coldspot grid for planner dashboard
# ---------------------------------------------------------------------------
def hotspot_grid(center=VALLETTA, n_lat: int = 22, n_lon: int = 22, seed: int = 11) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    lat0, lon0 = center
    # ~1 km box
    lats = np.linspace(lat0 - 0.010, lat0 + 0.010, n_lat)
    lons = np.linspace(lon0 - 0.012, lon0 + 0.012, n_lon)
    rows = []
    for lat in lats:
        for lon in lons:
            # a noisy gradient with some built-up hot cores
            core1 = math.exp(-((lat - 35.898) ** 2 + (lon - 14.513) ** 2) * 1e4) * 6
            core2 = math.exp(-((lat - 35.905) ** 2 + (lon - 14.520) ** 2) * 1e4) * 3.5
            cool = math.exp(-((lat - 35.8995) ** 2 + (lon - 14.5088) ** 2) * 1e4) * 5  # Hastings
            utci = 33.5 + core1 + core2 - cool + rng.normal(0, 0.8)
            rows.append({"lat": lat, "lon": lon, "utci_c": round(utci, 2)})
    df = pd.DataFrame(rows)
    lo, hi = df["utci_c"].quantile([0.05, 0.95])
    df["tier"] = np.where(df["utci_c"] >= hi, "hotspot",
                  np.where(df["utci_c"] <= lo, "coldspot", "normal"))
    return df
