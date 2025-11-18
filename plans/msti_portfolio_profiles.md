# MSTI Strategy 2 – Socio‑economic Objective Portfolio Profiles

## Objective

Show how different countries distribute their **government R&D budgets across socio‑economic objectives (SEOs)**, and compare these “portfolios” with the UK.

## SME questions addressed

- How do budget allocations differ by socio‑economic objective?
- How do country rankings differ when we look beyond health to the whole portfolio?

## Data

Minimum:

- OECD MSTI / GBARD table with:
  - country,
  - year,
  - SEO category,
  - GBARD amounts (preferably in a consistent price / PPP).
- Optional:
  - GDP for normalisation (if not already expressed as % of GDP).

## Steps

### 1. Build portfolio shares

- For a chosen year (or a short range of years):
  - sum GBARD by `(country, seo)`.
- For each country:
  - compute share of total GBARD allocated to each SEO.

Deliverable: `portfolio_shares.csv` with:

- `country`, `seo`, `gbard_share_percent`.

### 2. Select countries and SEOs

To keep visuals readable:

- Limit to:
  - a small set of countries (e.g. UK + 5–10 peers), and
  - a reduced set of SEOs (group finer categories into 6–8 meaningful buckets if needed).

### 3. Visualise portfolio profiles

Options:

- **Radar / spider charts**:
  - one per country, or multiple countries on one chart.
- **Stacked bar charts**:
  - x‑axis: country,
  - y‑axis: 100% stacked bar of GBARD share by SEO.
- **Heatmap**:
  - rows: countries,
  - columns: SEO buckets,
  - colour: percentage share.

### 4. Highlight UK’s distinctive features

Compute for the UK:

- which SEOs have higher shares than the peer median,
- which SEOs have lower shares.

Add a simple table or annotation describing this.

### 5. Craft the story

Use the Insight and Slide prompts to:

- describe the UK’s portfolio in relation to peers,
- highlight any notable over‑ or under‑emphasis,
- frame this as a starting point for strategic discussions rather than definitive judgements.
