# Changelog

All notable changes to this project will be documented in this file.

The format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

- Devcontainer setup (`.devcontainer/`) with Python and geospatial dependencies for running hackathon pipelines.
- Repository hygiene updates: `.gitignore` for editor/temp files and `.gitattributes` to normalise line endings across OSes.
- Data acquisition tooling:
  - `src/data_download.py` helper for GtR+ and Ofcom downloads (with placeholders for future MSTI pulls).
  - Structured `data/` workspace (tracked README + manifests, raw/processed folders kept out of git) plus cached Connected Nations Spring 2025 bundles for immediate analysis.
- OECD + IMD ingestion:
  - `python src/data_download.py msti` now pulls GBARD-by-SEO data (SDMX JSON saved under `data/raw/msti/` + processed CSV in `data/processed/`).
  - `data/raw/imd` stores the LAD-level deprivation summary (File 10 from the 2019 release) with a manifest for provenance.
  - `src/build_lad_metrics.py` aggregates Ofcom + IMD metrics into `data/processed/lad_digital_metrics.{parquet,csv}` for mapping and levelling-up analysis.
- Tooling:
  - Migrated dependency management to `uv` (`pyproject.toml` + `uv.lock` replace `requirements.txt`); devcontainer installs uv and runs `uv sync --frozen` automatically.
  - README now documents the uv workflow (`uv sync`, `uv run ...`).

## [0.1.0] - 2025-11-18

### Added

- Initial scaffold for the Mini Hackathon:
  - Nine strategy plans (three per dataset) in `plans/`.
  - Agent role definitions and instructions in `agents.md`.
  - Generic prompts for Deep Research, Code, Insight and Slides agents in `prompts/`.
  - `src/common_pipeline.py` Python scaffold for reusable data loading and summarisation.
  - `config/datasets.md` with notes on expected sources and keys.
