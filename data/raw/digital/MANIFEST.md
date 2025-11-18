# Ofcom Connected Nations – Spring 2025

Downloaded: 2025-11-18T22:32Z
Source page: https://www.ofcom.org.uk/phones-and-broadband/coverage-and-speeds/connected-nations-update-spring-2025

Files

- `fixed_coverage_full_fibre.zip` – bundle of all fixed coverage CSVs (UK + nations, LA, Parliamentary Constituency, residential subset, full fibre take-up).
- `mobile_coverage_all.zip` – UK/nations + LA + constituency mobile coverage tables.
- `about_fixed_data.pdf` – methodology for fixed coverage tables.
- `about_mobile_data.pdf` – methodology for mobile coverage tables.
- Extracted folders `fixed/` and `mobile/` contain the CSVs used by the LAD/SOAs steps in the plan.

Next steps

1. Join LA-level coverage data (`202501_fixed_laua_coverage_r01.csv`, `202501_mobile_coverage_laua_r01.csv`) on `laua`.
2. Enrich with IMD deciles (to be downloaded) and population/property counts.
3. Persist aggregated metrics to `data/processed/digital_lad_metrics.parquet` for downstream visualisation.
