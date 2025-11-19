import streamlit as st

st.title("Collaboration Networks (Coming Soon)")
st.caption("This page will surface GtR+ collaboration graphs once the project/person/organisation extracts finish downloading.")

st.markdown(
    """
    ### Planned functionality

    1. **Organisation network view** – force-directed graph filtered by region/theme highlighting strong vs weak links.
    2. **Missed opportunity table** – semantic similarity pairs that share research themes but have never collaborated.
    3. **Spin-out tracker** – time lag between funding and observable outcomes per region.

    ### What’s needed next

    - Run `python src/data_download.py gtr --resource organisations` (and similar for `persons`, `outcomes`) once the
      ongoing `projects` download completes.
    - Build tidy tables (`project_id`, `organisation_id`, `role`, `amount_awarded`) and save them under `data/processed/`.
    - Hook those tables into this page using NetworkX + Plotly for interactive visuals.

    Until those steps are complete this page acts as a placeholder so the Streamlit navigation matches the hackathon plan.
    """
)
