# Digital Infrastructure Strategy 3 – Mobile Multi‑network Coverage Gaps

## Objective

Identify and characterise areas with **limited mobile network coverage**, focusing on the number of operators providing reliable service.

## SME questions addressed

- Which areas have the lowest access to multiple mobile networks?
- How does mobile coverage relate to population density and other factors?

## Data

Minimum:

- Ofcom Connected Nations Spring 2025 mobile coverage tables, ideally with:
  - coverage by number of MNOs at postcode or area level.
- Optional:
  - population or property counts,
  - rural/urban classification.

## Steps

### 1. Prepare mobile coverage metrics

For each area or postcode:

- compute:
  - % of area / premises with 0, 1, 2, 3, 4 MNOs offering reliable coverage.
- Derive headline metrics:
  - `%_total_not_spots` (0 MNOs),
  - `%_single_network_only` (1 MNO),
  - `%_multi_network` (2+ MNOs).

Deliverable: `area_mobile_coverage.csv`.

### 2. Enrich with context

If available, join to:

- population or premises count,
- rural/urban classification,
- region.

This allows you to distinguish:

- sparsely populated rural not‑spots from
- more surprising urban gaps.

### 3. Visualise gaps

Ideas:

- **Map of not‑spots**:
  - highlight areas with high `%_total_not_spots` and/or high `%_single_network_only`.
- **Scatter plot**:
  - x‑axis: population density,
  - y‑axis: `%_multi_network`,
  - colour: region.
- **Ranked list**:
  - top N areas by total number of people affected by limited coverage.

### 4. Optional: relate to programmes

If time and data allow:

- link coverage metrics to programme information (e.g. Shared Rural Network documentation) to see:
  - which not‑spots are due to be addressed,
  - which may remain challenging. 

### 5. Craft the story

Use the Insight and Slide prompts to:

- explain clearly:
  - where the largest mobile coverage gaps are,
  - how many people are affected,
  - how this varies across rural and urban contexts.
- avoid over‑claiming about the causes; present this as a **targeting tool** for further investigation.
