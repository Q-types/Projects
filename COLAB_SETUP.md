# Google Colab Setup Guide

When opening my notebooks in Google Colab, I need to add this setup cell at the very top.

## Quick Setup Cell

Add this as the **first code cell** in your Colab notebook:

```python
# === COLAB SETUP ===
import sys
from pathlib import Path

# Check if running in Colab
try:
    import google.colab
    IN_COLAB = True
    
    # Clone my repo if not already present
    if not Path('Projects').exists():
        !git clone https://github.com/Q-types/Projects.git
    
    # Add my utils to Python path
    sys.path.insert(0, '/content/Projects')
    
    # Change to scripts directory
    import os
    os.chdir('/content/Projects/data_science/scripts')
    
    print("✅ Colab setup complete!")
    print(f"📁 Working directory: {Path.cwd()}")
    
except ImportError:
    IN_COLAB = False
    print("🏠 Running locally")
```

## Alternative: Use Colab-Compatible Versions

If you don't want to clone the repo, replace imports with:

```python
# Instead of:
# from utils.plot_styles import apply_style

# Use:
import sys
from pathlib import Path

# Check if in Colab
IN_COLAB = 'google.colab' in sys.modules

if IN_COLAB:
    # Clone repo for utils
    if not Path('Projects').exists():
        !git clone https://github.com/Q-types/Projects.git
    sys.path.insert(0, '/content/Projects')

# Now imports work
from utils.plot_styles import apply_style
```

## CFG Class Solution

For the CFG class, I've created a Colab-compatible version in `data_science/colab_setup.py`.

Use it like this:

```python
# At the top of notebook
import sys
from pathlib import Path

IN_COLAB = 'google.colab' in sys.modules

if IN_COLAB:
    sys.path.insert(0, '/content/Projects')
    from data_science.colab_setup import CFG, apply_style
else:
    # Local imports
    from utils.plot_styles import apply_style
    # Define CFG locally or import from notebook
```

## Full Example Notebook Start

```python
# Cell 1: Environment Setup
import sys
from pathlib import Path

IN_COLAB = 'google.colab' in sys.modules

if IN_COLAB:
    # Clone repo
    if not Path('Projects').exists():
        !git clone https://github.com/Q-types/Projects.git
    
    # Add to path
    sys.path.insert(0, '/content/Projects')
    
    # Use Colab-compatible versions
    from data_science.colab_setup import CFG, apply_style
else:
    # Local setup
    from utils.plot_styles import apply_style
    
    def find_project_root():
        current = Path.cwd()
        for p in [current] + list(current.parents):
            if (p / "setup.py").exists():
                return p
        return current
    
    class CFG:
        project_root = find_project_root()
        data_folder = project_root / "data_science" / "datasets" / "raw"
        img_dim1 = 15
        img_dim2 = 5

print(f"✅ Setup complete! Data folder: {CFG.data_folder}")

# Cell 2: Your actual code
apply_style('clean')
# ... rest of notebook
```

## Benefits

- ✅ Works in both local and Colab
- ✅ No manual path configuration
- ✅ Automatically clones latest code
- ✅ Same imports in both environments
