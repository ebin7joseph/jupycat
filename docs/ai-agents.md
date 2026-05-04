# Use with AI agents

`jupycat` was built so AI agents can read notebooks without `python3 -c "import json..."` hacks.

## Claude Code

Add to `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": ["Bash(jupycat:*)"]
  }
}
```

The agent can now read any notebook without permission prompts:

```
Agent: Let me check the model training cell.
       → jupycat notebook.ipynb -s "model.fit"

Agent: What were the results?
       → jupycat notebook.ipynb 12 -o

Agent: Let me see that plot.
       → jupycat notebook.ipynb 7 --img
       → Read /tmp/jupycat_cell7_0.png
```

## Why not just use `Read`?

Most AI tools have a file read command, but notebooks are JSON:

| Tool                            | Result                                         |
| ------------------------------- | ---------------------------------------------- |
| `cat notebook.ipynb`            | Raw JSON with escaped `\n`, base64 image blobs |
| `Read notebook.ipynb`           | Same JSON, often exceeds token limits          |
| `grep "pattern" notebook.ipynb` | Matches JSON lines, not cell boundaries        |
| **`jupycat notebook.ipynb 5`** | Clean Python source code                        |

## Security

`jupycat` is read-only by default. The only write operation is `--fix-ids`, which adds cell metadata without touching source code or outputs. No network access, no code execution, no dependencies.

This makes `Bash(jupycat:*)` a safe permission to grant — unlike `Bash(python3 -c:*)` which allows arbitrary code execution.
