# Digital Infrastructure Strategy 2 – Connectivity Ladder Profiles

## Objective

Create a **“connectivity ladder”** and show how different areas are distributed along it, to answer “who is furthest behind and who is leading?”.

## SME questions addressed

- Which areas have the lowest and highest access to high‑speed broadband?
- How does coverage vary by geography (region, local authority, constituency)?

## Data

Minimum:

- Ofcom Connected Nations Spring 2025 fixed coverage table at an appropriate geography.
- Optional:
  - population or property counts to weight percentages.

## Steps

### 1. Define the connectivity ladder

Create mutually exclusive categories such as:

1. **Not served** – below 10 Mbps.
2. **Basic** – 10–30 Mbps.
3. **Superfast** – 30–100 Mbps.
4. **Ultrafast** – 100–300 Mbps.
5. **Gigabit** – >= 300 Mbps or full fibre.

You can adjust thresholds to match Ofcom’s definitions if needed.

### 2. Map coverage to ladder categories

For each area:

- use Ofcom percentages to derive:
  - share of premises in each ladder rung (if possible), or
  - at least:
    - % gigabit,
    - % superfast,
    - % below 10 Mbps.

Deliverable: `area_connectivity_ladder.csv` with one row per area and ladder shares.

### 3. Build profiles

Visual options:

- **Stacked bar chart**:
  - x‑axis: area (maybe grouped by region),
  - y‑axis: 100% stacked bars showing ladder shares.
- **Ranked bar chart**:
  - sort areas by % gigabit or % sub‑10 Mbps.
- **Highlight table**:
  - list top and bottom 10 areas on key metrics.

### 4. Add simple benchmarks

- Compute national averages for each ladder rung.
- Show how each area compares to:
  - the national average,
  - its regional average.

### 5. Craft the story

Use the Insight and Slide prompts to:

- point out:
  - where gaps are closing,
  - where there is still a long “tail” of poorly connected areas.
- suggest how this framing (the ladder) could be used to track progress over time or communicate with stakeholders.
