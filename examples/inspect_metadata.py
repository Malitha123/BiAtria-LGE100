from __future__ import annotations

import argparse
from pathlib import Path

from common import load_metadata


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect BiAtria-LGE 100 metadata.")
    parser.add_argument("--data-root", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metadata = load_metadata(args.data_root)

    print("First rows:")
    print(metadata.head().to_string(index=False))

    print("\nScans by split:")
    print(metadata.groupby("Split").size().to_string())

    print("\nPatients by split:")
    print(metadata.groupby("Split")["patient_ID"].nunique().to_string())

    print("\nScans by timepoint:")
    print(
        metadata.groupby("image_taken")
        .size()
        .sort_values(ascending=False)
        .to_string()
    )


if __name__ == "__main__":
    main()
