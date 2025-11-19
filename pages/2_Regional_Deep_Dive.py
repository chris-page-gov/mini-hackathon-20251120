from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

LAD_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "lad_digital_metrics.csv"


@st.cache_data(show_spinner=False)
def load_lad() -> pd.DataFrame:
    df = pd.read_csv(LAD_PATH)
    df["imd_rank"] = pd.to_numeric(df["imd_rank"], errors="coerce")
    df["digital_resilience_score"] = pd.to_numeric(df["digital_resilience_score"], errors="coerce")
    df["digital_strain_index"] = pd.to_numeric(df["digital_strain_index"], errors="coerce")
    return df


def main() -> None:
    st.title("Regional Deep Dive")
    st.caption("Sources: Ofcom Connected Nations Spring 2025 + IMD 2019 (see data/processed/lad_digital_metrics.csv)")

    lad = load_lad()
    if lad.empty:
        st.error("LAD metrics file not found or empty. Run `python src/build_lad_metrics.py` first.")
        return

    with st.sidebar:
        st.header("Filters")
        decile = st.slider("IMD decile (1 = most deprived)", min_value=1, max_value=10, value=(1, 10))
        min_gigabit = st.slider("Minimum gigabit coverage (%)", min_value=0, max_value=100, value=0)
        lad_filter = lad[
            lad["imd_decile"].between(decile[0], decile[1])
            & (lad["gigabit_availability_pct"] >= min_gigabit)
        ]

    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Median digital resilience score",
            f"{lad_filter['digital_resilience_score'].median():.1f}",
            help="Average of gigabit availability % and 4G coverage %",
        )
    with col2:
        st.metric(
            "Median gigabit coverage",
            f"{lad_filter['gigabit_availability_pct'].median():.1f}%",
        )

    scatter = px.scatter(
        lad_filter,
        x="imd_rank",
        y="digital_resilience_score",
        hover_name="laua_name",
        size="gigabit_availability_pct",
        color="imd_decile",
        labels={
            "imd_rank": "IMD rank (lower = more deprived)",
            "digital_resilience_score": "Digital resilience score",
            "imd_decile": "IMD decile",
        },
        title="Deprivation vs digital resilience",
    )
    st.plotly_chart(scatter, use_container_width=True)

    st.write("### Outliers")
    top = lad_filter.nlargest(10, "digital_resilience_score")[["laua_name", "digital_resilience_score", "gigabit_availability_pct", "imd_decile"]]
    bottom = lad_filter.nsmallest(10, "digital_resilience_score")[["laua_name", "digital_resilience_score", "gigabit_availability_pct", "imd_decile"]]

    col_left, col_right = st.columns(2)
    with col_left:
        st.write("High-performing LADs")
        st.dataframe(top.reset_index(drop=True))
    with col_right:
        st.write("LADs at risk (low resilience)")
        st.dataframe(bottom.reset_index(drop=True))

    st.markdown(
        """
        **Next steps**
        - Add a choropleth once LAD boundary GeoJSON is available (`data/geo/`).
        - Incorporate GtR funding per LAD to correlate inputs with connectivity.
        """
    )


if __name__ == "__main__":
    main()
