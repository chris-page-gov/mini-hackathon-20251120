# GtR+ Strategy 2 – Regional Funding & Outcomes Explorer

## Objective

Create a regional view of **UKRI investment vs outcomes** to explore how GtR+ funding relates to:

- patents,
- spin‑outs,
- collaboration patterns.

The final output should resemble a **regional dashboard** answering “who is punching above or below their weight?”.

## SME questions addressed

- Does UKRI investment within a region or sector tend to foster growth specifically within that region or sector?
- Does UKRI investment in a domain lead firms to specialise in that domain?
- How can UKRI better support regional innovation?

## Data

Minimum:

- GtR+ projects with:
  - project ID, start and end dates,
  - amount awarded,
  - high‑level research domain,
  - lead organisation and its region.
- Outcomes table with:
  - outcome type (patent, spin‑out, collaboration),
  - associated project ID,
  - date.
- Optional:
  - regional “denominators” such as business counts or population.

## Steps

### 1. Define regions and domains

- Decide on geography:
  - NUTS1, NUTS2 or local enterprise partnership (LEP) level (keep it simple).
- Decide on domains:
  - use existing GtR classifications (e.g. “health”, “energy”, “ICT”) or map them into 5–10 broad buckets.

Deliverable: lookup tables for region codes and domain groups.

### 2. Build regional funding indicators

- Aggregate by `(region, domain)`:
  - total funding,
  - number of projects,
  - average project size.
- Optionally normalise by:
  - regional population,
  - number of businesses in that domain.

Deliverable: tidy table `region_domain_funding.csv`.

### 3. Build regional outcome indicators

- Link outcomes to projects via `project_id`.
- Aggregate by `(region, domain)`:
  - number of patents,
  - number of spin‑outs,
  - number of collaborative projects (multiple organisations).
- Derive simple ratios:
  - patents per £10m,
  - spin‑outs per £10m,
  - collaboration rate (% of projects with >1 organisation).

Deliverable: tidy table `region_domain_outcomes.csv`.

### 4. Compare funding and outcomes

- Join the two tables on `(region, domain)`.
- Create derived metrics for performance:
  - outcome‑per‑pound ratios,
  - relative performance vs national average.

Visual ideas:

- Heatmap:
  - rows = regions,
  - columns = domains,
  - colour = outcome‑per‑pound metric.
- Scatter plot:
  - x‑axis = funding per capita,
  - y‑axis = patents per capita,
  - colour = domain, bubble size = total funding.

### 5. Build a simple regional dashboard

Depending on your tools (Tableau, Power BI, Python):

- One overview page with:
  - map of funding intensity per region,
  - bar chart of outcome intensity,
  - a small multiples view per domain.
- Provide interactivity where possible (filter by domain, hover for numbers).

### 6. Craft the story

Use the Insight and Slide prompts to:

- highlight:
  - regions that appear to convert funding into outcomes efficiently,
  - regions with high funding but relatively low measured outcomes (or vice versa).
- remain careful not to over‑interpret causality – present this as **exploratory** evidence for further investigation.
