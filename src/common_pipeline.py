"""common_pipeline.py – minimal scaffold for reuse across datasets.

This is intentionally simple and heavily commented so that a code‑capable LLM
(Codex, GitHub Copilot Chat, ChatGPT with Code Interpreter) can extend it quickly.

The idea is:

- Keep dataset‑agnostic utilities here (loading, basic summaries).
- Implement dataset‑specific logic in separate notebooks or scripts that *import* this file.
- Use the strategy plans under `plans/` as the source of truth for what to compute.

NOTE: You will need to adapt column names to match the actual files you download.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Any

import pandas as pd


@dataclass
class DatasetConfig:
    """Light‑weight configuration for a tabular dataset.

    This is deliberately minimal. Extend it during the hackathon if helpful.
    """

    name: str
    path: Path
    index_cols: Optional[List[str]] = None


def load_table(config: DatasetConfig) -> pd.DataFrame:
    """Load a CSV or Excel file into a pandas DataFrame.

    - Uses the file extension to decide how to read.
    - Does *not* attempt to clean or rename columns – that is strategy‑specific.
    """
    path = config.path
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path!s}")

    if path.suffix.lower() in {".csv"}:
        df = pd.read_csv(path)
    elif path.suffix.lower() in {".xls", ".xlsx"}:
        df = pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    if config.index_cols:
        df = df.set_index(config.index_cols)

    return df


def summarise_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Return a basic numeric summary (count, mean, std, min, max, quartiles).

    This is a quick sanity check for any dataset.
    """
    return df.describe(include="number").T


def group_and_aggregate(
    df: pd.DataFrame,
    group_cols: List[str],
    agg_spec: Dict[str, List[str]],
) -> pd.DataFrame:
    """Generic grouped aggregation.

    Parameters
    ----------
    df:
        Input DataFrame.
    group_cols:
        Columns to group by (e.g. country, year; region, sector).
    agg_spec:
        Mapping of column name → list of aggregation functions
        (e.g. {"amount_awarded": ["sum", "mean"]}).

    Returns
    -------
    A DataFrame with a MultiIndex on the columns (metric, agg_func).
    You can flatten these later for chart‑friendly outputs.
    """
    grouped = df.groupby(group_cols).agg(agg_spec)
    grouped = grouped.reset_index()
    return grouped


def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Flatten MultiIndex columns into simple snake_case names.

    Example:
        ('amount_awarded', 'sum') → 'amount_awarded_sum'
    """
    new_cols = []
    for col in df.columns:
        if isinstance(col, tuple):
            parts = [str(p) for p in col if p != ""]
            new_cols.append("_".join(parts))
        else:
            new_cols.append(str(col))
    df = df.copy()
    df.columns = new_cols
    return df


def save_for_visualisation(df: pd.DataFrame, out_path: Path) -> None:
    """Save a DataFrame as CSV ready for use in tools like Tableau or Power BI."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)


if __name__ == "__main__":
    # This block is only an example and can be safely deleted.
    example_path = Path("/path/to/your/data.csv")  # TODO: replace during the hackathon
    config = DatasetConfig(name="example", path=example_path)
    try:
        df_example = load_table(config)
        summary = summarise_numeric(df_example)
        print("Loaded example dataset with shape", df_example.shape)
        print(summary.head())
    except FileNotFoundError:
        print("Example file not found – this is expected until you point it at real data.")
