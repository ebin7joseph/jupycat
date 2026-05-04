# Usage

## List all cells

```bash
$ jupycat notebook.ipynb
  0 [mark] (a1b2c3d4)  # Data Exploration
  1 [code] (e5f6g7h8)  import pandas as pd
  2 [code] (i9j0k1l2)  df = pd.read_csv("sales.csv")
  3 [mark] (m3n4o5p6)  ## Cleaning
  4 [code] (q7r8s9t0)  df.dropna(inplace=True)
  5 [code] (u1v2w3x4)  df.describe()
```

Each line shows: `index [type] (cell_id)  first line of source`

## Show a specific cell

```bash
$ jupycat notebook.ipynb 2
── cell 2 (i9j0k1l2) ──
df = pd.read_csv("sales.csv")
print(f"Rows: {len(df):,}")
df.head()
```

## Show cell with outputs

```bash
$ jupycat notebook.ipynb 2 -o
── cell 2 (i9j0k1l2) ──
df = pd.read_csv("sales.csv")
print(f"Rows: {len(df):,}")
df.head()

--- output ---
Rows: 14,832
   date        product   revenue
0  2024-01-01  Widget A  1234.56
1  2024-01-02  Widget B  789.01
```

The `-o` flag appends execution outputs (stdout, return values, errors) below the source.

## Search for a pattern

```bash
$ jupycat notebook.ipynb -s "def train"
── cell 7 (z5y4x3w2) ──
def train_model(X, y):
    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X, y)
    return clf
```

Searches all cell source code and prints matching cells with their index and cell ID.

Combine with `-o` to include outputs:

```bash
$ jupycat notebook.ipynb -s "accuracy" -o
```

## Extract images

```bash
$ jupycat notebook.ipynb 5 --img
/tmp/jupycat_cell5_0.png
```

Extracts PNG images from cell outputs to files. Prints the path to each extracted image.

Specify a directory:

```bash
$ jupycat notebook.ipynb 5 --img ./plots
./plots/jupycat_cell5_0.png
```

If no directory is given, images are saved to the OS temp directory.

## Fix missing cell IDs

```bash
$ jupycat notebook.ipynb --fix-ids
Fixed 3 cell(s) in notebook.ipynb
```

Adds IDs to cells that don't have them. Preserves existing IDs. Useful for AI agents (e.g. Claude Code in VSCode) that use `NotebookEdit` to modify notebooks — `NotebookEdit` requires cell IDs to target specific cells.

Cell IDs may be missing in notebooks created by older VSCode Jupyter extensions (nbformat 4.4), classic Jupyter Notebook (pre-7), or AI agents that generate notebook JSON without IDs. Running `--fix-ids` makes them compatible with modern tooling.

Safe to run multiple times — only writes when there are cells without IDs.

## Command reference

```
jupycat FILE                   list all cells
jupycat FILE CELL              show cell source
jupycat FILE CELL -o           show cell source + outputs
jupycat FILE -s PATTERN        search cells by content
jupycat FILE -s PATTERN -o     search with outputs
jupycat FILE CELL --img        extract images to temp dir
jupycat FILE CELL --img DIR    extract images to DIR
jupycat FILE --fix-ids         add missing cell IDs
jupycat -h                     show help
```

| Flag             | Description                           |
| ---------------- | ------------------------------------- |
| `CELL`           | Cell index (0-based)                  |
| `-s`, `--search` | Search pattern (substring match)      |
| `-o`, `--output` | Include cell execution outputs        |
| `--img [DIR]`    | Extract PNG images from cell outputs  |
| `--fix-ids`      | Add IDs to cells that don't have them |
