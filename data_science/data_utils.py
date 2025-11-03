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
    # Add more as needed
}


def get_data_folder():
    """Get the raw data folder path (works in local and Colab)"""
    try:
        import google.colab
        return Path('/content/Projects/data_science/datasets/raw')
    except ImportError:
        # Local - find project root
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            if (parent / 'setup.py').exists():
                return parent / 'data_science' / 'datasets' / 'raw'
        return Path.cwd() / 'data_science' / 'datasets' / 'raw'


def ensure_dataset(dataset_key, force_download=False):
    """
    Ensure dataset is available, download if needed.
    
    Args:
        dataset_key (str): Key from DATASETS registry
        force_download (bool): Re-download even if files exist
        
    Returns:
        Path: Path to the data folder
        
    Example:
        >>> data_folder = ensure_dataset("us_covid")
        >>> df = pd.read_csv(data_folder / "us_covid.csv")
    """
    if dataset_key not in DATASETS:
        raise ValueError(f"Unknown dataset '{dataset_key}'. Available: {list(DATASETS.keys())}")
    
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
