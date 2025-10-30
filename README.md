# EMCPy

[![CI][ci-badge]][ci-link] [![Docs][docs-badge]][docs-link]

**EMCPy** (Environmental Modeling Center Python utilities) provides tools for visualization, diagnostics, and analysis in support of NOAA’s Environmental Modeling Center (EMC) workflows. It offers a lightweight, extensible framework for building plots, handling data fields, and automating workflows used in EMC’s operational and research environments.

---

## Features

- **Plotting utilities**
  - High-level wrappers around Matplotlib and Cartopy
  - Support for discrete fields, colorbars, and meteorological conventions
  - Ready-to-use plot layers: scatter, gridded fields, contour, violin, box-and-whisker, error bars, and more

- **Consistent interfaces**
  - Unified API for building figures and subplots
  - Clear separation of plot layers, figure creation, and feature controls

- **Documentation and examples**
  - [Gallery of plot types](https://noaa-emc.github.io/emcpy/plot_types/index.html)
  - Explanations of design choices, discrete fields, and troubleshooting

[ci-badge]: https://github.com/NOAA-EMC/emcpy/actions/workflows/ci.yml/badge.svg
[ci-link]:  https://github.com/NOAA-EMC/emcpy/actions/workflows/ci.yml
[docs-badge]: https://img.shields.io/badge/docs-latest-blue.svg
[docs-link]:  https://noaa-emc.github.io/emcpy/
---

## Installation

```bash
pip install emcpy
```

For the latest development version:

```bash
git clone https://github.com/NOAA-EMC/emcpy.git
cd emcpy
pip install -e .[dev,test,docs]
```

---

## Documentation

Full documentation is available here:  
👉 [https://noaa-emc.github.io/emcpy/](https://noaa-emc.github.io/emcpy/)

---

## Contributing

Contributions are welcome! Please open issues or pull requests on [GitHub](https://github.com/NOAA-EMC/emcpy).

---

## License

This project is licensed under the **LGPL v2.1 or later**. See the [LICENSE](LICENSE) file for details.
