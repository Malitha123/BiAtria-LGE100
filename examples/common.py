from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def add_nifti_extension(identifier: str) -> str:
    """Return an identifier with a .nii.gz extension."""
    return identifier if identifier.endswith(".nii.gz") else f"{identifier}.nii.gz"


def infer_cohort(identifier: str) -> str:
    """Infer Utah or Waikato from an image or label identifier."""
    cohort = identifier.split("_", maxsplit=1)[0]
    if cohort not in {"Utah", "Waikato"}:
        raise ValueError(f"Cannot infer cohort from identifier: {identifier}")
    return cohort


def resolve_paths(row: Any, data_root: Path) -> tuple[Path, Path]:
    """Resolve image and label paths for one metadata row."""
    cohort = infer_cohort(str(row["image_ID"]))

    image_path = (
        data_root
        / cohort
        / "images"
        / add_nifti_extension(str(row["image_ID"]))
    )
    label_path = (
        data_root
        / cohort
        / "labels"
        / add_nifti_extension(str(row["label_ID"]))
    )
    return image_path, label_path


def load_metadata(data_root: Path) -> pd.DataFrame:
    """Load and normalise patient_image_mapping.csv."""
    metadata_path = data_root / "patient_image_mapping.csv"
    if not metadata_path.exists():
        raise FileNotFoundError(f"Metadata file not found: {metadata_path}")

    metadata = pd.read_csv(metadata_path)

    required_columns = {
        "patient_ID",
        "image_taken",
        "image_ID",
        "label_ID",
        "Split",
    }
    missing_columns = required_columns.difference(metadata.columns)
    if missing_columns:
        raise ValueError(
            f"Metadata is missing required columns: {sorted(missing_columns)}"
        )

    metadata["Split"] = metadata["Split"].astype(str).str.strip().str.lower()
    metadata["image_taken"] = (
        metadata["image_taken"].astype(str).str.strip().str.lower()
    )
    return metadata
