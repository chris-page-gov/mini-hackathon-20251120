# OECD MSTI GBARD download

Downloaded: 2025-11-18T23:51Z
Endpoint: https://sdmx.oecd.org/public/rest/data/DSD_RDS_GOV@DF_GBARD_NABS07

Parameters
- Countries: GBR, USA, DEU, FRA, JPN, CAN, ITA
- Years: 2010-2024
- Frequency: Annual (A)
- Measure: C (Government Allocations for R&D)
- FUNDMODE: _T (total)
- TRANSCOORD: _Z (not applicable)
- Units: kept in output (USD_PPP, XDC, PT_B1GQ)

Outputs
- Raw SDMX-JSON: `gbard_2010_2024.json`
- Processed CSV: `../processed/msti_gbard_2010_2024.csv`

Notes
- Use the processed file for quick analysis; it retains REF_AREA, SEO, UNIT_MEASURE, PRICE_BASE, and TIME_PERIOD columns.
- Additional countries/years can be fetched via `python src/data_download.py msti --countries=... --start-year=... --end-year=...`.
