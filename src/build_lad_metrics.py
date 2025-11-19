"""Build LAD-level digital + deprivation metrics for the UK Innovation Monitor."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIGITAL = BASE_DIR / "data" / "raw" / "digital"
RAW_IMD = BASE_DIR / "data" / "raw" / "imd"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

FIXED_FILE = RAW_DIGITAL / "fixed" / "202501_fixed_laua_coverage_r01.csv"
MOBILE_FILE = RAW_DIGITAL / "mobile" / "202501_mobile_coverage_laua_r01.csv"
IMD_FILE = RAW_IMD / "IMD2019_LAD.xlsx"


def load_fixed() -> pd.DataFrame:
    rename_map = {
        "All Premises": "premises_total",
        "Gigabit availability (% premises)": "gigabit_availability_pct",
        "Full Fibre availability (% premises)": "full_fibre_availability_pct",
        "SFBB availability (% premises)": "sfbb_availability_pct",
        "UFBB availability (% premises)": "ufbb_availability_pct",
        "Number of premises with Gigabit availability": "premises_gigabit_count",
    }
    df = pd.read_csv(FIXED_FILE)
    df = df.rename(columns=rename_map)
    keep_cols = [
        "laua",
        "laua_name",
        "premises_total",
        "gigabit_availability_pct",
        "full_fibre_availability_pct",
        "sfbb_availability_pct",
        "ufbb_availability_pct",
        "premises_gigabit_count",
    ]
    return df[keep_cols]


def load_mobile() -> pd.DataFrame:
    rename_map = {
        "4G_prem_out_0": "four_g_prem_out_0",
        "4G_prem_out_1": "four_g_prem_out_1",
        "4G_prem_out_2": "four_g_prem_out_2",
        "4G_prem_out_3": "four_g_prem_out_3",
        "4G_prem_out_4": "four_g_prem_out_4",
        "5G_high_confidence_prem_out_0": "five_g_hc_prem_out_0",
        "5G_high_confidence_prem_out_1": "five_g_hc_prem_out_1",
        "5G_high_confidence_prem_out_2": "five_g_hc_prem_out_2",
        "5G_high_confidence_prem_out_3": "five_g_hc_prem_out_3",
        "5G_high_confidence_prem_out_4": "five_g_hc_prem_out_4",
        "5G_very_high_confidence_prem_out_0": "five_g_vhc_prem_out_0",
        "5G_very_high_confidence_prem_out_4": "five_g_vhc_prem_out_4",
    }
    df = pd.read_csv(MOBILE_FILE)
    df = df.rename(columns=rename_map)
    keep_cols = [
        "laua",
        "laua_name",
        "four_g_prem_out_4",
        "five_g_hc_prem_out_3",
        "five_g_hc_prem_out_4",
        "five_g_vhc_prem_out_4",
    ]
    available = [c for c in keep_cols if c in df.columns]
    return df[available]


def load_imd() -> pd.DataFrame:
    df = pd.read_excel(IMD_FILE, sheet_name="IMD")
    df = df.rename(
        columns={
            "Local Authority District code (2019)": "lad_code",
            "Local Authority District name (2019)": "lad_name",
            "IMD - Average score ": "imd_average_score",
            "IMD - Rank of average score ": "imd_rank",
            "IMD - Proportion of LSOAs in most deprived 10% nationally ": "imd_pct_most_deprived",
        }
    )
    cols = ["lad_code", "lad_name", "imd_average_score", "imd_rank", "imd_pct_most_deprived"]
    df = df[cols]
    df["imd_decile"] = pd.qcut(df["imd_rank"], 10, labels=range(1, 11)).astype(int)
    return df


def main() -> None:
    fixed = load_fixed()
    mobile = load_mobile()
    imd = load_imd()

    lad = fixed.merge(mobile, on="laua", how="left", suffixes=("", "_mobile"))
    if "laua_name_mobile" in lad.columns:
        lad = lad.drop(columns=["laua_name_mobile"])
    lad = lad.merge(imd, left_on="laua", right_on="lad_code", how="left")

    lad["premises_gigabit_count"] = lad["premises_gigabit_count"].fillna(0)
    lad["gigabit_availability_pct"] = lad["gigabit_availability_pct"].fillna(0)
    lad["four_g_prem_out_4"] = lad["four_g_prem_out_4"].fillna(0)

    lad["digital_resilience_score"] = (
        lad["gigabit_availability_pct"] + lad["four_g_prem_out_4"]
    ) / 2

    lad["digital_strain_index"] = lad["premises_total"] / np.maximum(
        lad["premises_gigabit_count"], 1
    )

    lad["five_g_ready_pct"] = lad[["five_g_hc_prem_out_3", "five_g_hc_prem_out_4"]].sum(axis=1, min_count=1)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROCESSED_DIR / "lad_digital_metrics.parquet"
    lad.to_parquet(out_path, index=False)
    lad.to_csv(PROCESSED_DIR / "lad_digital_metrics.csv", index=False)
    print(f"[lad] saved {len(lad)} rows to {out_path}")


if __name__ == "__main__":
    main()
