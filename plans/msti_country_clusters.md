# MSTI Strategy 3 – Country Clusters by R&D Profile

## Objective

Cluster countries based on their **R&D budget profiles** (for example, GBARD shares across SEOs or total R&D effort indicators) and show where the UK sits in this landscape.

## SME questions addressed

- Do countries with similar R&D budget profiles form identifiable groups?
- Which cluster does the UK belong to, and what might that imply?

## Data

Minimum:

- Same GBARD by SEO data used in Strategy 2, or
- A combination of MSTI indicators (e.g. GERD, business share, higher education share).

## Steps

### 1. Build feature vectors for countries

- Choose a year (or average over a short period).
- For each country, build a feature vector, e.g.:
  - GBARD shares across key SEOs, and/or
  - GERD as % of GDP,
  - share of R&D performed by business vs higher education vs government.

Deliverable: `country_features.csv`.

### 2. Standardise and select features

- Standardise numeric features (e.g. z‑scores).
- Check for:
  - missing data,
  - highly correlated variables (drop some if needed).

### 3. Run a simple clustering algorithm

- Use a straightforward algorithm such as k‑means with a small k (for example 3–5).
- Explore different values of k quickly and pick one that yields interpretable clusters.
- Record:
  - cluster assignments per country,
  - cluster‑level averages of the main indicators.

Deliverable: `country_clusters.csv`.

### 4. Visualise clusters

Options:

- 2D scatter plot using:
  - PCA components, or
  - two key indicators (e.g. GERD% GDP vs business share).
  - Points coloured by cluster, with the UK highlighted.
- Table or small multiples showing the average portfolio for each cluster.

### 5. Craft the story

Use the Insight and Slide prompts to:

- describe the main cluster types (for example: “high private‑sector, high total spend”; “public‑sector‑led, moderate spend”).
- indicate where the UK sits and who its nearest peers are in this space.

Stress that clusters are **illustrative**, not definitive – they depend on feature choices and method.
