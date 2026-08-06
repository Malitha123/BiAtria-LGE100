from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Visualise one BiAtria-LGE 100 case.")
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--cohort", choices=["Utah", "Waikato"], required=True)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--output", type=Path, default=Path("overlay.png"))
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

    image = nib.load(str(image_path)).get_fdata(dtype=np.float32)
    label = np.asarray(nib.load(str(label_path)).dataobj, dtype=np.uint8)

    labelled_voxels_per_slice = np.count_nonzero(label, axis=(0, 1))
    z_index = int(np.argmax(labelled_voxels_per_slice))

    image_slice = np.rot90(image[:, :, z_index])
    label_slice = np.rot90(label[:, :, z_index])

    foreground = image_slice[image_slice > 0]
    if foreground.size:
        display_min, display_max = np.percentile(foreground, [1.0, 99.5])
    else:
        display_min, display_max = image_slice.min(), image_slice.max()

    masked_label = np.ma.masked_where(label_slice == 0, label_slice)

    plt.figure(figsize=(8, 8))
    plt.imshow(
        image_slice,
        cmap="gray",
        vmin=display_min,
        vmax=display_max,
    )
    overlay = plt.imshow(
        masked_label,
        cmap="tab10",
        alpha=0.45,
        vmin=0,
        vmax=4,
    )

    colour_bar = plt.colorbar(overlay, ticks=[1, 2, 3, 4])
    colour_bar.ax.set_yticklabels(
        [
            "Right atrial wall",
            "Left atrial wall",
            "Right atrial cavity",
            "Left atrial cavity",
        ]
    )

    plt.title(f"{args.cohort} case {args.case_id}, axial slice {z_index}")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(args.output, dpi=200, bbox_inches="tight")
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
