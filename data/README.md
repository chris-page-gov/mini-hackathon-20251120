# Data workspace

Raw datasets live under `data/raw/` and are ignored by git. Each dataset folder stores the original downloads plus a short manifest so we can refresh the data later.

## Structure

- `data/raw/gtr` – Gateway to Research Plus extracts (projects, organisations, links, outcomes).
- `data/raw/msti` – OECD MSTI / GBARD downloads (SDMX-JSON) sourced via `python src/data_download.py msti`.
- `data/raw/digital` – Ofcom Connected Nations Spring 2025 downloads along with accompanying documentation PDFs.
- `data/raw/imd` – LAD-level Indices of Multiple Deprivation summaries (2019).
- `data/processed` – Cleaned Parquet files aligned to the LAD aggregation and national benchmarking steps defined in the Gemini solution.
- `data/geo` – Supporting geographies (ONS LAD boundaries, postcode → LAD lookup tables).

## Refresh pattern

1. Run `python src/data_download.py ...` to fetch the latest raw files into `data/raw/`.
2. Run the dataset-specific prep notebooks / scripts (GtR+, MSTI, Digital Infra, IMD) to populate `data/processed/`.
3. Rebuild the Streamlit app to pick up the refreshed Parquet files.

Document any manual tweaks in the dataset-specific manifests located alongside the downloads (e.g. `data/raw/digital/MANIFEST.md`).
