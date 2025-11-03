#!/usr/bin/env python3
"""
Download Kaggle datasets to the raw data folder
"""
import kagglehub
import shutil
from pathlib import Path

# Dataset to download
DATASET_NAME = "niclowe/who-cases-dataset-and-wdi-country-population"

# Target directory
RAW_DATA_DIR = Path(__file__).parent.parent / "datasets" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

print(f"Downloading dataset: {DATASET_NAME}")
print(f"Target directory: {RAW_DATA_DIR.absolute()}")

# Download dataset (kagglehub caches it)
path = kagglehub.dataset_download(DATASET_NAME)
print(f"\nDataset downloaded to cache: {path}")

# Copy files to raw folder
source_path = Path(path)
if source_path.is_dir():
    for file in source_path.iterdir():
        if file.is_file():
            dest_file = RAW_DATA_DIR / file.name
            print(f"Copying: {file.name} -> {dest_file}")
            shutil.copy2(file, dest_file)
else:
    # Single file
    dest_file = RAW_DATA_DIR / source_path.name
    print(f"Copying: {source_path.name} -> {dest_file}")
    shutil.copy2(source_path, dest_file)

print(f"\n✅ Dataset files copied to: {RAW_DATA_DIR.absolute()}")
print("\nFiles in raw folder:")
for file in sorted(RAW_DATA_DIR.glob("*")):
    if file.is_file():
        size_mb = file.stat().st_size / (1024 * 1024)
        print(f"  - {file.name} ({size_mb:.2f} MB)")
