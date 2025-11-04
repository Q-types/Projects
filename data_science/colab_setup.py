"""
Colab Setup - Run this at the top of notebooks when using Google Colab

Add this cell to your Colab notebooks:

```python
# === COLAB SETUP ===
import sys
from pathlib import Path

# Check if running in Colab
try:
    import google.colab
    IN_COLAB = True
    
    # Clone the repo if not already present
    if not Path('Projects').exists():
        !git clone https://github.com/Q-types/Projects.git
    
    # Add utils to path
    sys.path.insert(0, '/content/Projects')
    
    # Change to notebooks directory
    %cd /content/Projects/data_science/scripts
    
except ImportError:
    IN_COLAB = False
    # Running locally, no setup needed
```
"""

# Colab-compatible versions of local utilities

def apply_style(preset="clean"):
    """
    Apply matplotlib style presets (Colab-compatible version)
    
    Args:
        preset (str): 'clean' or 'presentation'
    """
    import matplotlib.pyplot as plt
    
    STYLE_PRESETS = {
        "clean": {
            "figure.figsize": (10, 5),
            "lines.linewidth": 1.2,
            "axes.grid": True,
            "grid.alpha": 0.3,
            "axes.facecolor": "white",
            "axes.edgecolor": "gray",
            "axes.labelsize": 12,
            "axes.titlesize": 14,
            "font.size": 11,
            "legend.frameon": False,
            "legend.fontsize": 10,
            "lines.markersize": 4,
        },
        "presentation": {
            "figure.figsize": (12, 6),
            "lines.linewidth": 2.0,
            "axes.grid": True,
            "grid.alpha": 0.2,
            "axes.facecolor": "white",
            "axes.edgecolor": "gray",
            "axes.labelsize": 14,
            "axes.titlesize": 16,
            "font.size": 13,
            "legend.frameon": False,
            "legend.fontsize": 12,
            "lines.markersize": 6,
        },
    }
    
    if preset not in STYLE_PRESETS:
        raise ValueError(f"Unknown preset '{preset}'. Available: {list(STYLE_PRESETS.keys())}")
    
    plt.rcParams.update(STYLE_PRESETS[preset])


def get_project_root():
    """
    Get project root - works in both local and Colab environments
    """
    from pathlib import Path
    import sys
    
    # Check if in Colab
    try:
        import google.colab
        return Path('/content/Projects')
    except ImportError:
        # Local environment - find project root
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            if (parent / 'setup.py').exists() or (parent / '.git').exists():
                return parent
        return current


class CFG:
    """
    Configuration class that works in both local and Colab environments
    """
    project_root = get_project_root()
    data_folder = project_root / "data_science" / "datasets" / "raw"
    img_dim1 = 15
    img_dim2 = 5
    imgr_dim1 = 6
    imgr_dim2 = 4
    imgr2_dim1 = 7.5
    imgr2_dim2 = 5
    imgj_dim1 = 3.5
    imgj_dim2 = 2.5
    imgj2_dim1 = 7.2
    imgj2_dim2 = 3.5
    imgp_dim1 = 10
    imgp_dim2 = 5.625