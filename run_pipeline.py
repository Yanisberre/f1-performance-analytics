import fastf1
import pandas as pd
from pathlib import Path

from scripts.config import (
    SEASONS,
    GRANDS_PRIX,
    SESSION_TYPE
)

# =====================================
# ENABLE CACHE
# =====================================

fastf1.Cache.enable_cache("cache")

# =====================================
# CREATE BASE DATA FOLDER
# =====================================

base_data_path = Path("data")
base_data_path.mkdir(exist_ok=True)

# =====================================
# CONSOLIDATED DATASET LIST
# =====================================

all_race_pace = []

print("===================================")
print("MULTI-SEASON F1 PIPELINE STARTED")
print("===================================")

# =====================================
# MAIN LOOP
# =====================================

for season in SEASONS:

    for grand_prix in GRANDS_PRIX:

        print(
            f"\nLoading {season} "
            f"{grand_prix}..."
        )

        try:

            session = fastf1.get_session(
                season,
                grand_prix,
                SESSION_TYPE
            )

            session.load()

            laps = session.laps

            # =====================================
            # CREATE DATASET
            # =====================================

            race_pace_df = laps[
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

            race_pace_df = race_pace_df.dropna(
                subset=["LapTime"]
            )

            race_pace_df["LapTimeSeconds"] = (
                race_pace_df["LapTime"]
                .dt.total_seconds()
            )

            # =====================================
            # ADD METADATA
            # =====================================

            race_pace_df["Season"] = season
            race_pace_df["GrandPrix"] = grand_prix

            # =====================================
            # ADD TO CONSOLIDATED LIST
            # =====================================

            all_race_pace.append(race_pace_df)

            # =====================================
            # CREATE OUTPUT FOLDER
            # =====================================

            output_folder = (
                base_data_path /
                f"{season}_{grand_prix}"
            )

            output_folder.mkdir(exist_ok=True)

            # =====================================
            # EXPORT INDIVIDUAL CSV
            # =====================================

            race_pace_df.to_csv(
                output_folder / "race_pace.csv",
                index=False
            )

            print(
                f"Dataset exported for "
                f"{season} {grand_prix}"
            )

        except Exception as e:

            print(
                f"Error for "
                f"{season} {grand_prix}: "
                f"{e}"
            )

# =====================================
# CONSOLIDATED EXPORT
# =====================================

print("\nCreating consolidated dataset...")

consolidated_df = pd.concat(
    all_race_pace,
    ignore_index=True
)

consolidated_df.to_csv(
    "data/consolidated_race_pace.csv",
    index=False
)

print("Consolidated dataset exported!")

print("\n===================================")
print("PIPELINE FINISHED")
print("===================================")