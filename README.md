# Mini Hackathon – Analysis & Visualisation Templates

## Purpose

This repository provides a reusable scaffold for the mini hackathon built around three datasets:

- **Gateway to Research Plus (GtR+)** – UKRI-funded research and innovation projects.
- **OECD Main Science and Technology Indicators (MSTI)** – government budget allocations and other R&D indicators across countries.
- **Digital Infrastructure (Ofcom Connected Nations, Spring 2025)** – UK fixed broadband and mobile coverage.

**Facts about the datasets**

- GtR / GtR+ is published by UKRI and exposes project, people, organisation and outcome level data via an API and bulk downloads.
- MSTI is an OECD database with over 100 indicators, including Government Budget Allocations for R&D (GBARD) by socio‑economic objective.
- The Digital Infrastructure data here is derived from Ofcom’s Connected Nations Spring 2025 update, which reports fixed broadband and mobile coverage across the UK as of January 2025.

**Design choices in this repo (opinionated)**

- A **common pipeline** pattern is used for all three datasets: acquire → tidy → derive metrics → visualise → narrate.
- Work is organised into **nine strategies** (three per dataset), each with a plan document under `plans/`.
- A light‑weight **agent pattern** (using ChatGPT / Deep Research / Codex‑style tools) is defined in `agents.md` so you can plug this into your preferred AI tooling.

Use this repo as a starting point: copy it, adapt the plans, and swap in the actual code and dashboards you build during the hackathon.
## Quick data acquisition

A helper script (`src/data_download.py`) automates the tedious download steps so you can get straight to analysis:

```bash
# Grab Ofcom Connected Nations files (and unzip them)
python src/data_download.py digital --extract

# Pull a recent slice of GtR+ projects (adjust --since-year / --max-pages as needed)
python src/data_download.py gtr --resource projects --since-year 2015 --max-pages 50

# Resume a long GtR download if it was interrupted
python src/data_download.py gtr --resource projects --since-year 2015 --resume

# Fetch OECD MSTI / GBARD data (adjust countries / years as needed)
python src/data_download.py msti --countries GBR,USA,DEU,FRA,JPN,CAN,ITA --start-year 2010 --end-year 2024

# Generate the MSTI Gemini visuals (expects the OECD CSV in data/raw/msti/)
python src/gemini-viz.py

# Build LAD-level digital + deprivation metrics for mapping
python src/build_lad_metrics.py
```

The script writes into `data/raw/…` (ignored by git); keep short MANIFEST.md notes in those folders so others know which filters you used. Processed artefacts (Parquet/CSV) land under `data/processed/` ready for analysis or feeding the Streamlit app.

## Environment setup (uv)

This repo now uses [uv](https://github.com/astral-sh/uv) for dependency management (the devcontainer installs it automatically). For local setups:

1. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Create/update the virtual environment: `uv sync`
3. Run commands via uv, e.g.:
   - `uv run python src/data_download.py ...`
   - `uv run streamlit run Home.py`

## Repository structure

- `README.md` – this file; overview and how to use the scaffold.
- `CHANGELOG.md` – changes over time.
- `agents.md` – roles and instructions for AI agents (Deep Research, Code, Storytelling).
- `plans/` – nine concrete strategy plans (three per dataset).
- `prompts/` – ready‑to‑paste prompts for Deep Research / Code / Narrative agents.
- `src/common_pipeline.py` – a minimal Python scaffold for data loading and summary tables (to extend).
- `config/datasets.md` – quick notes on expected data sources and fields.

## How to use this in the mini hackathon

1. **Choose a dataset and SME question**

   - GtR+: collaboration, missed opportunities, regional impacts.
   - MSTI: cross‑country comparisons of R&D budgets, especially health and other socio‑economic objectives.
   - Digital Infrastructure: spatial inequalities in broadband/mobile coverage and their correlates.

2. **Pick one of the three strategies for that dataset**

   - Open the relevant file in `plans/` (for example: `plans/gtr_collaboration_network.md`).
   - Confirm the strategy really does address the SME question you care about.
   - If you have time, you can blend ideas from more than one strategy.

3. **Run the Deep Research prompt (optional but recommended)**

   - Open `prompts/deep_research_prompt.md`.
   - Paste it into ChatGPT’s Deep Research (or equivalent).
   - Fill in the `{{DATASET_NAME}}` and `{{SME_QUESTION}}` placeholders.
   - Skim the output for:
     - caveats about the data,
     - definitions of key indicators,
     - any published examples you might emulate.

4. **Use the Code Agent prompt to generate a working pipeline**

   - Open `prompts/code_agent_prompt.md`.
   - Paste it into your code‑capable model (e.g. ChatGPT with Code Interpreter, GitHub Copilot Chat, or Codex‑style tooling).
   - Point it at the chosen **plan file** and dataset file.
   - Let it:
     - write a Python notebook or script,
     - produce clean, documented code,
     - export summary tables and chart‑ready data.

5. **Use the Narrative / Slides prompts to build the story**

   - Once charts and summary tables exist, open:
     - `prompts/insight_prompt.md` to draft the narrative,
     - `prompts/slide_prompt.md` to get a first pass at slides using the provided PowerPoint template.
   - Paste in:
     - a list of your main metrics and chart types,
     - screenshots or descriptions of the visuals,
     - the SME question(s) you are targeting.

6. **Iterate towards something that scores well against the marking criteria**

   Keep checking your work against:

   - **Impact & storytelling** – is there a clear “so what?” for a non‑technical decision‑maker?
   - **Creativity & innovation** – are you using visuals or combinations of views that genuinely add insight?
   - **Clarity & readability** – is it easy to read at a glance, with minimal clutter?

## Overview of the nine strategies

### Dataset 1 – GtR+ (UKRI Gateway to Research Plus)

1. **Collaboration Network & Missed Opportunities**  
   - Build person/organisation collaboration networks.  
   - Highlight themes where organisations share interests but have never collaborated (“white‑space” opportunities).  
   - File: `plans/gtr_collaboration_network.md`.

2. **Regional Funding & Outcomes Explorer**  
   - Aggregate projects by region and sector.  
   - Compare funding inputs to outputs (patents, spin‑outs, collaborations) to spot over‑ and under‑performance.  
   - File: `plans/gtr_regional_outcomes.md`.

3. **Funding‑to‑Engagement Time Lags**  
   - Measure the lag between award dates and first visible external outputs (spin‑outs, patents, collaborations).  
   - Show variation by sector, region and funder.  
   - File: `plans/gtr_time_lags.md`.

### Dataset 2 – MSTI (OECD Main Science and Technology Indicators)

4. **Health R&D Budget Rankings**  
   - Compare government health R&D budget allocations as a percentage of GDP across countries and over time.  
   - Reproduce and extend the Life Sciences Competitiveness narrative.  
   - File: `plans/msti_health_rankings.md`.

5. **Socio‑economic Objective Portfolio Profiles**  
   - For each country, profile the distribution of GBARD across socio‑economic objectives (health, environment, defence, etc.).  
   - Visualise as radar charts or stacked bars to tell “portfolio” stories.  
   - File: `plans/msti_portfolio_profiles.md`.

6. **Country Clusters by R&D Profile**  
   - Use normalised budget shares to cluster countries with similar R&D profiles.  
   - Position the UK within these clusters and discuss strategic positioning.  
   - File: `plans/msti_country_clusters.md`.

### Dataset 3 – Digital Infrastructure (Ofcom Connected Nations)

7. **Connectivity vs Deprivation Map**  
   - Join Ofcom coverage statistics to indices of multiple deprivation and rural/urban classifications.  
   - Show how connectivity varies with deprivation and geography.  
   - File: `plans/digitalinfra_connectivity_deprivation.md`.

8. **Connectivity Ladder Profiles**  
   - Define a “connectivity ladder” (sub‑10 Mbps → superfast → ultrafast → gigabit) and show the distribution for each local area or constituency.  
   - Present “before vs ambition” or “peer comparison” views.  
   - File: `plans/digitalinfra_connectivity_ladder.md`.

9. **Mobile Multi‑network Coverage Gaps**  
   - Focus on areas with only one (or zero) mobile network operators providing reliable coverage.  
   - Relate these gaps to population density and any available programme data (e.g. SRN).  
   - File: `plans/digitalinfra_mobile_gaps.md`.

## Common implementation pattern across datasets

Although the subject‑matter differs, all nine options can be implemented with the same basic components:

1. **Config‑driven data ingestion**
   - Simple configuration (`config/datasets.md` plus your own notes) describing:
     - source (CSV, Excel, API),
     - expected keys (country, region, time, sector),
     - any joins (e.g. region ↔ deprivation index).

2. **Reusable Python scaffold (`src/common_pipeline.py`)**
   - Functions to:
     - load and inspect data,
     - apply tidy‑data conventions,
     - compute grouped summaries,
     - export lightweight CSVs for charting tools (Tableau, Power BI, Flourish, etc.).

3. **Agent‑assisted analysis & storytelling**
   - Deep Research agent: contextual background and definitions.
   - Code agent: implements the pipeline for a chosen plan.
   - Insight / Slide agents: generate plain‑English narratives and slide outlines.

This structure means you can **reuse the same approach** for more than one dataset during the hackathon:

- Once the pipeline is working for (say) the Digital Infrastructure ladder, you can re‑point it at a GtR+ regional summary or an MSTI cross‑country view by:
  - swapping in a different dataset,
  - changing the grouping keys,
  - updating a few chart definitions.

## Recommended “best” solution to build yourself

In terms of effort vs reward in a mini hackathon, a good choice is:

> A single, config‑driven Python notebook (or script) using `src/common_pipeline.py`, plus AI‑assisted prompts from `prompts/`, that you can point at any of the three datasets to generate:
> - a clean, analysable dataset,
> - 3–5 high‑impact charts,
> - a one‑page narrative suitable for the presentation template.

You can then tailor that pipeline to one or two of the nine strategies, depending on your team’s interest and time.

For full details of that pattern, see:
- `agents.md` – how to orchestrate Deep Research, Code, and Storytelling agents.
- `plans/*` – step‑by‑step instructions per strategy.
- `prompts/*` – copy‑paste prompts for the different agents.

Good luck with the hackathon – and feel free to extend this repo after the event with your final notebooks and decks!
