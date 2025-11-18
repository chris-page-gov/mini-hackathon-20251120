# Changelog

All notable changes to this project will be documented in this file.

The format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

- Devcontainer setup (`.devcontainer/`) with Python and geospatial dependencies for running hackathon pipelines.
- Repository hygiene updates: `.gitignore` for editor/temp files and `.gitattributes` to normalise line endings across OSes.
- Data acquisition tooling:
  - `src/data_download.py` helper for GtR+ and Ofcom downloads (with placeholders for future MSTI pulls).
  - Structured `data/` workspace (tracked README + manifests, raw/processed folders kept out of git) plus cached Connected Nations Spring 2025 bundles for immediate analysis.

## [0.1.0] - 2025-11-18

### Added

- Initial scaffold for the Mini Hackathon:
  - Nine strategy plans (three per dataset) in `plans/`.
  - Agent role definitions and instructions in `agents.md`.
  - Generic prompts for Deep Research, Code, Insight and Slides agents in `prompts/`.
  - `src/common_pipeline.py` Python scaffold for reusable data loading and summarisation.
  - `config/datasets.md` with notes on expected sources and keys.
