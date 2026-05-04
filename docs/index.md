# Jupycat

`cat` for Jupyter notebooks. Read cells, outputs, and images from the command line.

```
$ jupycat notebook.ipynb
  0 [mark] (a1b2c3d4)  # My Analysis
  1 [code] (e5f6g7h8)  import pandas as pd
  2 [code] (i9j0k1l2)  df = pd.read_csv("data.csv")
  3 [mark] (m3n4o5p6)  ## Results
  4 [code] (q7r8s9t0)  df.describe()
```

## Why?

Jupyter notebooks are JSON files. Reading them with `cat`, `grep`, or `head` gives you escaped newlines, base64 blobs, and metadata noise. `jupycat` gives you the actual code.

```
┌─────────────────────────────────────────────┐
│  cat notebook.ipynb                         │
│  → 500 lines of JSON you can't read         │
│                                             │
│  jupycat notebook.ipynb 3                   │
│  → the actual Python code in cell 3         │
└─────────────────────────────────────────────┘
```

## The AI agent problem

AI coding agents (Claude Code, Cursor, Codex) run in terminals — no Jupyter UI. When they encounter a `.ipynb` file, they have to deal with raw JSON:

```
┌─────────────────────────────────────────────────────────────┐
│  Problem 1: Token waste                                     │
│                                                             │
│  Agent reads notebook.ipynb → 50KB of JSON with base64      │
│  images, metadata, execution counts, output MIME types...   │
│  The actual code is maybe 2KB buried in there.              │
├─────────────────────────────────────────────────────────────┤
│  Problem 2: No cell awareness                               │
│                                                             │
│  Agent sees a flat JSON blob. It can't easily:              │
│  - jump to cell N                                           │
│  - search across cells                                      │
│  - see which cell produced which output                     │
├─────────────────────────────────────────────────────────────┤
│  Problem 3: Hacky workarounds                               │
│                                                             │
│  Agent runs python3 -c "import json; ..."                   │
│  → arbitrary code execution just to read a file             │
│  → different hack every time, wastes context                │
│  → no permission safety (unlike Bash(jupycat:*))            │
└─────────────────────────────────────────────────────────────┘
```

`jupycat` solves all three:

```
┌─────────────────────────────────────────────────────────────┐
│  jupycat notebook.ipynb          → cell overview in 3 lines │
│  jupycat notebook.ipynb 5 -o    → just cell 5 + its output │
│  jupycat notebook.ipynb -s "fit"→ find the training cell    │
│  jupycat notebook.ipynb 7 --img → extract plot for viewing  │
│  jupycat notebook.ipynb --fix-ids → enable NotebookEdit     │
│                                                             │
│  ✓ Minimal tokens   ✓ Cell-aware   ✓ Safe to auto-allow    │
└─────────────────────────────────────────────────────────────┘
```

## Install

```bash
pip install jupycat
```

**Zero dependencies.** Uses only Python standard library.

**Requires:** Python 3.8+

## Quick start

```bash
jupycat notebook.ipynb              # list all cells
jupycat notebook.ipynb 5            # show cell 5
jupycat notebook.ipynb 5 -o         # show cell 5 with outputs
jupycat notebook.ipynb -s "def foo" # search cell source for pattern
jupycat notebook.ipynb 7 --img      # extract images to default temp dir of OS
jupycat notebook.ipynb 7 --img .    # extract images to current directory
jupycat notebook.ipynb --fix-ids    # add missing cell IDs
```

## License

MIT
