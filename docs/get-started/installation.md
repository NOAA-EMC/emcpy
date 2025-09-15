# Installation
EMCPy is designed to run on both local machines and HPC systems.
We recommend setting it up inside a **clean virtual environment** to avoid conflicts with other Python
packages.

## 1. Create and activate a virtual environment
```bash
python -m venv .venv
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

```{note}
If you prefer Conda, you can use `conda create -n emcpy python=3.10` instead.
```

## 2. Upgrade pip
```bash
python -m pip install --upgrade pip
```

## 3. Install EMCPy
If you are developing from source (recommended for contributors):
```bash
pip install -e .
```

This performs an editable install, meaning changes you make to the source code are immediately
available in your environment.
If EMCPy is available on PyPI, you can install the latest release directly:
```bash
pip install emcpy
```

## 4. Optional extras
Some features require additional packages:
- **Cartopy** for map projections
```bash
pip install cartopy
```
- **Jupyter** for interactive notebooks
```bash
pip install jupyterlab
```

```{tip}
On some systems (especially HPC), Cartopy may require GEOS/PROJ libraries.
If you see build errors, consult [Cartopy’s installation
guide](https://scitools.org.uk/cartopy/docs/latest/installing.html).
```
---
Once installed, head to the [Quickstart](quickstart.md) to make your first EMCPy plot