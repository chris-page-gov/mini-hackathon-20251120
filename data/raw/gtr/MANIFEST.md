# Gateway to Research Plus extracts

Downloaded: 2025-11-18T22:39Z
Source: https://gtr.ukri.org/gtr/api/projects

Notes

- `projects_sample.ndjson` was generated via `python src/data_download.py gtr --resource projects --since-year 2018 --fetch-size 50 --max-pages 1`.
- Pagination metadata is stored in `projects_sample_meta.json`.
- Increase `--max-pages` (or remove it) to pull the full cohort, and optionally switch to `organisations`, `persons`, or `outcomes` using the same script.

Next steps

1. Expand the download to cover at least 2015 onwards (match the Gemini "Innovation Ecosystem" story).
2. Derive `(project_id, organisation_id)` and `(project_id, person_id)` tidy tables for the collaboration and regional aggregation pipelines.
3. Join with ONS postcode → LAD lookup to align with the Ofcom / IMD geography.
