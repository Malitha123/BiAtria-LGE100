from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

import nibabel as nib
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset

from common import resolve_paths


class BiAtriaLGE3DDataset(Dataset):
    """Load complete 3D BiAtria-LGE 100 image-label pairs."""

    def __init__(
        self,
        metadata: pd.DataFrame,
        data_root: Path,
        transform: Optional[Callable] = None,
    ) -> None:
        self.metadata = metadata.reset_index(drop=True).copy()
        self.data_root = Path(data_root)
        self.transform = transform

    def __len__(self) -> int:
        return len(self.metadata)

    @staticmethod
    def normalise_nonzero(image: np.ndarray) -> np.ndarray:
        image = image.astype(np.float32, copy=False)
        foreground = image != 0

        if not np.any(foreground):
            return image

        values = image[foreground]
        mean = float(values.mean())
        standard_deviation = max(float(values.std()), 1e-8)

        normalised = np.zeros_like(image, dtype=np.float32)
        normalised[foreground] = (values - mean) / standard_deviation
        return normalised

    def __getitem__(self, index: int) -> dict:
        row = self.metadata.iloc[index]
        image_path, label_path = resolve_paths(row, self.data_root)

        image_nifti = nib.load(str(image_path))
        label_nifti = nib.load(str(label_path))

        image = image_nifti.get_fdata(dtype=np.float32)
        label = np.asarray(label_nifti.dataobj, dtype=np.int64)

        if image.shape != label.shape:
            raise ValueError(
                f"Shape mismatch for {row['image_ID']}: "
                f"{image.shape} versus {label.shape}"
            )

        image = self.normalise_nonzero(image)

        # NIfTI array [H, W, D] to PyTorch [D, H, W].
        image = np.transpose(image, (2, 0, 1))
        label = np.transpose(label, (2, 0, 1))

        sample = {"image": image, "label": label}

        if self.transform is not None:
            sample = self.transform(sample)
            image = sample["image"]
            label = sample["label"]

        return {
            "image": torch.as_tensor(image, dtype=torch.float32).unsqueeze(0),
            "label": torch.as_tensor(label, dtype=torch.long),
            "patient_ID": row["patient_ID"],
            "image_taken": row["image_taken"],
            "image_ID": row["image_ID"],
            "label_ID": row["label_ID"],
            "affine": torch.as_tensor(image_nifti.affine, dtype=torch.float64),
        }
