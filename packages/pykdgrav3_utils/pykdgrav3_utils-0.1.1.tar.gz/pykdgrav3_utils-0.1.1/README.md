# pykdgrav3_utils

This package contains modules to handle IO of PKDGRAV3.
They can be used to read/write snapshots, FoF data or unit conversions.

However, this package is not intended to provide any plotting routine.

## Install

### From pip

```bash
python3 -m pip pykdgrav3_utils
```

### From source

```bash
git clone git@bitbucket.org:iacsimgro/pykdgrav3_utils.git
cd pykdgrav3_utils
python3 -m pip install .
```

## Development (using poetry)

```bash
make poetry-download
make install
make pre-commit-install
make codestyle
make publish
```
