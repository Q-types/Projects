# Communik8 NLP Project

NLP analysis and classification project.

## Directory Structure

```
communik8_nlp/
├── data/           # Raw and processed datasets
├── notebooks/      # Jupyter notebooks (work here!)
├── reports/        # Generated reports and visualizations
├── src/            # Source code and modules
├── artifacts/      # Saved models, thresholds, figures
└── config/         # Configuration files (taxonomy JSON, stopword lists)
```

## Colab Setup

Use this setup cell at the top of your notebooks:

```python
# === COLAB SETUP ===
import sys
from pathlib import Path

try:
    import google.colab
    IN_COLAB = True
    
    # Clone repo if not present
    if not Path('Projects').exists():
        !git clone https://github.com/Q-types/Projects.git
    else:
        !cd Projects && git pull origin main
    
    # Navigate to this project's notebooks folder
    %cd /content/Projects/data_science/mini_projects/communik8_nlp/notebooks
    
    # Add project src to path
    project_root = Path('/content/Projects/data_science/mini_projects/communik8_nlp')
    sys.path.insert(0, str(project_root / 'src'))
    
    # Add main data_science utils to path
    sys.path.insert(0, '/content/Projects')
    
    print("✅ Colab setup complete!")
    print(f"📁 Working directory: {Path.cwd()}")
    
except ImportError:
    IN_COLAB = False
    # Local - navigate to notebooks folder
    project_root = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()
    sys.path.insert(0, str(project_root / 'src'))
```

## Usage in Notebooks

After running the setup cell, you can use relative paths:

```python
import pandas as pd

# Save to artifacts (relative path works!)
df.to_csv("../artifacts/feedback_cleaned.csv", index=False)

# Load from data
df = pd.read_csv("../data/raw_data.csv")

# Load config
import json
with open("../config/taxonomy.json") as f:
    taxonomy = json.load(f)
```

Or use absolute paths:

```python
from pathlib import Path

project_root = Path.cwd().parent  # One level up from notebooks/

# Save to artifacts
artifacts_path = project_root / "artifacts" / "feedback_cleaned.csv"
df.to_csv(artifacts_path, index=False)

# Load from data
data_path = project_root / "data" / "raw_data.csv"
df = pd.read_csv(data_path)
```

## Workflow

1. **Data**: Put raw datasets in `data/`
2. **Notebooks**: Do your analysis in `notebooks/` (you're here!)
3. **Code**: Put reusable code in `src/` as `.py` modules
4. **Artifacts**: Save trained models, figures, etc. to `artifacts/`
5. **Config**: Store configuration files in `config/`
6. **Reports**: Generate final reports in `reports/`
