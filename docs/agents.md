# Example Agent Configs

Drop these into your agent's instructions file to teach it how to use jupycat.

## Claude Code (`CLAUDE.md`)

Add to your project's `CLAUDE.md` or `~/.claude/CLAUDE.md` for global.

### Minimal

```markdown
- use `jupycat` to read Jupyter notebooks instead of `python3 -c` or `Read`:
  - `jupycat notebook.ipynb` — list cells: `index [type] (cell_id)  first line`
  - `jupycat notebook.ipynb N` — show cell N source
  - `jupycat notebook.ipynb N -o` — show cell N source + outputs
  - `jupycat notebook.ipynb -s "pattern"` — search cell source for pattern
  - `jupycat notebook.ipynb N --img` — extract images to temp dir
  - `jupycat notebook.ipynb --fix-ids` — add missing cell IDs (required by NotebookEdit in VSCode agents)
```

### Full

```markdown
# Jupyter Notebooks

- always read cell outputs when reading jupyter notebooks
- use `jupycat` to read Jupyter notebooks instead of `python3 -c` or `Read`:
  - `jupycat notebook.ipynb` — list cells: `index [type] (cell_id)  first line`
  - `jupycat notebook.ipynb N` — show cell N source
  - `jupycat notebook.ipynb N -o` — show cell N source + outputs
  - `jupycat notebook.ipynb -s "pattern"` — search cell source for pattern
  - `jupycat notebook.ipynb N --img` — extract images to temp dir
  - `jupycat notebook.ipynb --fix-ids` — add missing cell IDs (required by NotebookEdit in VSCode agents)

## Workflow

1. Run `jupycat notebook.ipynb` to see all cells at a glance
2. Use cell index or search to find the cell you need
3. Use `-o` to see outputs — don't skip this for data analysis notebooks
4. Use `--img` to extract plots, then `Read` the image file to view it
5. Before using `NotebookEdit` (VSCode AI agents), run `--fix-ids` if cells lack IDs
6. Use the cell ID from jupycat output when calling `NotebookEdit`
```

### Permissions

Add to `.claude/settings.local.json` to auto-allow:

```json
{
  "permissions": {
    "allow": ["Bash(jupycat:*)"]
  }
}
```

## Cursor (`.cursorrules`)

```markdown
# Jupyter Notebooks

When working with Jupyter notebooks (.ipynb files), use the `jupycat` CLI tool:

- `jupycat notebook.ipynb` — list all cells with index, type, cell ID, and first line
- `jupycat notebook.ipynb N` — show source of cell N
- `jupycat notebook.ipynb N -o` — show source + outputs of cell N
- `jupycat notebook.ipynb -s "pattern"` — search cell source for a pattern
- `jupycat notebook.ipynb N --img` — extract images from cell N to temp dir
- `jupycat notebook.ipynb --fix-ids` — add missing cell IDs

Do NOT read .ipynb files directly — they are JSON and waste tokens.
Always check outputs with `-o` when analyzing data notebooks.
```

## Codex (`AGENTS.md` / `codex.md`)

```markdown
# Jupyter Notebooks

Use `jupycat` to read .ipynb files. Do not parse notebook JSON directly.

Commands:
  jupycat FILE              list cells: index [type] (cell_id) first_line
  jupycat FILE N            show cell N
  jupycat FILE N -o         show cell N with outputs
  jupycat FILE -s PATTERN   search cell source
  jupycat FILE N --img      extract images to /tmp
  jupycat FILE --fix-ids    add missing cell IDs

Always use -o when inspecting data analysis or model training cells.
```
