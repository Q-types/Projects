"""
Data acquisition utilities for my data science projects.

This module handles dataset downloads and ensures reproducibility
across local and Colab environments.
"""

import kagglehub
from pathlib import Path
import shutil


# Dataset registry - centralized source of truth
DATASETS = {
    # Complete time series dataset collection
    "tsdata": {
        "kaggle_id": "konradb/tsdata-1",
        "files": [
            "medium_posts.csv",
            "daily-minimum-temperatures-in-me.csv",
            "example_air_passengers.csv",
            "google_chg.csv",
            "outdoor-temperature-12UTC.csv",
            "exp1.csv",
            "exp2.csv",
            "quarterly_gdp_change.csv",
            "irish_electricity_daily.xlsx",
            "Sample - Superstore.xls",
            "ex1_wiki_visits.csv",
            "arma_series2.csv",
            "example_wp_log_R_outliers2.csv",
            "diabetic.csv",
            "ambient_temperature_system_failure.csv",
            "rossman_sales.csv",
            "energy_daily.csv",
            "example_retail_sales.csv",
            "avocado.csv",
            "example_wp_log_R_outliers1.csv",
            "iroots.png",
            "passengers.csv",
            "exp3.csv",
            "us_energy.csv",
            "passengers_test.csv",
            "irish_electricity.csv",
            "tesla_prices_5y.csv",
            "passengers_train.csv",
            "example_wp_log_peyton_manning.csv",
            "dataset_temperature.csv",
            "sunspots.csv",
            "arma_series3.csv",
            "Fremont_Bridge.csv",
            "us_covid.csv",
            "arma_series1.csv",
            "savings_change.csv",
            "wiki_log_R.csv",
            "irish_electricity_daily.csv",
        ]
    },
    
    # Convenience aliases for commonly used datasets
    "us_covid": {
        "kaggle_id": "konradb/tsdata-1",
        "files": ["us_covid.csv"]
    },
    "passengers": {
        "kaggle_id": "konradb/tsdata-1",
        "files": ["example_air_passengers.csv", "passengers.csv", "passengers_train.csv", "passengers_test.csv"]
    },
    "avocado": {
        "kaggle_id": "konradb/tsdata-1",
        "files": ["avocado.csv"]
    },
    "energy": {
        "kaggle_id": "konradb/tsdata-1",
        "files": ["energy_daily.csv", "us_energy.csv"]
    },
    "irish_electricity": {
        "kaggle_id": "konradb/tsdata-1",
        "files": ["irish_electricity.csv", "irish_electricity_daily.csv", "irish_electricity_daily.xlsx"]
    },
    
    # WHO health data
    "who_cases": {
        "kaggle_id": "niclowe/who-cases-dataset-and-wdi-country-population",
        "files": ["WHO_full_data2003.csv", "API_SP.POP.TOTL_DS2_en_excel_v2_887218.xls"]
    },
    
    # Hourly energy consumption (PJM interconnection)
    "pjm_energy": {
        "kaggle_id": "robikscube/hourly-energy-consumption",
        "files": [
            "est_hourly.paruqet",
            "PJMW_hourly.csv",
            "pjm_hourly_est.csv",
            "PJM_Load_hourly.csv",
            "DAYTON_hourly.csv",
            "NI_hourly.csv",
            "PJME_hourly.csv",
            "FE_hourly.csv",
            "DOM_hourly.csv",
            "EKPC_hourly.csv",
            "DEOK_hourly.csv",
            "DUQ_hourly.csv",
            "AEP_hourly.csv",
            "COMED_hourly.csv",
        ]
    },
    
    # Convenience alias for pjm_hourly_est.csv
    "pjm_hourly": {
        "kaggle_id": "robikscube/hourly-energy-consumption",
        "files": ["pjm_hourly_est.csv"]
    },
    # Add more as needed
}


def get_data_folder(check_drive=True):
    """
    Get the raw data folder path (works in local and Colab).
    
    In Colab, checks both Drive (for custom data) and cloned repo (for Kaggle downloads).
    
    Args:
        check_drive (bool): If True and in Colab, prefer Drive if mounted
    """
    try:
        import google.colab
        
        # Check if Drive is mounted and prefer it for custom data
        drive_path = Path('/content/drive/MyDrive/Projects/data_science/datasets/raw')
        if check_drive and drive_path.exists():
            return drive_path
        
        # Fall back to cloned repo location (for Kaggle downloads)
        return Path('/content/Projects/data_science/datasets/raw')
        
    except ImportError:
        # Local - find project root
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            if (parent / 'setup.py').exists():
                return parent / 'data_science' / 'datasets' / 'raw'
        return Path.cwd() / 'data_science' / 'datasets' / 'raw'


def ensure_dataset(dataset_key, kaggle_id=None, force_download=False):
    """
    Ensure dataset is available, download if needed.
    
    If dataset_key is not in registry and kaggle_id is provided,
    the dataset will be automatically downloaded and added to the registry.
    
    Args:
        dataset_key (str): Key from DATASETS registry (or new key name)
        kaggle_id (str, optional): Kaggle dataset ID (e.g., "username/dataset-name")
                                   Required if dataset_key not in registry
        force_download (bool): Re-download even if files exist
        
    Returns:
        Path: Path to the data folder
        
    Examples:
        >>> # Use existing dataset
        >>> data_folder = ensure_dataset("us_covid")
        >>> df = pd.read_csv(data_folder / "us_covid.csv")
        
        >>> # Auto-download new dataset
        >>> data_folder = ensure_dataset("my_new_data", kaggle_id="username/my-dataset")
        >>> # Dataset is now available and added to registry
    """
    # If dataset not in registry, try to auto-download and register it
    if dataset_key not in DATASETS:
        if kaggle_id is None:
            raise ValueError(
                f"Unknown dataset '{dataset_key}'. Available: {list(DATASETS.keys())}\n"
                f"To add a new dataset, provide kaggle_id parameter:\n"
                f"  ensure_dataset('{dataset_key}', kaggle_id='username/dataset-name')"
            )
        
        print(f"🆕 New dataset '{dataset_key}' - downloading and registering...")
        data_folder = get_data_folder()
        data_folder.mkdir(parents=True, exist_ok=True)
        
        # Download from Kaggle
        print(f"📥 Downloading from Kaggle: {kaggle_id}")
        cache_path = kagglehub.dataset_download(kaggle_id)
        
        # Discover and copy files
        files = []
        for file in Path(cache_path).glob("*"):
            if file.is_file():
                dest = data_folder / file.name
                shutil.copy2(file, dest)
                files.append(file.name)
                print(f"   Copied: {file.name}")
        
        # Register the dataset
        DATASETS[dataset_key] = {
            "kaggle_id": kaggle_id,
            "files": files
        }
        print(f"✅ Dataset '{dataset_key}' registered with {len(files)} files")
        print(f"✅ Dataset ready at: {data_folder}")
        return data_folder
    
    # Dataset exists in registry - proceed normally
    dataset_info = DATASETS[dataset_key]
    data_folder = get_data_folder()
    data_folder.mkdir(parents=True, exist_ok=True)
    
    # Check if files already exist
    files_exist = all((data_folder / f).exists() for f in dataset_info["files"])
    
    if files_exist and not force_download:
        print(f"✅ Dataset '{dataset_key}' already available")
        return data_folder
    
    # Download from Kaggle
    print(f"📥 Downloading dataset '{dataset_key}' from Kaggle...")
    cache_path = kagglehub.dataset_download(dataset_info["kaggle_id"])
    
    # Copy files to data folder
    for file in Path(cache_path).glob("*"):
        if file.is_file():
            dest = data_folder / file.name
            shutil.copy2(file, dest)
            print(f"   Copied: {file.name}")
    
    print(f"✅ Dataset ready at: {data_folder}")
    return data_folder


def get_custom_data_path(filename):
    """
    Get path to custom data file (works in local and Colab with Drive).
    
    Use this for custom CSV files you've uploaded to Drive.
    Automatically handles local vs Colab paths.
    
    Args:
        filename (str): Name of the file (e.g., "customer_feedback.csv")
        
    Returns:
        Path: Full path to the file
        
    Example:
        >>> path = get_custom_data_path("customer_feedback.csv")
        >>> df = pd.read_csv(path)
    """
    data_folder = get_data_folder(check_drive=True)
    file_path = data_folder / filename
    
    if not file_path.exists():
        print(f"⚠️  Warning: File not found: {file_path}")
        print(f"   Make sure file is in: {data_folder}")
        try:
            import google.colab
            print(f"   💡 Tip: Mount Drive and upload to MyDrive/Projects/data_science/datasets/raw/")
        except ImportError:
            pass
    
    return file_path


def list_datasets():
    """List all registered datasets"""
    print("Available datasets:")
    for key, info in DATASETS.items():
        print(f"  • {key}")
        print(f"    Kaggle: {info['kaggle_id']}")
        print(f"    Files: {', '.join(info['files'])}")
        print()


if __name__ == "__main__":
    # Test/example usage
    list_datasets()
