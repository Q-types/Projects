# Mini Projects

This directory contains smaller, focused data science projects with a standardized structure.

## Directory Structure

```
mini_projects/
├── data/           # Raw and processed datasets
├── notebooks/      # Jupyter notebooks for exploration and analysis
├── reports/        # Generated reports, visualizations, presentations
├── src/            # Source code, utilities, modules
├── artifacts/      # Saved models, thresholds, figures, trained objects
└── config/         # Configuration files (taxonomy JSON, stopword lists, etc.)
```

## Usage

Each project should follow this structure for consistency and reproducibility.

### Example Workflow

```python
# In notebooks/
from pathlib import Path
import sys

# Add src to path
project_root = Path.cwd().parent
sys.path.insert(0, str(project_root / 'src'))

# Import your modules
from my_module import MyClass

# Load data
data_path = project_root / 'data' / 'dataset.csv'
df = pd.read_csv(data_path)

# Save artifacts
model_path = project_root / 'artifacts' / 'model.pkl'
joblib.dump(model, model_path)

# Save reports
report_path = project_root / 'reports' / 'analysis.html'
fig.savefig(report_path)
```

## Projects

List your projects here as you add them:

- `communik8_nlp/` - NLP analysis project
- (Add more as you create them)

## Notes

- Use `.gitkeep` files to track empty directories
- Large data files should be gitignored (add to .gitignore if needed)
- Artifacts (models, etc.) should be gitignored if large
- Config files and reports should be committed to git
