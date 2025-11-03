# Shared Utilities

Reusable utilities for data science projects across the workspace.

## Plot Styles

### Quick Start

```python
# In any notebook or script
from utils import apply_clean_style

apply_clean_style()
```

### Available Styles

#### Clean Style (Default)
Professional, minimalist style with white background and softened grid lines.

```python
from utils import apply_clean_style
apply_clean_style()
```

#### Using Named Presets
```python
from utils.plot_styles import apply_style

# Clean style (default)
apply_style('clean')

# Presentation style (larger fonts, thicker lines)
apply_style('presentation')
```

### Adding Custom Presets

Edit `/Users/q/Projects/utils/plot_styles.py` and add new entries to the `STYLE_PRESETS` dictionary.

## Directory Structure

```
utils/
├── __init__.py          # Package initialization
├── plot_styles.py       # Matplotlib styling utilities
└── README.md           # This file
```
