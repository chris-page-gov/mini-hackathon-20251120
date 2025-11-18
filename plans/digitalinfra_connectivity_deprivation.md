# Digital Infrastructure Strategy 1 – Connectivity vs Deprivation Map

## Objective

Explore how **broadband and mobile coverage** vary with **indices of deprivation** and geography across the UK.

## SME questions addressed

- How does broadband and mobile coverage vary across regions, local authorities or postcodes?
- Are there correlations between digital connectivity and indices of deprivation?

## Data

Minimum:

- Ofcom Connected Nations Spring 2025 tables with:
  - coverage metrics at local authority or similar level.
- Indices of Multiple Deprivation (IMD) for the same geographies:
  - deciles or ranks.
- Optional:
  - rural/urban classification,
  - population or property counts.

## Steps

### 1. Prepare the geography

- Pick a geography level that:
  - is available in both Ofcom and deprivation data,
  - keeps the number of areas manageable (for example: local authority).
- Build a lookup table with:
  - area code,
  - area name,
  - IMD decile (or average score),
  - rural/urban flag (optional).

### 2. Prepare connectivity indicators

From Ofcom:

- Extract for each area:
  - % of premises with:
    - less than 10 Mbps,
    - less than 30 Mbps,
    - superfast (>=30 Mbps),
    - gigabit,
    - full fibre.
  - Mobile:
    - % area or premises with 0/1/2/3/4 MNOs providing reliable coverage (if available).

Deliverable: `area_connectivity.csv`.

### 3. Join and derive key metrics

- Join `area_connectivity` with deprivation data on the area code.
- Derive a small set of headline metrics, for example:
  - `gigabit_coverage_percent`,
  - `sub_10mbps_percent`,
  - `full_mobile_coverage_percent` (if available),
  - IMD decile (1 = most deprived).

### 4. Visualise relationships

Ideas:

- **Scatter plot**:
  - x‑axis: IMD decile (or rank),
  - y‑axis: gigabit coverage,
  - colour: region,
  - size: population.
- **Bivariate map**:
  - choropleth where colour encodes both connectivity and deprivation (e.g. low connectivity & high deprivation highlighted).
- **Small multiples or faceting**:
  - one map for fixed, one for mobile.

### 5. Craft the story

Use the Insight and Slide prompts to:

- highlight:
  - whether more deprived areas are systematically less well served,
  - regional exceptions (for example, high deprivation but good coverage, or vice versa).
- remain cautious about:
  - causality,
  - differences between urban and rural areas that may explain patterns.
