from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "msti_gbard_2010_2024.csv"


@st.cache_data(show_spinner=False)
def load_msti() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["TIME_PERIOD"] = df["TIME_PERIOD"].astype(int)
    return df


def render_seo_mix(df: pd.DataFrame) -> None:
    st.write("### UK portfolio mix by socio-economic objective")
    subset = df[(df["REF_AREA"] == "GBR") & (df["UNIT_MEASURE"] == "USD_PPP")].copy()
    if subset.empty:
        st.info("No UK observations found in the processed file.")
        return
    fig = px.area(
        subset,
        x="TIME_PERIOD",
        y="value",
        color="SEO",
        title="UK GBARD (USD PPP) by socio-economic objective",
        labels={"TIME_PERIOD": "Year", "value": "USD PPP (millions)", "SEO": "Objective"},
    )
    st.plotly_chart(fig, use_container_width=True)


def render_gdp_share(df: pd.DataFrame, countries: list[str], year_range: tuple[int, int]) -> None:
    st.write("### GBARD as % of GDP (comparators)")
    subset = df[
        (df["UNIT_MEASURE"] == "PT_B1GQ")
        & (df["TIME_PERIOD"].between(year_range[0], year_range[1]))
        & (df["REF_AREA"].isin(countries))
    ]
    if subset.empty:
        st.warning("No % GDP observations for the selected combination.")
        return
    fig = px.line(
        subset,
        x="TIME_PERIOD",
        y="value",
        color="REF_AREA_NAME",
        markers=True,
        labels={"TIME_PERIOD": "Year", "value": "% of GDP", "REF_AREA_NAME": "Country"},
    )
    st.plotly_chart(fig, use_container_width=True)


def main() -> None:
    st.title("National Overview")
    st.caption("Source: data/processed/msti_gbard_2010_2024.csv")

    df = load_msti()
    all_countries = sorted(df["REF_AREA_NAME"].dropna().unique())
    default_countries = [c for c in ["United Kingdom", "Germany", "France", "United States", "Japan"] if c in all_countries]

    with st.sidebar:
        st.header("Filters")
        countries = st.multiselect("Comparator countries", options=all_countries, default=default_countries)
        year_min, year_max = int(df["TIME_PERIOD"].min()), int(df["TIME_PERIOD"].max())
        year_range = st.slider("Year range", min_value=year_min, max_value=year_max, value=(max(year_min, 2010), year_max))

    render_seo_mix(df)
    render_gdp_share(df, countries, year_range)

    st.markdown(
        """
        **Notes**
        - SEO mix currently focuses on the UK to mirror the Gemini “health priority” storyline.
        - % GDP lines highlight whether comparator countries are catching up or lagging the UK.
        """
    )


if __name__ == "__main__":
    main()
