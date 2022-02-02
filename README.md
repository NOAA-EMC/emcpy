# EMCPy
EMCPy is a Python toolkit that supplies useful tools and utilities to help developers at EMC accomplish their Python needs without having to be an expert in Python. It is designed so that novice users can develop plots or calculate statistics with only a few lines of code while giving experienced Python users the ability to be power users. EMCPy utilizes modern program practices  and its centralized functions include plotting routines, statistical calculations, look up tables and helpful I/O procedures.

### Clone Repository
```sh
$> git clone https://github.com/noaa-emc/emcpy
```

### Load environments on Hera
```sh
$> cd empcy
$> source modulefiles/EMCPy.hera.modulefile
```

### Load environments on Orion
```sh
$> cd empcy
$> source modulefiles/EMCPy.orion.modulefile
```

### Documentation
Documentation is automatically generated when `develop` is updated and available [here](https://noaa-emc.github.io/emcpy/emcpy.html).

To manually generate documentation upon installation (requires [`pdoc`](https://pdoc.dev/)):
```sh
$> pdoc --docformat "google" emcpy
```
