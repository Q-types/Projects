"""
Reusable matplotlib plotting styles and configurations.
"""

import matplotlib.pyplot as plt


def apply_clean_style():
    """
    Apply clean visual plotting preferences to matplotlib.
    
    This style provides a minimalist, professional look with:
    - White background for clarity
    - Softened grid lines
    - Consistent sizing
    - Clean legends without frames
    
    Usage:
        from utils import apply_clean_style
        apply_clean_style()
    """
    plt.rcParams.update({
        "figure.figsize": (10, 5),           # Consistent figure size
        "lines.linewidth": 1.2,              # Thinner lines (default is ~1.5–2 in fivethirtyeight)
        "axes.grid": True,                   # Keep the grid for readability
        "grid.alpha": 0.3,                   # Soften the grid lines
        "axes.facecolor": "white",           # White background for clarity
        "axes.edgecolor": "gray",            # Softer border
        "axes.labelsize": 12,
        "axes.titlesize": 14,
        "font.size": 11,
        "legend.frameon": False,             # Cleaner legends
        "legend.fontsize": 10,
        "lines.markersize": 4,
    })


# Optional: Define additional style presets
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


def apply_style(preset="clean"):
    """
    Apply a named style preset to matplotlib.
    
    Args:
        preset (str): Name of the preset ('clean', 'presentation')
    
    Usage:
        from utils.plot_styles import apply_style
        apply_style('presentation')
    """
    if preset not in STYLE_PRESETS:
        raise ValueError(f"Unknown preset '{preset}'. Available: {list(STYLE_PRESETS.keys())}")
    
    plt.rcParams.update(STYLE_PRESETS[preset])
