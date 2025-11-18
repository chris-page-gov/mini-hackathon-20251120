# Dataset configuration notes

These notes are *not* a formal machine‑readable config, but a quick reference for humans and AI agents.

## GtR+ (Gateway to Research Plus)

- **Source**: UKRI GtR / GtR+ bulk download or API.
- **Unit of analysis**: projects, organisations, people, outcomes (patents, spin‑outs, publications, etc.).
- **Typical keys and fields**
  - `project_id`, `title`, `abstract`, `start_date`, `end_date`, `amount_awarded`.
  - `organisation_id`, `organisation_name`, `organisation_region`.
  - `person_id`, `person_name`, `role` (PI, Co‑I, etc.).
  - `category` / `research_topic` / `programme`.
  - `outcome_type` (patent, spin‑out, collaboration) and `outcome_date`.
- **Joins**
  - Projects ↔ organisations (many‑to‑many).
  - Projects ↔ people (many‑to‑many).
  - Projects ↔ outcomes (one‑to‑many).
  - Organisations ↔ geographic region.

## MSTI (OECD Main Science and Technology Indicators, GBARD)

- **Source**: OECD data explorer – MSTI / GBARD by socio‑economic objective.
- **Unit of analysis**: country‑year by socio‑economic objective (SEO).
- **Typical keys and fields**
  - `country`, `iso_code`.
  - `year`.
  - `seo` (socio‑economic objective, e.g. health, environment).
  - `gbard_local_currency`, `gbard_constant_price`, `gbard_ppp`, `gbard_percent_gdp`.
- **Joins**
  - Country ↔ region groupings (G7, EU27, OECD, etc.), if desired.
  - Country ↔ external indicators (e.g. GDP, population, health outcomes) if you choose to extend.

## Digital Infrastructure (Ofcom Connected Nations – Spring 2025)

- **Source**: Ofcom Connected Nations Spring 2025 update – fixed and mobile coverage tables.
- **Unit of analysis**: postcode, local authority, or higher geography, depending on which table you select.
- **Typical keys and fields**
  - `postcode` or `lad_code` / `lad_name`.
  - Coverage metrics:
    - `% premises <10 Mbps`, `<30 Mbps`, `30–100 Mbps`, `>=300 Mbps`, `gigabit`, `full_fibre`.
    - Mobile coverage by MNO count (0, 1, 2, 3, 4 operators).
  - **External enrichment (optional)**:
    - Index of Multiple Deprivation (IMD deciles).
    - Rural/urban classification.
    - Population or property counts.
- **Joins**
  - Geography ↔ deprivation indices (ONS / MHCLG).
  - Geography ↔ population / property counts (ONS).

You can convert this into a proper YAML or JSON config if you want a fully automated pipeline later.
