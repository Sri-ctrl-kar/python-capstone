Campus Energy Dashboard — README
===============================

Project overview
----------------
This Python script builds a simple pipeline to ingest campus electricity CSVs, clean and aggregate them,
produce building-level summaries, and generate a visual dashboard (PNG) plus exported CSV/text reports.

Quick features
--------------
- Reads CSV files from ./data/ (auto-generates sample data if the folder is missing)
- Expects columns: Date, Building, KWH (Date parseable by pandas)
- Computes daily/weekly aggregates and per-building summaries
- Generates: dashboard.png, cleaned_energy_data.csv, building_summary.csv, summary.txt

Requirements
------------
- Python 3.8+
- Packages: pandas, numpy, matplotlib
Install with:
pip install pandas numpy matplotlib

Data format
-----------
Each CSV should contain rows like:
Date,Building,KWH
2023-01-01,Library,234

- Date: ISO or any format parseable by pandas.to_datetime
- Building: building identifier (filename used if missing)
- KWH: numeric energy reading

How to run
----------
1. Place CSV files into a directory named data/ (optional — script will create sample files if missing).
2. Run the main script:
python your_script.py
(Replace your_script.py with the actual script filename containing the pipeline.)

Outputs
-------
- cleaned_energy_data.csv — combined and cleaned time-indexed data
- building_summary.csv — per-building aggregates (mean, min, max, sum)
- summary.txt — plain-text executive summary
- dashboard.png — the generated dashboard visualization

Notes & troubleshooting
-----------------------
- If dates or KWH values are invalid they will be coerced/dropped during cleaning.
- To change resampling (daily/weekly), edit the resample(...) calls in the script.
- For large datasets, consider batching or increasing memory/resources.

License
-------
Use and modify freely for educational or internal projects. No warranty.
