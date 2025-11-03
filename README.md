# Data Science Portfolio

This repository contains my data science coursework and projects.

## Structure

- **data_science/**: Main data science projects and experiments
  - `notebooks/`: Jupyter notebooks
  - `scripts/`: Python scripts
  - `datasets/`: Data files (not tracked in git)
  - `models/`: Trained models (not tracked in git)
  - `reports/`: Analysis reports
- **research/**: Research papers and experiments
- **utils/**: Utility functions and helper code

## Setup

### Local Development
```bash
# Install dependencies
conda env create -f environment.yml
conda activate [your-env-name]
```

### Google Colab Integration

**Option 1: Open from GitHub**
1. In Colab: `File → Open notebook → GitHub tab`
2. Enter your GitHub username or repo URL
3. Select the notebook you want to work on

**Option 2: Clone in Colab**
```python
from google.colab import drive
drive.mount('/content/drive')

# Clone repo
!git clone https://github.com/[your-username]/Portfolio.git
```

## Workflow

1. Work locally and commit changes
2. Push to GitHub: `git push origin main`
3. Open in Colab via GitHub integration
4. Save Colab changes back to GitHub: `File → Save a copy in GitHub`
