BiAtria-LGE 100
A Multi-Centre 3D LGE-MRI Dataset for Bi-Atrial Wall and Cavity Segmentation in Atrial Fibrillation
BiAtria-LGE 100 is a curated multi-centre cardiac magnetic resonance imaging dataset for automated segmentation of the left and right atrial walls and cavities.
The dataset contains 100 paired three-dimensional late gadolinium enhancement magnetic resonance imaging volumes and corresponding multi-class segmentation masks.
Utah cohort: 91 image-mask pairs
Waikato cohort: 9 image-mask pairs
Format: compressed NIfTI, `.nii.gz`
Task: five-class voxel-wise segmentation, including background
Approximate Figshare download size: 1.39 GB
Recommended use: non-clinical research and method development
> The Figshare record is currently private. Replace the access and DOI placeholders in this README when the public or controlled-access record is released.
<p align="center">
  <img src="docs/images/Utah_image_0090_axial_slices.png" alt="Representative axial LGE-MRI slices from Utah_image_0090" width="100%">
</p>
<p align="center">
  Representative axial slices from <code>Utah_image_0090.nii.gz</code>. The display intensity has been clipped using robust percentiles for visualisation only.
</p>
Contents
Dataset overview
Dataset composition
Segmentation labels
Directory structure
Metadata
Installation
Quick start
Read an image and label
Access the metadata
Visualise an image and segmentation
Validate the dataset
Create a patient-level validation split
PyTorch dataset example
Calculate class-wise Dice scores
Calculate anatomical volumes
Preprocessing recommendations
Recommended experimental protocol
Intended and potential future uses
Known limitations
Ethics and responsible use
Citation
Related material
Licence and access
Contact
Dataset overview
The Utah cohort contains longitudinal imaging from 38 de-identified patients, with examinations acquired before treatment and at several post-treatment follow-up timepoints.
The supplied Utah metadata define a patient-level development split:
Partition	Patients	Image-mask pairs
Utah training	31	73
Utah test	7	18
Total Utah	38	91
Waikato cohort	To be confirmed from cohort metadata	9
Total dataset		100
No Utah patient appears in both the supplied training and test partitions.
The two-cohort structure supports:
supervised multi-class segmentation;
longitudinal analysis;
cross-cohort evaluation;
external validation;
domain adaptation and generalisation;
uncertainty estimation;
model calibration;
automated segmentation quality control.
Dataset composition
Utah cohort
The Utah cohort contains 91 paired LGE-MRI images and segmentation masks from 38 de-identified patients.
Available acquisition timepoints include:
pre-treatment;
3 months;
4 months;
6 months;
7 months;
8 months;
9 months;
11 months.
Supplied Utah training partition
Patients: `patient_ID_005` to `patient_ID_035`
Number of patients: 31
Number of image-mask pairs: 73
Supplied Utah test partition
Patients: `patient_ID_001` to `patient_ID_004`
Patients: `patient_ID_036` to `patient_ID_038`
Number of patients: 7
Number of image-mask pairs: 18
The split is defined at the patient level. All longitudinal scans from one patient remain in the same partition.
Waikato cohort
The Waikato cohort contains nine paired LGE-MRI images and segmentation masks.
The cohort may be used for external or cross-cohort evaluation. Researchers must state whether Waikato data were used for:
training;
hyperparameter selection;
preprocessing optimisation;
model selection;
threshold selection;
probability calibration;
domain adaptation;
validation;
final external testing.
Do not describe Waikato as an independent external test cohort when it has influenced model development.
Image geometry
Common and additional geometries observed in the dataset include:
Geometry	Notes
`640 x 640 x 44` voxels	Common geometry
`576 x 576 x 44` voxels	Additional Utah geometry
`0.625 x 0.625 x 2.5 mm`	Reported voxel spacing
The supplied example file, `Utah_image_0090.nii.gz`, was verified as:
Property	Value
Shape	`576 x 576 x 44`
Data type	`uint16`
Voxel spacing	`0.625 x 0.625 x 2.5 mm`
Orientation from affine	`LPS`
Geometry, orientation, affine transforms, voxel spacing, and data type should still be checked for every image-label pair.
Segmentation labels
The segmentation masks contain integer-encoded voxel labels.
Voxel value	Anatomical structure
0	Background
1	Right atrial wall
2	Left atrial wall
3	Right atrial cavity
4	Left atrial cavity
Valid label values are:
```python
VALID_LABELS = {0, 1, 2, 3, 4}
```
Use nearest-neighbour interpolation whenever a segmentation mask is resampled. Linear, cubic, or spline interpolation can create invalid intermediate class values.
Directory structure
The examples in this README assume the following structure:
```text
Bi_Atrial_Segmentation_Data/
├── Utah/
│   ├── images/
│   │   ├── Utah_image_0001.nii.gz
│   │   ├── Utah_image_0002.nii.gz
│   │   └── ...
│   └── labels/
│       ├── Utah_label_0001.nii.gz
│       ├── Utah_label_0002.nii.gz
│       └── ...
├── Waikato/
│   ├── images/
│   │   ├── Waikato_image_0001.nii.gz
│   │   └── ...
│   └── labels/
│       ├── Waikato_label_0001.nii.gz
│       └── ...
└── patient_image_mapping.csv
```
The filename identifiers in `patient_image_mapping.csv` do not include the `.nii.gz` extension.
Metadata
The supplied CSV uses the following columns:
Column	Description
`patient_ID`	De-identified patient identifier
`image_taken`	Relative acquisition timepoint, such as `pre`, `3mo`, or `11mo`
`image_ID`	Image identifier without the `.nii.gz` extension
`label_ID`	Segmentation-mask identifier without the `.nii.gz` extension
`Split`	Supplied patient-level partition, `Train` or `Test`
Example:
```csv
patient_ID,image_taken,image_ID,label_ID,Split
patient_ID_001,pre,Utah_image_0001,Utah_label_0001,Test
patient_ID_001,3mo,Utah_image_0002,Utah_label_0002,Test
patient_ID_005,pre,Utah_image_0013,Utah_label_0013,Train
```
The current mapping describes the Utah cohort. Add corresponding Waikato rows to a future metadata release if patient-level Waikato mapping can be shared.
Recommended additional metadata fields include:
`cohort`;
`image_path`;
`label_path`;
`scanner_vendor`, when permitted;
`scanner_model`, when permitted;
`field_strength`, when permitted;
`acquisition_protocol`, when permitted;
`sex`, age group, and other subgroup variables, when ethically and legally permitted;
`release_version`;
`quality_control_status`.
Installation
Create a Python environment and install the basic dependencies:
```bash
python -m venv .venv
```
Activate the environment.
Linux or macOS:
```bash
source .venv/bin/activate
```
Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```
Install the dependencies:
```bash
python -m pip install --upgrade pip
python -m pip install nibabel numpy pandas matplotlib scikit-learn torch
```
For basic inspection only, the minimum packages are:
```bash
python -m pip install nibabel numpy pandas matplotlib
```
Quick start
```python
from pathlib import Path

DATA_ROOT = Path("Bi_Atrial_Segmentation_Data")
METADATA_PATH = DATA_ROOT / "patient_image_mapping.csv"

assert DATA_ROOT.exists(), f"Dataset directory not found: {DATA_ROOT}"
assert METADATA_PATH.exists(), f"Metadata file not found: {METADATA_PATH}"
```
Read an image and label
```python
from pathlib import Path

import nibabel as nib
import numpy as np

DATA_ROOT = Path("Bi_Atrial_Segmentation_Data")

image_path = DATA_ROOT / "Utah" / "images" / "Utah_image_0090.nii.gz"
label_path = DATA_ROOT / "Utah" / "labels" / "Utah_label_0090.nii.gz"

image_nifti = nib.load(str(image_path))
label_nifti = nib.load(str(label_path))

# Load the image as float32.
image = image_nifti.get_fdata(dtype=np.float32)

# Preserve integer class values in the label.
label = np.asarray(label_nifti.dataobj, dtype=np.uint8)

print("Image shape:", image.shape)
print("Label shape:", label.shape)
print("Image dtype:", image.dtype)
print("Label dtype:", label.dtype)
print("Voxel spacing:", image_nifti.header.get_zooms()[:3])
print("Orientation:", nib.aff2axcodes(image_nifti.affine))
print("Image intensity range:", float(image.min()), float(image.max()))
print("Label values:", np.unique(label))
```
Verify that the image and label occupy the same voxel grid:
```python
if image.shape != label.shape:
    raise ValueError(
        f"Image-label shape mismatch: image={image.shape}, label={label.shape}"
    )

if not np.allclose(image_nifti.affine, label_nifti.affine, atol=1e-5):
    raise ValueError("Image and label affine matrices do not match.")

valid_labels = {0, 1, 2, 3, 4}
observed_labels = set(np.unique(label).tolist())

if not observed_labels.issubset(valid_labels):
    raise ValueError(f"Unexpected label values: {sorted(observed_labels)}")
```
Inspect the complete NIfTI header
```python
print(image_nifti.header)
```
Access selected header fields
```python
header = image_nifti.header

print("Dimensions:", tuple(int(v) for v in header["dim"][1:4]))
print("Voxel spacing:", tuple(float(v) for v in header["pixdim"][1:4]))
print("NIfTI datatype:", header.get_data_dtype())
print("qform code:", int(header["qform_code"]))
print("sform code:", int(header["sform_code"]))
print("Affine matrix:\n", image_nifti.affine)
```
Access the metadata
```python
from pathlib import Path

import pandas as pd

DATA_ROOT = Path("Bi_Atrial_Segmentation_Data")
metadata = pd.read_csv(DATA_ROOT / "patient_image_mapping.csv")

print(metadata.head())
print(metadata.columns.tolist())
print(metadata.shape)
```
Normalise the split and timepoint fields
```python
metadata["Split"] = metadata["Split"].str.strip().str.lower()
metadata["image_taken"] = metadata["image_taken"].str.strip().str.lower()
```
Count scans and patients by split
```python
scan_counts = metadata.groupby("Split").size()
patient_counts = metadata.groupby("Split")["patient_ID"].nunique()

print("Scans by split:")
print(scan_counts)

print("\nPatients by split:")
print(patient_counts)
```
Expected Utah counts:
```text
train: 73 scans from 31 patients
test: 18 scans from 7 patients
```
List the scans for one patient
```python
patient_id = "patient_ID_001"

patient_rows = (
    metadata.loc[metadata["patient_ID"] == patient_id]
    .sort_values("image_taken")
    .reset_index(drop=True)
)

print(patient_rows)
```
Count scans by acquisition timepoint
```python
timepoint_counts = (
    metadata.groupby("image_taken")
    .size()
    .sort_values(ascending=False)
)

print(timepoint_counts)
```
Resolve image and label paths from the CSV
```python
from pathlib import Path

def infer_cohort(identifier: str) -> str:
    """Infer Utah or Waikato from an identifier such as Utah_image_0001."""
    cohort = identifier.split("_", maxsplit=1)[0]
    if cohort not in {"Utah", "Waikato"}:
        raise ValueError(f"Cannot infer cohort from identifier: {identifier}")
    return cohort

def add_nifti_extension(identifier: str) -> str:
    if identifier.endswith(".nii.gz"):
        return identifier
    return f"{identifier}.nii.gz"

def resolve_paths(row, data_root: Path) -> tuple[Path, Path]:
    cohort = infer_cohort(row["image_ID"])

    image_path = (
        data_root
        / cohort
        / "images"
        / add_nifti_extension(row["image_ID"])
    )
    label_path = (
        data_root
        / cohort
        / "labels"
        / add_nifti_extension(row["label_ID"])
    )

    return image_path, label_path
```
Use it for one row:
```python
row = metadata.iloc[0]
image_path, label_path = resolve_paths(row, DATA_ROOT)

print(image_path)
print(label_path)
print("Image exists:", image_path.exists())
print("Label exists:", label_path.exists())
```
Add the resolved paths to the DataFrame:
```python
resolved = metadata.apply(
    lambda row: resolve_paths(row, DATA_ROOT),
    axis=1,
)

metadata[["image_path", "label_path"]] = pd.DataFrame(
    resolved.tolist(),
    index=metadata.index,
)

print(metadata.head())
```
Visualise an image and segmentation
Display one axial image slice
```python
import matplotlib.pyplot as plt
import numpy as np

z_index = image.shape[2] // 2
image_slice = np.rot90(image[:, :, z_index])

foreground = image_slice[image_slice > 0]
if foreground.size:
    display_min, display_max = np.percentile(foreground, [1.0, 99.5])
else:
    display_min, display_max = image_slice.min(), image_slice.max()

plt.figure(figsize=(7, 7))
plt.imshow(
    image_slice,
    cmap="gray",
    vmin=display_min,
    vmax=display_max,
)
plt.title(f"Axial LGE-MRI slice, z={z_index}")
plt.axis("off")
plt.tight_layout()
plt.show()
```
Overlay the segmentation mask
```python
import matplotlib.pyplot as plt
import numpy as np

z_index = image.shape[2] // 2

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

plt.title(f"Image and segmentation overlay, z={z_index}")
plt.axis("off")
plt.tight_layout()
plt.show()
```
Automatically select a slice containing the most labelled voxels
```python
labelled_voxels_per_slice = np.count_nonzero(label, axis=(0, 1))
z_index = int(np.argmax(labelled_voxels_per_slice))

print("Selected slice:", z_index)
print("Labelled voxels:", int(labelled_voxels_per_slice[z_index]))
```
Validate the dataset
The following audit checks:
missing image or label files;
duplicate image or label identifiers;
image-label shape mismatches;
affine mismatches;
unexpected label values;
patient leakage across supplied partitions;
unreadable NIfTI files.
```python
from pathlib import Path

import nibabel as nib
import numpy as np
import pandas as pd

VALID_LABELS = {0, 1, 2, 3, 4}

def audit_dataset(data_root: Path) -> pd.DataFrame:
    metadata_path = data_root / "patient_image_mapping.csv"
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
            f"Metadata is missing columns: {sorted(missing_columns)}"
        )

    if metadata["image_ID"].duplicated().any():
        duplicates = metadata.loc[
            metadata["image_ID"].duplicated(keep=False),
            "image_ID",
        ].tolist()
        raise ValueError(f"Duplicate image IDs: {duplicates}")

    if metadata["label_ID"].duplicated().any():
        duplicates = metadata.loc[
            metadata["label_ID"].duplicated(keep=False),
            "label_ID",
        ].tolist()
        raise ValueError(f"Duplicate label IDs: {duplicates}")

    split_count_per_patient = (
        metadata.assign(
            normalised_split=metadata["Split"].str.strip().str.lower()
        )
        .groupby("patient_ID")["normalised_split"]
        .nunique()
    )

    leaking_patients = split_count_per_patient[
        split_count_per_patient > 1
    ].index.tolist()

    if leaking_patients:
        raise ValueError(
            f"Patients occur in multiple splits: {leaking_patients}"
        )

    records = []

    for row_index, row in metadata.iterrows():
        image_path, label_path = resolve_paths(row, data_root)

        record = {
            "row": row_index,
            "patient_ID": row["patient_ID"],
            "image_ID": row["image_ID"],
            "label_ID": row["label_ID"],
            "image_exists": image_path.exists(),
            "label_exists": label_path.exists(),
            "readable": False,
            "shape_match": False,
            "affine_match": False,
            "labels_valid": False,
            "image_shape": None,
            "label_shape": None,
            "observed_labels": None,
            "error": None,
        }

        if not image_path.exists() or not label_path.exists():
            record["error"] = "Missing image or label file"
            records.append(record)
            continue

        try:
            image_nifti = nib.load(str(image_path))
            label_nifti = nib.load(str(label_path))

            image_shape = tuple(image_nifti.shape)
            label_shape = tuple(label_nifti.shape)
            observed_labels = set(
                np.unique(np.asarray(label_nifti.dataobj)).tolist()
            )

            record["readable"] = True
            record["image_shape"] = image_shape
            record["label_shape"] = label_shape
            record["shape_match"] = image_shape == label_shape
            record["affine_match"] = np.allclose(
                image_nifti.affine,
                label_nifti.affine,
                atol=1e-5,
            )
            record["observed_labels"] = sorted(observed_labels)
            record["labels_valid"] = observed_labels.issubset(VALID_LABELS)

        except Exception as exc:
            record["error"] = f"{type(exc).__name__}: {exc}"

        records.append(record)

    return pd.DataFrame(records)
```
Run the audit:
```python
audit = audit_dataset(DATA_ROOT)
audit.to_csv("BiAtria_LGE100_audit.csv", index=False)

problem_rows = audit.loc[
    ~(
        audit["image_exists"]
        & audit["label_exists"]
        & audit["readable"]
        & audit["shape_match"]
        & audit["affine_match"]
        & audit["labels_valid"]
    )
]

print(f"Audited rows: {len(audit)}")
print(f"Rows requiring review: {len(problem_rows)}")

if not problem_rows.empty:
    print(problem_rows.to_string(index=False))
```
Create a patient-level validation split
The supplied Utah metadata contain training and test partitions, but no separate validation partition.
When a validation set is needed, split only the supplied training patients. Do not divide scans from one patient across training and validation.
```python
from sklearn.model_selection import GroupShuffleSplit

metadata = pd.read_csv(DATA_ROOT / "patient_image_mapping.csv")
metadata["Split"] = metadata["Split"].str.strip().str.lower()

development = metadata.loc[metadata["Split"] == "train"].reset_index(drop=True)

splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.20,
    random_state=42,
)

train_indices, validation_indices = next(
    splitter.split(
        development,
        groups=development["patient_ID"],
    )
)

training_metadata = development.iloc[train_indices].reset_index(drop=True)
validation_metadata = development.iloc[validation_indices].reset_index(drop=True)

training_patients = set(training_metadata["patient_ID"])
validation_patients = set(validation_metadata["patient_ID"])

assert training_patients.isdisjoint(validation_patients)

print(
    f"Training: {len(training_metadata)} scans, "
    f"{len(training_patients)} patients"
)
print(
    f"Validation: {len(validation_metadata)} scans, "
    f"{len(validation_patients)} patients"
)
```
The held-out Utah test partition and Waikato cohort should not be used to choose model architecture, preprocessing, thresholds, stopping criteria, or calibration parameters when they are intended for final evaluation.
PyTorch dataset example
This example loads complete 3D volumes and returns tensors in the PyTorch convention `[channels, depth, height, width]`.
```python
from pathlib import Path
from typing import Callable, Optional

import nibabel as nib
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset

class BiAtriaLGE3DDataset(Dataset):
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

        mean = float(image[foreground].mean())
        standard_deviation = float(image[foreground].std())

        if standard_deviation < 1e-8:
            standard_deviation = 1.0

        normalised = np.zeros_like(image, dtype=np.float32)
        normalised[foreground] = (
            image[foreground] - mean
        ) / standard_deviation

        return normalised

    def __getitem__(self, index: int):
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

        # Convert [height, width, depth] to [depth, height, width].
        image = np.transpose(image, (2, 0, 1))
        label = np.transpose(label, (2, 0, 1))

        sample = {
            "image": image,
            "label": label,
        }

        if self.transform is not None:
            sample = self.transform(sample)
            image = sample["image"]
            label = sample["label"]

        image_tensor = torch.as_tensor(
            image,
            dtype=torch.float32,
        ).unsqueeze(0)

        label_tensor = torch.as_tensor(
            label,
            dtype=torch.long,
        )

        return {
            "image": image_tensor,
            "label": label_tensor,
            "patient_ID": row["patient_ID"],
            "image_taken": row["image_taken"],
            "image_ID": row["image_ID"],
            "label_ID": row["label_ID"],
            "affine": torch.as_tensor(
                image_nifti.affine,
                dtype=torch.float64,
            ),
        }
```
Use the loader:
```python
metadata = pd.read_csv(DATA_ROOT / "patient_image_mapping.csv")
metadata["Split"] = metadata["Split"].str.strip().str.lower()

training_rows = metadata.loc[metadata["Split"] == "train"]

dataset = BiAtriaLGE3DDataset(
    metadata=training_rows,
    data_root=DATA_ROOT,
)

sample = dataset[0]

print("Image tensor:", sample["image"].shape)
print("Label tensor:", sample["label"].shape)
print("Patient:", sample["patient_ID"])
print("Timepoint:", sample["image_taken"])
```
A `DataLoader` can then be created:
```python
from torch.utils.data import DataLoader

loader = DataLoader(
    dataset,
    batch_size=1,
    shuffle=True,
    num_workers=4,
    pin_memory=True,
)

batch = next(iter(loader))

print("Batch image shape:", batch["image"].shape)
print("Batch label shape:", batch["label"].shape)
```
The original in-plane size is large. Full-volume 3D training may require patch-based sampling, mixed precision, gradient accumulation, or batch size 1 depending on GPU memory.
Calculate class-wise Dice scores
```python
import numpy as np

CLASS_NAMES = {
    0: "Background",
    1: "Right atrial wall",
    2: "Left atrial wall",
    3: "Right atrial cavity",
    4: "Left atrial cavity",
}

def dice_per_class(
    prediction: np.ndarray,
    target: np.ndarray,
    class_ids=(1, 2, 3, 4),
    epsilon: float = 1e-8,
) -> dict[str, float]:
    if prediction.shape != target.shape:
        raise ValueError(
            f"Shape mismatch: {prediction.shape} versus {target.shape}"
        )

    scores = {}

    for class_id in class_ids:
        predicted_class = prediction == class_id
        target_class = target == class_id

        intersection = np.logical_and(
            predicted_class,
            target_class,
        ).sum()

        denominator = (
            predicted_class.sum()
            + target_class.sum()
        )

        if denominator == 0:
            score = float("nan")
        else:
            score = float(
                (2.0 * intersection + epsilon)
                / (denominator + epsilon)
            )

        scores[CLASS_NAMES[class_id]] = score

    return scores
```
Example:
```python
scores = dice_per_class(
    prediction=predicted_label,
    target=label,
)

for class_name, score in scores.items():
    print(f"{class_name}: {score:.4f}")
```
Report each foreground class separately. A pooled or macro-average score should not replace class-wise results.
Calculate anatomical volumes
Voxel counts can be converted to physical volume using the NIfTI voxel spacing.
```python
import numpy as np

spacing_mm = image_nifti.header.get_zooms()[:3]
voxel_volume_mm3 = float(np.prod(spacing_mm))

class_volumes_ml = {}

for class_id, class_name in CLASS_NAMES.items():
    if class_id == 0:
        continue

    voxel_count = int(np.count_nonzero(label == class_id))
    volume_mm3 = voxel_count * voxel_volume_mm3
    volume_ml = volume_mm3 / 1000.0

    class_volumes_ml[class_name] = volume_ml

for class_name, volume_ml in class_volumes_ml.items():
    print(f"{class_name}: {volume_ml:.2f} mL")
```
These values describe the segmented regions. They must not be interpreted as clinically validated measurements without appropriate methodological and clinical validation.
Preprocessing recommendations
Researchers should document every preprocessing operation. At minimum, report:
orientation standardisation;
voxel-spacing resampling;
image interpolation method;
mask interpolation method;
intensity clipping;
intensity normalisation;
cropping or padding;
patch or slice extraction;
data augmentation;
postprocessing;
handling of empty classes;
handling of varying in-plane dimensions.
Orientation
Use the affine matrix rather than assuming that all arrays use the same anatomical orientation.
```python
import nibabel as nib

canonical_image = nib.as_closest_canonical(image_nifti)
canonical_label = nib.as_closest_canonical(label_nifti)
```
Apply equivalent spatial operations to the image and label, then verify alignment.
Intensity normalisation
LGE-MRI does not have a universal fixed intensity scale. One possible per-volume normalisation is z-score normalisation over non-zero voxels.
```python
foreground = image != 0
normalised = np.zeros_like(image, dtype=np.float32)

if np.any(foreground):
    values = image[foreground]
    mean = float(values.mean())
    standard_deviation = max(float(values.std()), 1e-8)
    normalised[foreground] = (
        values - mean
    ) / standard_deviation
```
Alternative approaches may include robust percentile clipping, histogram standardisation, cohort-specific normalisation, or learned normalisation. The selected method should be fixed using development data only.
Resampling
When resampling:
use linear or higher-order interpolation for images, as appropriate;
use nearest-neighbour interpolation for masks;
verify that only labels `0, 1, 2, 3, 4` remain;
preserve or record the original affine and spacing;
state the target spacing in publications.
Longitudinal leakage
Do not place different timepoints from the same patient into different partitions. This applies to training, validation, test, calibration, and cross-validation folds.
Recommended experimental protocol
A recommended evaluation protocol is:
Use the supplied Utah training partition for model development.
Create validation folds only from the Utah training patients.
Keep the supplied Utah test patients completely held out.
Use Waikato for cross-cohort or external evaluation only when it has not influenced development.
Report Utah and Waikato results separately.
Report metrics for all four foreground structures.
Provide confidence intervals or patient-level uncertainty estimates.
Account for repeated scans from the same patient in statistical analysis.
Report excluded cases and the reasons for exclusion.
Include representative failure cases.
Recommended metrics include:
Dice similarity coefficient;
Intersection over Union;
sensitivity or recall;
precision;
95th-percentile Hausdorff distance;
average symmetric surface distance;
relative volume error;
calibration error, when probabilistic outputs are evaluated.
Do not rely only on pooled results. The Utah cohort is much larger than the Waikato cohort, so pooled averages can obscure cross-cohort degradation.
Intended and potential future uses
BiAtria-LGE 100 is intended for non-clinical research involving:
supervised multi-class bi-atrial segmentation;
atrial wall and cavity segmentation;
2D and 3D segmentation methods;
cross-cohort robustness evaluation;
external validation;
transfer learning;
domain adaptation and domain generalisation;
longitudinal cardiac imaging analysis;
uncertainty quantification;
model calibration;
automated segmentation quality control;
segmentation failure detection;
out-of-distribution detection;
few-shot and data-efficient learning;
active learning;
self-supervised representation learning;
test-time adaptation;
benchmarking of cardiac segmentation methods.
Potential quality-control research includes detecting:
missing anatomical classes;
anatomically implausible masks;
disconnected components;
excessive false-positive regions;
wall-cavity label reversal;
segmentation leakage;
empty masks;
unusual atrial volumes;
low-confidence predictions.
Known limitations
The Utah cohort is substantially larger than the Waikato cohort.
The Waikato cohort contains only nine image-mask pairs.
The Utah cohort contains repeated scans from some patients.
Follow-up timepoints are not uniform across patients.
Images include more than one in-plane matrix size.
Intensity scale and data type may vary across images or cohorts.
The dataset may not represent all scanners, institutions, protocols, populations, or disease presentations.
Statistical analyses must account for repeated observations.
Subgroup analysis may be limited by the metadata that can be shared.
Annotation variability may not be fully characterised.
The current mapping table describes the Utah cohort. Waikato patient-level metadata should be documented separately when available and permitted.
Performance on this dataset does not establish clinical validity.
Ethics and responsible use
The dataset must be treated as de-identified human research data.
Users must not:
attempt to identify participants;
reconstruct identifying information;
link dataset identifiers to external identifiable records;
redistribute the data outside the applicable licence or access agreement;
use the data for direct clinical decision-making without independent validation;
present a model as clinically validated solely because it performs well on this dataset.
Any downstream clinical use requires independent external validation, site-specific evaluation, appropriate human oversight, ethics approval, governance review, and regulatory assessment where applicable.
Researchers are encouraged to report:
failure modes;
uncertainty;
calibration;
cohort-specific performance;
subgroup performance when metadata permit;
clinically relevant limitations.
Citation
Researchers using this dataset must cite both:
the BiAtria-LGE 100 Figshare dataset record;
the associated publication listed under Related material.
Dataset citation
Replace the following placeholder with the citation generated by Figshare after publication:
```text
Gunawardhana, M., et al. (2026).
BiAtria-LGE 100: A Multi-Centre 3D LGE-MRI Dataset for Bi-Atrial
Wall and Cavity Segmentation in Atrial Fibrillation.
University of Auckland Institutional Figshare.
DOI: [FIGSHARE DOI]
```
BibTeX template
```bibtex
@dataset{gunawardhana_2026_biatria_lge100,
  author    = {Gunawardhana, Malitha and others},
  title     = {BiAtria-LGE 100: A Multi-Centre 3D LGE-MRI Dataset for
               Bi-Atrial Wall and Cavity Segmentation in Atrial Fibrillation},
  year      = {2026},
  publisher = {University of Auckland Institutional Figshare},
  doi       = {[FIGSHARE DOI]},
  url       = {[FIGSHARE URL]}
}
```
Related material
Associated publication:
> **TASSNet: A Deep Learning Framework for Robust Bi-Atrial Segmentation for Assessing Structural Basis of Atrial Fibrillation**
Add the complete author list, journal, year, volume, pages, and DOI before the repository is made public.
Suggested BibTeX placeholder:
```bibtex
@article{gunawardhana_tassnet,
  author  = {[AUTHORS]},
  title   = {TASSNet: A Deep Learning Framework for Robust Bi-Atrial
             Segmentation for Assessing Structural Basis of Atrial Fibrillation},
  journal = {[JOURNAL]},
  year    = {[YEAR]},
  volume  = {[VOLUME]},
  number  = {[ISSUE]},
  pages   = {[PAGES]},
  doi     = {[DOI]}
}
```
Licence and access
The Figshare record should state the final licence and access conditions.
Before open release, confirm:
permission to redistribute the Utah images;
permission to redistribute the Waikato images;
permission to redistribute the segmentation masks;
ethics and participant-consent conditions;
institutional data-governance requirements;
restrictions in source-data or collaboration agreements;
whether commercial reuse is permitted.
When open distribution is not permitted, use a metadata-only Figshare record or a controlled-access process.
Access statement template
```text
BiAtria-LGE 100 is available through the University of Auckland
Institutional Figshare repository at [FIGSHARE DOI]. Access is subject
to the licence, ethics, privacy, governance, and data-sharing conditions
described in the Figshare record.
```
Contact
Primary contact
Malitha Gunawardhana  
University of Auckland | Waipapa Taumata Rau  
Email: `[INSTITUTIONAL EMAIL]`
For access requests, ethics questions, or data-governance enquiries, include the authorised data custodian and institutional contact details.
Versioning
Recommended release format:
```text
Version 1.0
Release year: 2026
```
Future versions should document:
added or removed cases;
corrected metadata;
corrected image-label pairings;
annotation revisions;
split revisions;
changes to access conditions;
checksum changes.
A `CHANGELOG.md` file is recommended for all revisions.
