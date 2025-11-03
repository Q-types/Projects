# Notebook Template - Best Practices

Use this template for all my course notebooks to ensure reproducibility.

## Cell 1: Environment Setup

```python
# === ENVIRONMENT SETUP ===
import sys
from pathlib import Path

# Detect environment
IN_COLAB = 'google.colab' in sys.modules

if IN_COLAB:
    # Clone repo if needed
    if not Path('Projects').exists():
        !git clone https://github.com/Q-types/Projects.git
    
    # Add to path
    sys.path.insert(0, '/content/Projects')
    
    print("🌐 Running in Google Colab")
else:
    print("🏠 Running locally")

# Import my utilities (works in both environments)
from data_science.colab_setup import CFG, apply_style
from data_science.data_utils import ensure_dataset

print(f"✅ Setup complete!")
```

## Cell 2: Data Acquisition

```python
# === DATA ACQUISITION ===
# Ensure dataset is available (downloads if needed)
data_folder = ensure_dataset("us_covid")

# Now load the data
import pandas as pd
df = pd.read_csv(data_folder / "us_covid.csv")

print(f"✅ Loaded {len(df)} rows")
```

## Cell 3: Imports & Configuration

```python
# === IMPORTS ===
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet

# Apply my plotting style
apply_style('clean')

# Suppress warnings
import warnings
warnings.simplefilter('ignore', FutureWarning)
```

## Cell 4+: Analysis

```python
# Now do my actual work...
```

---

## Why This Pattern?

✅ **Reproducible**: Anyone can run my notebooks  
✅ **Portable**: Works in Colab and locally  
✅ **Self-documenting**: Clear where data comes from  
✅ **Professional**: Same pattern used in industry  
✅ **Efficient**: Only downloads data once  
✅ **Maintainable**: Centralized dataset registry  

## Adding New Datasets

Edit `data_science/data_utils.py` and add to DATASETS:

```python
DATASETS = {
    "my_new_dataset": {
        "kaggle_id": "username/dataset-name",
        "files": ["file1.csv", "file2.csv"]
    },
}
```

Then use: `ensure_dataset("my_new_dataset")`
