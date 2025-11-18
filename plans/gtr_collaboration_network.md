# GtR+ Strategy 1 – Collaboration Network & Missed Opportunities

## Objective

Build an authorship and organisation collaboration network from **GtR+** to:

- show how academia, industry and other organisations collaborate, and
- highlight **“missed opportunities”** where organisations share interests but have not yet collaborated.

The final output should be:

- a clear network‑style visual (or small multiples) and
- a short story about where additional collaboration might be most fruitful.

## SME questions addressed

- How can we identify more areas for private–public research collaboration?
- How can we use authorship networks to visualise collaboration patterns and transitions from academia to industry?
- Where do overlapping or complementary research topics lack joint projects?

## Data

Minimum:

- GtR+ projects with:
  - project IDs, titles, abstracts,
  - start and end dates,
  - funding body,
  - high‑level research topics or classifications.
- Linked tables for:
  - organisations (universities, firms, local government),
  - people (PIs, Co‑Is),
  - outcomes (optional; patents, spin‑outs).

## Steps

### 1. Acquire and subset the data

- Download or query the smallest GtR+ extract that:
  - covers a manageable time window (for example: last 5–10 years),
  - focuses on one broad theme (for example: green innovation, life sciences).
- Filter to:
  - projects with at least two organisations involved,
  - projects located in or relevant to the UK.

Deliverable: a tidy table with one row per `(project_id, organisation_id)` and another per `(project_id, person_id)`.

### 2. Construct the collaboration network

- Choose a level for nodes:
  - **organisation‑level** (recommended for readability).
- Create edges where:
  - two organisations appear on the same project (undirected edge),
  - optionally weighted by:
    - number of joint projects,
    - total funding of joint projects.
- Add attributes to nodes:
  - sector (HEI, business, local government, charity),
  - region,
  - main research theme (from project classifications).

Deliverable: an edge list and node attribute table suitable for a network visualisation tool (e.g. Python + plotly, Gephi, Flourish).

### 3. Identify “missed opportunities”

- For each organisation:
  - derive a vector of research themes or topic codes (e.g. top 3 themes).
- For pairs of organisations:
  - identify pairs that:
    - share at least one theme,
    - **have no edge** (no joint project).
- Aggregate these potential pairs by:
  - region,
  - sector combination (university–business, business–business, university–local government).

Deliverables:

- A summary table of “high‑potential” pairs with:
  - both organisations’ names,
  - shared theme(s),
  - region,
  - funding intensity of that theme in the region.

### 4. Build the visualisations

- Main visual:
  - organisation‑level network:
    - nodes coloured by sector,
    - node size proportional to total funding or number of projects,
    - edge thickness proportional to number of joint projects.
- Supporting visual:
  - small table or bar chart of:
    - regions with the largest number of “high‑potential” (yet unconnected) organisation pairs.

If network visuals become cluttered:

- focus on:
  - one region,
  - one theme (e.g. green tech),
  - top N organisations by funding.

### 5. Craft the story

Use the Insight and Slide prompts to:

- state clearly:
  - where collaboration is already dense,
  - where there are obvious gaps between organisations with similar interests.
- suggest 2–3 practical follow‑up actions (for example:
  - “target networking events in region X between HEIs and SMEs in green tech”).

