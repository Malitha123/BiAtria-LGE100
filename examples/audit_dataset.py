from __future__ import annotations

import argparse
from pathlib import Path

import nibabel as nib
import numpy as np
import pandas as pd

from common import load_metadata, resolve_paths


VALID_LABELS = {0, 1, 2, 3, 4}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit BiAtria-LGE 100.")
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("BiAtria_LGE100_audit.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metadata = load_metadata(args.data_root)

    duplicate_image_ids = metadata.loc[
        metadata["image_ID"].duplicated(keep=False), "image_ID"
    ].tolist()
    duplicate_label_ids = metadata.loc[
        metadata["label_ID"].duplicated(keep=False), "label_ID"
    ].tolist()

    if duplicate_image_ids:
        raise ValueError(f"Duplicate image IDs: {duplicate_image_ids}")
    if duplicate_label_ids:
        raise ValueError(f"Duplicate label IDs: {duplicate_label_ids}")

    split_counts = metadata.groupby("patient_ID")["Split"].nunique()
    leaking_patients = split_counts[split_counts > 1].index.tolist()

    if leaking_patients:
        raise ValueError(f"Patients occur in multiple splits: {leaking_patients}")

    records = []

    for row_index, row in metadata.iterrows():
        image_path, label_path = resolve_paths(row, args.data_root)

        record = {
            "row": row_index,
            "patient_ID": row["patient_ID"],
            "image_ID": row["image_ID"],
            "label_ID": row["label_ID"],
            "image_exists": image_path.exists(),
            "label_exists": label_path.exists(),
            "shape_match": False,
            "affine_match": False,
            "labels_valid": False,
            "observed_labels": "",
            "status": "error",
            "error": "",
        }

        if not image_path.exists() or not label_path.exists():
            record["error"] = "Missing image or label file"
            records.append(record)
            continue

        try:
            image_nifti = nib.load(str(image_path))
            label_nifti = nib.load(str(label_path))

            observed_labels = set(
                np.unique(np.asarray(label_nifti.dataobj)).tolist()
            )

            record["shape_match"] = image_nifti.shape == label_nifti.shape
            record["affine_match"] = np.allclose(
                image_nifti.affine,
                label_nifti.affine,
                atol=1e-5,
            )
            record["labels_valid"] = observed_labels.issubset(VALID_LABELS)
            record["observed_labels"] = ",".join(
                str(value) for value in sorted(observed_labels)
            )

            if (
                record["shape_match"]
                and record["affine_match"]
                and record["labels_valid"]
            ):
                record["status"] = "ok"
            else:
                record["error"] = "One or more validation checks failed"

        except Exception as exc:
            record["error"] = f"{type(exc).__name__}: {exc}"

        records.append(record)

    audit = pd.DataFrame(records)
    audit.to_csv(args.output, index=False)

    print(f"Audited rows: {len(audit)}")
    print(f"Valid rows: {(audit['status'] == 'ok').sum()}")
    print(f"Rows requiring review: {(audit['status'] != 'ok').sum()}")
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
