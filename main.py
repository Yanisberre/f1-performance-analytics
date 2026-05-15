import fastf1
import pandas as pd

# Cache
fastf1.Cache.enable_cache("cache")

print("Loading session...")

# Charger session Monaco 2024 Race
session = fastf1.get_session(2024, "Monaco", "R")
session.load()

# Infos session
session_info = {
    "Year": 2024,
    "GrandPrix": "Monaco",
    "Session": "Race",
    "Circuit": session.event['Location'],
    "Country": session.event['Country'],
    "EventName": session.event['EventName'],
    "EventDate": session.event['EventDate']
}

# DataFrame
session_df = pd.DataFrame([session_info])

# Export CSV
session_df.to_csv(
    "data/session_metadata.csv",
    index=False
)

print("Session metadata exported!")

print(session_df)