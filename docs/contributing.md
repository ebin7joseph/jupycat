# Contributing

## Setup

```bash
git clone https://github.com/ebinjoseph/jupycat
cd jupycat
pip install -e .
```

## Tests

```bash
pytest tests/ -v
```

All changes should include tests. The test suite uses only pytest with no additional fixtures or plugins.

## Project structure

```
jupycat/
├── src/jupycat/
│   ├── __init__.py      # version
│   └── cli.py           # all CLI logic
├── tests/
│   └── test_cli.py      # tests
├── docs/                # mkdocs site
├── mkdocs.yml
├── pyproject.toml
└── LICENSE
```

## Guidelines

- Zero dependencies — stdlib only
- Keep it simple — one file for all CLI logic
- Every feature needs a test
