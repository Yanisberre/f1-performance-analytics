# F1 Performance Analytics

A scalable Formula 1 analytics pipeline built with Python, FastF1 and Power BI.

---

# Project Overview

This project aims to collect, transform and visualize Formula 1 telemetry and race data for performance analysis.

The pipeline automatically generates datasets that can be used in Power BI dashboards for:

- Telemetry analysis
- Driver comparison
- Race pace analysis
- Tyre strategy analysis
- Sector dominance
- Weather impact
- Performance KPIs

---

# Tech Stack

- Python
- FastF1
- Pandas
- Power BI
- Git
- GitHub

---

# Project Structure

```bash
f1-performance-analytics/
│
├── cache/
├── dashboards/
├── data/
├── notebooks/
├── scripts/
│   ├── config.py
│   └── telemetry.py
│
├── main.py
├── run_pipeline.py
└── README.md
```

Features

Automated Data Pipeline

The pipeline automatically generates:

* Telemetry datasets
* Lap times datasets
* Sector times datasets
* Tyre strategy datasets
* Weather datasets
* Race pace datasets
* Driver KPI datasets

⸻

Scalability

The project supports:

* Multiple seasons
* Multiple Grand Prix
* Dynamic dataset generation
* Modular pipeline architecture

⸻

Example Datasets

* telemetry.csv
* lap_times.csv
* sector_times.csv
* tyres_strategy.csv
* weather.csv
* race_pace.csv
* driver_kpis.csv
* track_dominance.csv

⸻

Future Improvements

* Advanced Power BI dashboards
* Interactive Streamlit web app
* Multi-race analytics
* AI race pace prediction
* Tyre degradation modeling
* Real-time telemetry visualization

⸻

Author

Yanis Berreghis