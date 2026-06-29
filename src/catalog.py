"""Catalog loading helpers."""

from __future__ import annotations

import json
from pathlib import Path

from src.models import DatasetRecord


DEFAULT_CATALOG_PATH = Path("data/processed/seed_catalog.json")


def load_catalog(path: Path | str = DEFAULT_CATALOG_PATH) -> list[DatasetRecord]:
    catalog_path = Path(path)
    with catalog_path.open("r", encoding="utf-8") as file:
        raw_records = json.load(file)
    return [DatasetRecord.from_dict(record) for record in raw_records]


def group_by_canonical_id(
    records: list[DatasetRecord],
) -> dict[str, list[DatasetRecord]]:
    grouped: dict[str, list[DatasetRecord]] = {}
    for record in records:
        grouped.setdefault(record.canonical_dataset_id, []).append(record)
    return grouped
