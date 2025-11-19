"""Utility script for pulling the three hackathon datasets.

Supports:
- GtR+ (Gateway to Research) via the public REST API (JSON).
- Digital Infrastructure (Ofcom Connected Nations Spring 2025) via static downloads.
- MSTI / GBARD placeholder hook (documented for downstream implementation once
  the precise OECD API query is finalised).

Usage (examples):
    python src/data_download.py gtr --resource projects --since-year 2015 --max-pages 50
    python src/data_download.py digital --extract

The script intentionally keeps dependencies light (requests + stdlib) so it can
run in the devcontainer and in CI if required.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import pandas as pd
import requests

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"

GTR_RESOURCE_KEYS: Dict[str, str] = {
    "projects": "project",
    "organisations": "organisation",
    "persons": "person",
    "outcomes": "outcome",
}

DIGITAL_FILES: Dict[str, str] = {
    "digital/fixed_coverage_full_fibre.zip": "https://www.ofcom.org.uk/siteassets/resources/documents/research-and-data/multi-sector/infrastructure-research/connect-nations-spring-2025/data-downloads/fixed-coverage-and-full-fibre-take-up.zip.zip?v=396496",
    "digital/mobile_coverage_all.zip": "https://www.ofcom.org.uk/siteassets/resources/documents/research-and-data/multi-sector/infrastructure-research/connect-nations-spring-2025/data-downloads/mobile-coverage-all.zip?v=396502",
    "digital/about_fixed_data.pdf": "https://www.ofcom.org.uk/siteassets/resources/documents/research-and-data/multi-sector/infrastructure-research/connect-nations-spring-2025/data-downloads/about-this-data---fixed-coverage-and-full-fibre-take-up.pdf?v=396500",
    "digital/about_mobile_data.pdf": "https://www.ofcom.org.uk/siteassets/resources/documents/research-and-data/multi-sector/infrastructure-research/connect-nations-spring-2025/data-downloads/about-this-data-mobile-coverage.pdf?v=396503",
}

OECD_BASE_URL = "https://sdmx.oecd.org/public/rest"
OECD_GBARD_FLOW = "DSD_RDS_GOV@DF_GBARD_NABS07"

REF_AREA_LABELS = {
    "GBR": "United Kingdom",
    "USA": "United States",
    "DEU": "Germany",
    "FRA": "France",
    "JPN": "Japan",
    "CAN": "Canada",
    "ITA": "Italy",
    "AUS": "Australia",
    "KOR": "South Korea",
    "CHN": "China",
}


@dataclass
class DownloadStats:
    records: int
    pages: int
    duration_s: float


def _request_json(url: str, params: Optional[dict] = None, retries: int = 8) -> dict:
    for attempt in range(retries):
        response = requests.get(
            url,
            params=params,
            headers={"Accept": "application/json"},
            timeout=60,
        )
        if response.status_code == 429 and attempt < retries - 1:
            wait = min(60, 2 ** attempt)
            print(f"[gtr] rate limited, sleeping {wait}s before retry")
            time.sleep(wait)
            continue
        response.raise_for_status()
        return response.json()
    response.raise_for_status()


def _download_file(url: str, dest: Path, overwrite: bool = False) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and not overwrite:
        print(f"[skip] {dest} already exists")
        return
    with requests.get(url, stream=True, timeout=120) as response:
        response.raise_for_status()
        total = int(response.headers.get("content-length", 0))
        chunk_size = 1 << 15
        written = 0
        with dest.open("wb") as fh:
            for chunk in response.iter_content(chunk_size):
                if chunk:
                    fh.write(chunk)
                    written += len(chunk)
                    if total:
                        pct = (written / total) * 100
                        sys.stdout.write(f"\r[download] {dest.name} {pct:5.1f}%")
                        sys.stdout.flush()
        if total:
            sys.stdout.write("\n")
    print(f"[ok] downloaded {dest.relative_to(BASE_DIR)} ({written/1_000_000:.2f} MB)")


def download_gtr(
    resource: str,
    since_year: Optional[int],
    fetch_size: int,
    max_pages: Optional[int],
    output_name: Optional[str],
    delay: float,
    log_every: int = 100,
    resume: bool = False,
) -> DownloadStats:
    resource = resource.lower()
    if resource not in GTR_RESOURCE_KEYS:
        raise ValueError(f"Unsupported GtR resource '{resource}'.")
    key = GTR_RESOURCE_KEYS[resource]
    base_url = f"https://gtr.ukri.org/gtr/api/{resource}"
    output_dir = RAW_DIR / "gtr"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / (output_name or f"{resource}.ndjson")
    meta_file = output_dir / f"{output_file.stem}_meta.json"

    cutoff_ms = None
    if since_year is not None:
        cutoff_ms = int(datetime(since_year, 1, 1, tzinfo=timezone.utc).timestamp() * 1000)

    total_pages = None
    downloaded = 0
    start_page = 1
    file_mode = "w"
    existing_meta = None
    if resume and output_file.exists():
        if meta_file.exists():
            existing_meta = json.loads(meta_file.read_text())
            last_page = existing_meta.get("last_page")
            if existing_meta.get("status") == "completed":
                print("[gtr] existing download already marked completed; remove the meta file to restart.")
                return DownloadStats(
                    records=existing_meta.get("records_kept", 0),
                    pages=existing_meta.get("last_page", 0),
                    duration_s=0.0,
                )
            start_page = (last_page or 0) + 1
            downloaded = existing_meta.get("records_kept", 0)
            total_pages = existing_meta.get("total_pages_reported")
            print(f"[gtr] resuming from page {start_page}")
        else:
            raise FileNotFoundError(
                "Cannot resume without existing metadata. Remove the NDJSON file or rerun without --resume."
            )
        file_mode = "a"
    start_time = time.time()

    meta_state = {
        "resource": resource,
        "since_year": since_year,
        "fetch_size": fetch_size,
        "max_pages": max_pages,
        "records_kept": downloaded,
        "total_pages_reported": total_pages,
        "status": "in_progress",
        "last_page": start_page - 1,
        "downloaded_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ"),
    }
    meta_file.write_text(json.dumps(meta_state, indent=2))

    with output_file.open(file_mode, encoding="utf-8") as sink:
        page = start_page
        while True:
            if max_pages is not None and page > max_pages:
                break
            params = {
                "fetchSize": fetch_size,
                "size": fetch_size,
                "page": page,
            }
            payload = _request_json(base_url, params=params)
            batch = payload.get(key, [])
            if not isinstance(batch, list):
                batch = [batch]
            kept = 0
            for record in batch:
                if cutoff_ms and isinstance(record.get("start"), (int, float)):
                    if record["start"] < cutoff_ms:
                        continue
                sink.write(json.dumps(record))
                sink.write("\n")
                kept += 1
            downloaded += kept
            total_pages = payload.get("totalPages", total_pages)
            total_size = payload.get("totalSize")
            should_log = page == 1 or (log_every and page % log_every == 0)
            if should_log:
                print(
                    f"[gtr] page {page}/{total_pages or '?'} => kept {kept} records (total {downloaded})"
                )
            if total_pages is None:
                if not batch:
                    break
            else:
                if page >= total_pages:
                    break
            page += 1
            if delay:
                time.sleep(delay)
            meta_state.update(
                {
                    "records_kept": downloaded,
                    "total_pages_reported": total_pages,
                    "status": "in_progress",
                    "last_page": page - 1,
                }
            )
            meta_file.write_text(json.dumps(meta_state, indent=2))

    meta_state.update(
        {
            "records_kept": downloaded,
            "total_pages_reported": total_pages,
            "status": "completed",
            "last_page": page - 1,
        }
    )
    meta_file.write_text(json.dumps(meta_state, indent=2))
    duration = time.time() - start_time
    print(f"[gtr] wrote {downloaded} records to {output_file.relative_to(BASE_DIR)}")
    return DownloadStats(records=downloaded, pages=(page - 1), duration_s=duration)


def download_digital(extract: bool, overwrite: bool) -> None:
    for rel_path, url in DIGITAL_FILES.items():
        dest = RAW_DIR / rel_path
        _download_file(url, dest, overwrite=overwrite)
    if extract:
        import zipfile

        fixed_zip = RAW_DIR / "digital" / "fixed_coverage_full_fibre.zip"
        mobile_zip = RAW_DIR / "digital" / "mobile_coverage_all.zip"
        for archive, folder in (
            (fixed_zip, RAW_DIR / "digital" / "fixed"),
            (mobile_zip, RAW_DIR / "digital" / "mobile"),
        ):
            if not archive.exists():
                print(f"[warn] archive missing: {archive}")
                continue
            folder.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(archive) as zf:
                zf.extractall(folder)
            print(f"[ok] extracted {archive.name} -> {folder.relative_to(BASE_DIR)}")


def _build_oecd_key(countries: List[str]) -> str:
    refs = "+".join(countries)
    # REF_AREA . FREQ . MEASURE . SEO . FUNDMODE . TRANSCOORD . UNIT . PRICE
    parts = [refs, "A", "C", "", "_T", "_Z", "", ""]
    return ".".join(parts)


def _parse_sdmx_json(payload: Dict[str, Any]) -> pd.DataFrame:
    """Convert SDMX-JSON data (from OECD) into a tidy DataFrame."""

    structures = payload["data"]["structures"][0]
    series_dims = structures["dimensions"]["series"]
    obs_dims = structures["dimensions"]["observation"]
    dataset = payload["data"]["dataSets"][0]

    obs_dimension = obs_dims[0]
    time_values = obs_dimension["values"]

    rows: List[Dict[str, Any]] = []
    for key, series_data in dataset["series"].items():
        indices = [int(idx) for idx in key.split(":")]
        dim_values = {}
        for dim_meta, idx in zip(series_dims, indices):
            dim_values[dim_meta["id"]] = dim_meta["values"][idx]["id"]

        for obs_idx, values in series_data["observations"].items():
            obs_value = values[0]
            time_index = int(obs_idx)
            time_period = time_values[time_index]["id"]
            rows.append({**dim_values, "TIME_PERIOD": time_period, "value": obs_value})

    return pd.DataFrame(rows)


def download_msti_gbard(
    *,
    countries: List[str],
    start_year: int,
    end_year: int,
    output_stem: Optional[str],
) -> Dict[str, Path]:
    """Download GBARD-by-SEO data for the requested countries and years."""

    raw_dir = RAW_DIR / "msti"
    processed_dir = Path("data/processed")
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    key = _build_oecd_key(countries)
    params = {
        "startPeriod": str(start_year),
        "endPeriod": str(end_year),
        "dimensionAtObservation": "TIME_PERIOD",
        "detail": "dataonly",
    }
    headers = {"Accept": "application/vnd.sdmx.data+json;version=2.0"}
    url = f"{OECD_BASE_URL}/data/{OECD_GBARD_FLOW}/{key}"
    response = requests.get(url, params=params, headers=headers, timeout=120)
    response.raise_for_status()

    raw_name = output_stem or f"gbard_{start_year}_{end_year}.json"
    raw_path = raw_dir / raw_name
    raw_path.write_text(response.text)

    df = _parse_sdmx_json(response.json())
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"])

    # Focus on the most useful units (PPP dollars + % of GDP)
    df_filtered = df[df["UNIT_MEASURE"].isin(["USD_PPP", "XDC", "PT_B1GQ"])].copy()
    df_filtered["REF_AREA_NAME"] = df_filtered["REF_AREA"].map(REF_AREA_LABELS.get)

    csv_path = processed_dir / f"msti_gbard_{start_year}_{end_year}.csv"
    df_filtered.to_csv(csv_path, index=False)
    return {"raw": raw_path, "csv": csv_path}


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dataset downloader")
    subparsers = parser.add_subparsers(dest="command", required=True)

    gtr = subparsers.add_parser("gtr", help="Download Gateway to Research data")
    gtr.add_argument("--resource", default="projects", choices=sorted(GTR_RESOURCE_KEYS))
    gtr.add_argument("--since-year", type=int, default=None)
    gtr.add_argument("--fetch-size", type=int, default=200)
    gtr.add_argument("--max-pages", type=int, default=None, help="Limit pages for testing")
    gtr.add_argument("--delay", type=float, default=0.2, help="Delay between API calls (seconds)")
    gtr.add_argument("--resume", action="store_true", help="Resume from existing NDJSON/meta files")
    gtr.add_argument("--output-name", default=None, help="Override output filename")

    digital = subparsers.add_parser("digital", help="Download Ofcom digital infrastructure files")
    digital.add_argument("--extract", action="store_true", help="Unzip the downloaded archives")
    digital.add_argument("--overwrite", action="store_true", help="Re-download even if files exist")

    msti = subparsers.add_parser("msti", help="Download MSTI / GBARD extracts")
    msti.add_argument(
        "--countries",
        default="GBR,USA,DEU,FRA,JPN,CAN,ITA",
        help="Comma-separated ISO country codes to include",
    )
    msti.add_argument("--start-year", type=int, default=2010)
    msti.add_argument("--end-year", type=int, default=datetime.utcnow().year)
    msti.add_argument("--output-stem", default=None, help="Override raw JSON filename")

    return parser.parse_args(argv)


def main(argv: Optional[Iterable[str]] = None) -> None:
    args = parse_args(argv)
    if args.command == "gtr":
        stats = download_gtr(
            resource=args.resource,
            since_year=args.since_year,
            fetch_size=args.fetch_size,
            max_pages=args.max_pages,
            output_name=args.output_name,
            delay=args.delay,
            resume=args.resume,
        )
        print(
            f"[done] fetched {stats.records} {args.resource} rows across {stats.pages} pages in {stats.duration_s:.1f}s"
        )
    elif args.command == "digital":
        download_digital(extract=args.extract, overwrite=args.overwrite)
    elif args.command == "msti":
        countries = [c.strip().upper() for c in args.countries.split(",") if c.strip()]
        paths = download_msti_gbard(
            countries=countries,
            start_year=args.start_year,
            end_year=args.end_year,
            output_stem=args.output_stem,
        )
        print(
            "[done] downloaded MSTI GBARD data "
            f"(raw: {paths['raw']}, csv: {paths['csv']})"
        )
    else:
        raise ValueError(f"Unknown command {args.command}")


if __name__ == "__main__":
    main()
