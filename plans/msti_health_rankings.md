# MSTI Strategy 1 – Health R&D Budget Rankings

## Objective

Compare **government health R&D budget allocations as a percentage of GDP** across countries and over time, and show where the UK sits in these rankings.

## SME questions addressed

- How does the UK compare with other countries in health R&D allocations as a % of GDP?
- How do rankings change when we look at other socio‑economic objectives?

## Data

Minimum:

- OECD MSTI / GBARD table for:
  - government budget allocations for R&D by socio‑economic objective (SEO),
  - including the metric “health R&D as % of GDP” or equivalent.
- Country list including:
  - G7,
  - EU27,
  - other relevant comparators.

## Steps

### 1. Extract health R&D budget data

- From the MSTI / GBARD dataset:
  - filter to SEO = “health” (or the closest category label).
  - extract for a recent time window (for example: last 10–15 years).
- Fields needed:
  - `country`, `year`,
  - `gbard_percent_gdp` (or equivalent).

Deliverable: tidy table `health_gbard_percent_gdp.csv`.

### 2. Build rankings

- For each year:
  - rank countries by health GBARD as % of GDP.
- Compute:
  - the UK’s rank per year,
  - the median, minimum and maximum across a chosen peer group.

Deliverable: `health_rankings.csv`.

### 3. Visualise rankings and trends

Visuals:

- Line chart:
  - y‑axis: health R&D as % of GDP,
  - x‑axis: year,
  - lines: UK vs a small set of peers (for example: US, Germany, France, Korea).
- Bar chart:
  - latest year rankings for all available countries,
  - highlight the UK bar with a different colour.

### 4. Extend to other socio‑economic objectives

If time allows:

- Repeat the above for 2–3 other SEOs (e.g. environment, defence).
- Either:
  - create small multiples for each SEO, or
  - create a single chart showing the UK’s rank across SEOs.

### 5. Craft the story

Use the Insight and Slide prompts to:

- state clearly:
  - where the UK stands in absolute terms,
  - how it compares with key peers,
  - how its position has trended.
- avoid over‑stating causal claims; focus on:
  - “relative effort” as measured by GBARD.
