import pandas as pd

def create_telemetry_dataset(quali, export_folder):

    print("Creating telemetry dataset...")

    drivers = ["LEC", "SAI", "NOR", "VER"]

    all_telemetry = []

    for driver in drivers:

        lap = quali.laps.pick_drivers(driver).pick_fastest()

        if lap is None:
            continue

        telemetry = lap.get_car_data().add_distance()

        telemetry = telemetry[
            [
                "Distance",
                "Speed",
                "RPM",
                "Throttle",
                "Brake",
                "nGear"
            ]
        ].copy()

        telemetry["Driver"] = driver

        all_telemetry.append(telemetry)

    telemetry_df = pd.concat(all_telemetry)

    telemetry_df.to_csv(
        f"{export_folder}/telemetry.csv",
        index=False
    )

    print("Telemetry dataset exported!")