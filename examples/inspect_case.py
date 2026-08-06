from __future__ import annotations

import argparse
from pathlib import Path

import nibabel as nib
import numpy as np


VALID_LABELS = {0, 1, 2, 3, 4}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect one BiAtria-LGE 100 case.")
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--cohort", choices=["Utah", "Waikato"], required=True)
    parser.add_argument("--case-id", required=True, help="Case number, for example 0090")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    image_path = (
        args.data_root
        / args.cohort
        / "images"
        / f"{args.cohort}_image_{args.case_id}.nii.gz"
    )
    label_path = (
        args.data_root
        / args.cohort
        / "labels"
        / f"{args.cohort}_label_{args.case_id}.nii.gz"
    )

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    if not label_path.exists():
        raise FileNotFoundError(f"Label not found: {label_path}")

    image_nifti = nib.load(str(image_path))
    label_nifti = nib.load(str(label_path))

    image = image_nifti.get_fdata(dtype=np.float32)
    label = np.asarray(label_nifti.dataobj, dtype=np.uint8)

    observed_labels = set(np.unique(label).tolist())

    print(f"Image: {image_path}")
    print(f"Label: {label_path}")
    print(f"Image shape: {image.shape}")
    print(f"Label shape: {label.shape}")
    print(f"Image dtype: {image.dtype}")
    print(f"Label dtype: {label.dtype}")
    print(f"Voxel spacing: {image_nifti.header.get_zooms()[:3]}")
    print(f"Orientation: {nib.aff2axcodes(image_nifti.affine)}")
    print(f"Image intensity range: {float(image.min())} to {float(image.max())}")
    print(f"Observed labels: {sorted(observed_labels)}")

    if image.shape != label.shape:
        raise ValueError("Image and label shapes do not match.")

    if not np.allclose(image_nifti.affine, label_nifti.affine, atol=1e-5):
        raise ValueError("Image and label affine matrices do not match.")

    if not observed_labels.issubset(VALID_LABELS):
        raise ValueError(f"Unexpected label values: {sorted(observed_labels)}")

    print("Status: valid image-label pair")


if __name__ == "__main__":
    main()
