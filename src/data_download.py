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
from typing import Dict, Iterable, Optional

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


@dataclass
class DownloadStats:
    records: int
    pages: int
    duration_s: float


def _request_json(url: str, params: Optional[dict] = None) -> dict:
    response = requests.get(
        url,
        params=params,
        headers={"Accept": "application/json"},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


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
    page = 1
    start_time = time.time()

    with output_file.open("w", encoding="utf-8") as sink:
        while True:
            if max_pages is not None and page > max_pages:
                break
            params = {
                "fetchSize": fetch_size,
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
            time.sleep(0.5)

    metadata = {
        "resource": resource,
        "since_year": since_year,
        "fetch_size": fetch_size,
        "max_pages": max_pages,
        "records_kept": downloaded,
        "total_pages_reported": total_pages,
        "downloaded_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ"),
    }
    meta_file.write_text(json.dumps(metadata, indent=2))
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


def download_msti_gbard(*, placeholder: bool = False) -> None:
    """Placeholder for the MSTI download flow.

    The OECD SDMX endpoint occasionally changes the expected key ordering. The
    recommendation from the Gemini strategy is to pull GBARD by socio-economic
    objective (NABS 2007) for the UK plus comparator countries, then persist the
    flattened CSV under `data/raw/msti/`.

    Until the exact SDMX query is nailed, this function simply raises with a
    helpful message so the developer running the script knows what to do next.
    """

    raise NotImplementedError(
        "MSTI / GBARD download not implemented yet. Use the OECD Data Explorer to "
        "export the required table, then drop the CSV into data/raw/msti/ along "
        "with a MANIFEST.md describing the query."
    )


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dataset downloader")
    subparsers = parser.add_subparsers(dest="command", required=True)

    gtr = subparsers.add_parser("gtr", help="Download Gateway to Research data")
    gtr.add_argument("--resource", default="projects", choices=sorted(GTR_RESOURCE_KEYS))
    gtr.add_argument("--since-year", type=int, default=None)
    gtr.add_argument("--fetch-size", type=int, default=200)
    gtr.add_argument("--max-pages", type=int, default=None, help="Limit pages for testing")
    gtr.add_argument("--output-name", default=None, help="Override output filename")

    digital = subparsers.add_parser("digital", help="Download Ofcom digital infrastructure files")
    digital.add_argument("--extract", action="store_true", help="Unzip the downloaded archives")
    digital.add_argument("--overwrite", action="store_true", help="Re-download even if files exist")

    msti = subparsers.add_parser("msti", help="Download MSTI / GBARD extracts")
    msti.add_argument("--run", action="store_true", help="Explicitly acknowledge the placeholder")

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
        )
        print(
            f"[done] fetched {stats.records} {args.resource} rows across {stats.pages} pages in {stats.duration_s:.1f}s"
        )
    elif args.command == "digital":
        download_digital(extract=args.extract, overwrite=args.overwrite)
    elif args.command == "msti":
        download_msti_gbard()
    else:
        raise ValueError(f"Unknown command {args.command}")


if __name__ == "__main__":
    main()
