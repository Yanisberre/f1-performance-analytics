import fastf1
import pandas as pd
import os

from scripts.config import (
    YEAR,
    GRAND_PRIX,
    QUALI_SESSION,
    RACE_SESSION,
    EXPORT_FOLDER
)

from scripts.telemetry import create_telemetry_dataset

# =====================================
# CREATE EXPORT FOLDER
# =====================================

os.makedirs(EXPORT_FOLDER, exist_ok=True)

# =====================================
# CACHE
# =====================================

fastf1.Cache.enable_cache("cache")

print("===================================")
print("F1 DATA PIPELINE STARTED")
print("===================================")

print(f"Season: {YEAR}")
print(f"Grand Prix: {GRAND_PRIX}")

# =====================================
# LOAD SESSIONS
# =====================================

print("Loading Qualifying session...")
quali = fastf1.get_session(
    YEAR,
    GRAND_PRIX,
    QUALI_SESSION
)
quali.load()

print("Loading Race session...")
race = fastf1.get_session(
    YEAR,
    GRAND_PRIX,
    RACE_SESSION
)
race.load()

# =====================================
# TELEMETRY DATASET
# =====================================

create_telemetry_dataset(
    quali,
    EXPORT_FOLDER
)

# =====================================
# LAP TIMES DATASET
# =====================================

print("Creating lap times dataset...")

results = quali.results.copy()

lap_times_df = results[
    [
        "Abbreviation",
        "FullName",
        "TeamName",
        "Position",
        "Q1",
        "Q2",
        "Q3"
    ]
]

lap_times_df.columns = [
    "Driver",
    "FullName",
    "Team",
    "Position",
    "Q1",
    "Q2",
    "Q3"
]

lap_times_df.to_csv(
    f"{EXPORT_FOLDER}/lap_times.csv",
    index=False
)

print("Lap times dataset exported!")

# =====================================
# SECTOR TIMES DATASET
# =====================================

print("Creating sector times dataset...")

fastest_laps = []

for driver in quali.drivers:

    laps = quali.laps.pick_drivers(driver)

    if laps.empty:
        continue

    fastest = laps.pick_fastest()

    if fastest is None:
        continue

    fastest_laps.append({
        "Driver": driver,
        "Sector1Time": fastest["Sector1Time"],
        "Sector2Time": fastest["Sector2Time"],
        "Sector3Time": fastest["Sector3Time"]
    })

sector_times_df = pd.DataFrame(fastest_laps)

sector_times_df.to_csv(
    f"{EXPORT_FOLDER}/sector_times.csv",
    index=False
)

print("Sector times dataset exported!")

# =====================================
# TYRES DATASET
# =====================================

print("Creating tyres dataset...")

tyres_df = race.laps[
    [
        "Driver",
        "Team",
        "LapNumber",
        "Compound",
        "TyreLife",
        "Stint",
        "LapTime"
    ]
].copy()

tyres_df = tyres_df.dropna(subset=["LapTime"])

tyres_df.to_csv(
    f"{EXPORT_FOLDER}/tyres_strategy.csv",
    index=False
)

print("Tyres dataset exported!")

# =====================================
# WEATHER DATASET
# =====================================

print("Creating weather dataset...")

weather_df = race.weather_data.copy()

weather_df = weather_df[
    [
        "Time",
        "AirTemp",
        "Humidity",
        "Pressure",
        "Rainfall",
        "TrackTemp",
        "WindDirection",
        "WindSpeed"
    ]
]

weather_df.to_csv(
    f"{EXPORT_FOLDER}/weather.csv",
    index=False
)

print("Weather dataset exported!")

# =====================================
# RACE PACE DATASET
# =====================================

print("Creating race pace dataset...")

race_pace_df = race.laps[
    [
        "Driver",
        "Team",
        "LapNumber",
        "LapTime",
        "Compound",
        "TyreLife",
        "Stint",
        "Position"
    ]
].copy()

race_pace_df = race_pace_df.dropna(subset=["LapTime"])

race_pace_df["LapTimeSeconds"] = (
    race_pace_df["LapTime"]
    .dt.total_seconds()
)

race_pace_df.to_csv(
    f"{EXPORT_FOLDER}/race_pace.csv",
    index=False
)

print("Race pace dataset exported!")

# =====================================
# DRIVER KPI DATASET
# =====================================

print("Creating driver KPI dataset...")

kpi_data = []

for driver in race.drivers:

    laps = race.laps.pick_drivers(driver)

    if laps.empty:
        continue

    fastest_lap = laps.pick_fastest()

    if fastest_lap is None:
        continue

    telemetry = fastest_lap.get_car_data()

    if telemetry.empty:
        continue

    kpi_data.append({
        "Driver": fastest_lap["Driver"],
        "Team": fastest_lap["Team"],
        "BestLapTime": fastest_lap["LapTime"].total_seconds(),
        "MaxSpeed": telemetry["Speed"].max(),
        "AverageSpeed": telemetry["Speed"].mean()
    })

kpi_df = pd.DataFrame(kpi_data)

kpi_df = kpi_df.sort_values(
    by="BestLapTime"
)

kpi_df.to_csv(
    f"{EXPORT_FOLDER}/driver_kpis.csv",
    index=False
)

print("Driver KPI dataset exported!")

# =====================================
# TRACK DOMINANCE DATASET
# =====================================

print("Creating track dominance dataset...")

dominance_data = []

for driver in ["LEC", "SAI", "NOR", "VER"]:

    lap = quali.laps.pick_drivers(driver).pick_fastest()

    if lap is None:
        continue

    telemetry = lap.get_car_data().add_distance()

    telemetry = telemetry[
        [
            "Distance",
            "Speed"
        ]
    ].copy()

    telemetry["Driver"] = driver

    dominance_data.append(telemetry)

dominance_df = pd.concat(dominance_data)

dominance_df.to_csv(
    f"{EXPORT_FOLDER}/track_dominance.csv",
    index=False
)

print("Track dominance dataset exported!")

# =====================================
# SESSION METADATA
# =====================================

print("Creating session metadata dataset...")

session_info = {
    "Year": YEAR,
    "GrandPrix": GRAND_PRIX,
    "QualifyingSession": QUALI_SESSION,
    "RaceSession": RACE_SESSION,
    "Circuit": race.event['Location'],
    "Country": race.event['Country'],
    "EventName": race.event['EventName'],
    "EventDate": race.event['EventDate']
}

session_df = pd.DataFrame([session_info])

session_df.to_csv(
    f"{EXPORT_FOLDER}/session_metadata.csv",
    index=False
)

print("Session metadata exported!")

# =====================================
# PIPELINE END
# =====================================

print("===================================")
print("ALL DATASETS EXPORTED SUCCESSFULLY")
print("===================================")