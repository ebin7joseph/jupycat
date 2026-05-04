# jupycat

[![PyPI](https://img.shields.io/pypi/v/jupycat.svg)](https://pypi.org/project/jupycat/)
[![Python](https://img.shields.io/pypi/pyversions/jupycat.svg)](https://pypi.org/project/jupycat/)
[![Tests](https://github.com/ebin7joseph/jupycat/actions/workflows/test.yml/badge.svg)](https://github.com/ebin7joseph/jupycat/actions/workflows/test.yml)
[![Docs](https://github.com/ebin7joseph/jupycat/actions/workflows/docs.yml/badge.svg)](https://ebin7joseph.github.io/jupycat/)
[![License](https://img.shields.io/pypi/l/jupycat.svg)](https://github.com/ebin7joseph/jupycat/blob/main/LICENSE)

`cat` for Jupyter notebooks. Read cells, outputs, and images from the command line.

```
$ jupycat notebook.ipynb
  0 [mark] (a1b2c3d4)  # My Analysis
  1 [code] (e5f6g7h8)  import pandas as pd
  2 [code] (i9j0k1l2)  df = pd.read_csv("data.csv")
```

## Install

```bash
pip install jupycat
```

**Zero dependencies** · Python 3.8+

## Quick start

```bash
jupycat notebook.ipynb              # list all cells
jupycat notebook.ipynb 5            # show cell 5
jupycat notebook.ipynb 5 -o         # show cell 5 with outputs
jupycat notebook.ipynb -s "def foo" # search cell source for pattern
jupycat notebook.ipynb 7 --img      # extract images to temp dir
jupycat notebook.ipynb 7 --img .    # extract images to current directory
jupycat notebook.ipynb --fix-ids    # add missing cell IDs
```

## Docs

[Usage](docs/usage.md) · [AI Agents](docs/ai-agents.md) · [Contributing](docs/contributing.md)

## License

MIT
