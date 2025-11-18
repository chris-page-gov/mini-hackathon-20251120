# GtR+ Strategy 3 – Funding‑to‑Engagement Time Lags

## Objective

Measure the **time between funding and external engagement** (e.g. patents, spin‑outs, collaborations) to:

- understand typical lag times,
- spot sectors or regions where engagement is unusually slow or fast.

## SME questions addressed

- Can we track time lags between funding and external engagement to highlight bottlenecks?
- Are there systematic differences across sectors, regions or funders?

## Data

Minimum:

- GtR+ projects with:
  - project ID,
  - start date,
  - end date,
  - amount awarded,
  - funder,
  - domain,
  - region of lead organisation.
- Outcomes table with:
  - outcome type,
  - `project_id`,
  - `outcome_date`.

## Steps

### 1. Build project–outcome pairs

- Join projects to outcomes on `project_id`.
- For each `(project_id, outcome)` pair, calculate:
  - `lag_start = outcome_date - start_date`,
  - `lag_end = outcome_date - end_date`.

Decide whether to use `lag_start` or `lag_end` as your main measure (be explicit in comments).

### 2. Clean and filter lags

- Filter out:
  - obviously bad dates (nulls, negative lags, extreme outliers due to data entry errors).
- Cap very long lags (for example at 10 years) if necessary to make visualisations readable.

Deliverable: tidy table of lags with columns:

- `project_id`, `funder`, `domain`, `region`,
- `outcome_type`, `lag_years`.

### 3. Summarise lags by group

- Group by:
  - sector (domain),
  - region,
  - funder (if you want to compare UKRI councils).
- Compute:
  - median lag,
  - interquartile range,
  - proportion of outcomes within 2/3/5 years.

Deliverable: `lag_summary.csv`.

### 4. Visualise lag distributions

Examples:

- Box plots of `lag_years` by domain or region.
- Cumulative distribution curves showing:
  - proportion of outcomes achieved within N years.
- Simple table or bar chart for:
  - “% of outcomes within 3 years of funding” by domain.

### 5. Craft the story

Use the Insight and Slide prompts to:

- describe the typical pattern:
  - “Most outcomes emerge within X–Y years” etc.
- highlight:
  - domains where lags are significantly longer or shorter,
  - potential hypotheses (e.g. clinical research vs software).

Be cautious about:
- data completeness (not all outcomes are reported),
- differences in how outcome dates are recorded across types.
