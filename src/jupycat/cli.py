#!/usr/bin/env python3
"""Read Jupyter notebook cells from the command line.

Usage:
  jupycat FILE                       list cells (index + type + cell ID + first line)
  jupycat FILE CELL                  print cell source (with cell ID header)
  jupycat FILE CELL -o               print cell source + outputs
  jupycat FILE -s PATTERN            print cells matching pattern (with cell IDs)
  jupycat FILE -s PATTERN -o         matching cells with outputs
  jupycat FILE --fix-ids             add IDs to cells that have none
  jupycat FILE CELL --img             extract images to OS temp dir
  jupycat FILE CELL --img PATH        extract images to PATH
"""
import argparse
import base64
import json
import os
import sys
import tempfile
import uuid


def load_notebook(path):
    with open(path) as f:
        return json.load(f)


def fmt_outputs(cell):
    parts = []
    for out in cell.get("outputs", []):
        otype = out.get("output_type", "")
        if otype == "stream":
            parts.append("".join(out.get("text", [])))
        elif otype in ("execute_result", "display_data"):
            data = out.get("data", {})
            if "text/plain" in data:
                parts.append("".join(data["text/plain"]))
            elif "image/png" in data:
                parts.append("[image]")
        elif otype == "error":
            parts.append("".join(out.get("traceback", [])))
    return "\n".join(parts)


def print_cell(cell, show_output=False):
    print("".join(cell["source"]))
    if show_output and cell.get("outputs"):
        text = fmt_outputs(cell)
        if text.strip():
            print(f"\n--- output ---\n{text}")


def cmd_list(cells):
    for i, c in enumerate(cells):
        first = "".join(c["source"]).split("\n")[0][:80]
        cid = c.get("id", "")
        print(f"{i:3d} [{c['cell_type'][:4]}] ({cid})  {first}")


def cmd_show(cells, index, show_output=False):
    if index < 0 or index >= len(cells):
        print(f"Error: cell {index} out of range (0-{len(cells) - 1})", file=sys.stderr)
        sys.exit(1)
    cell = cells[index]
    cid = cell.get("id", "")
    print(f"── cell {index} ({cid}) ──")
    print_cell(cell, show_output)


def cmd_search(cells, pattern, show_output=False):
    found = False
    for i, c in enumerate(cells):
        src = "".join(c["source"])
        if pattern in src:
            cid = c.get("id", "")
            print(f"── cell {i} ({cid}) ──")
            print_cell(c, show_output)
            found = True
    if not found:
        print(f"No cells matching '{pattern}'", file=sys.stderr)


def cmd_img(cells, index, img_dir):
    if index < 0 or index >= len(cells):
        print(f"Error: cell {index} out of range (0-{len(cells) - 1})", file=sys.stderr)
        sys.exit(1)

    if img_dir is None:
        img_dir = tempfile.gettempdir()
    os.makedirs(img_dir, exist_ok=True)

    count = 0
    for out in cells[index].get("outputs", []):
        data = out.get("data", {})
        if "image/png" in data:
            path = os.path.join(img_dir, f"jupycat_cell{index}_{count}.png")
            with open(path, "wb") as f:
                f.write(base64.b64decode(data["image/png"]))
            print(path)
            count += 1

    if not count:
        print(f"No images in cell {index}", file=sys.stderr)


def cmd_fix_ids(path):
    with open(path) as f:
        nb = json.load(f)

    fixed = 0
    for cell in nb["cells"]:
        if not cell.get("id"):
            cell["id"] = uuid.uuid4().hex[:8]
            fixed += 1

    if fixed:
        with open(path, "w") as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
            f.write("\n")
        print(f"Fixed {fixed} cell(s) in {path}")
    else:
        print(f"All cells already have IDs in {path}")


def main():
    parser = argparse.ArgumentParser(
        prog="jupycat",
        description="cat for Jupyter notebooks.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  jupycat notebook.ipynb              list all cells
  jupycat notebook.ipynb 5            show cell 5
  jupycat notebook.ipynb 5 -o         show cell 5 with outputs
  jupycat notebook.ipynb -s "def foo" find cells containing "def foo"
  jupycat notebook.ipynb --fix-ids    add missing cell IDs
  jupycat notebook.ipynb 7 --img      extract images to OS temp dir
  jupycat notebook.ipynb 7 --img .    extract images to current dir
""",
    )
    parser.add_argument("notebook", help="path to .ipynb file")
    parser.add_argument("cell", nargs="?", type=int, help="cell index to display")
    parser.add_argument("-s", "--search", help="search pattern in cell source")
    parser.add_argument("-o", "--output", action="store_true", help="include cell outputs")
    parser.add_argument("--img", nargs="?", const=None, default=False,
                        help="extract images to PATH (default: OS temp dir)")
    parser.add_argument("--fix-ids", action="store_true", help="add IDs to cells missing them")
    args = parser.parse_args()

    if args.fix_ids:
        cmd_fix_ids(args.notebook)
        return

    cells = load_notebook(args.notebook)["cells"]

    if args.img is not False and args.cell is not None:
        cmd_img(cells, args.cell, args.img)
        return

    if args.search:
        cmd_search(cells, args.search, args.output)
    elif args.cell is not None:
        cmd_show(cells, args.cell, args.output)
    else:
        cmd_list(cells)


if __name__ == "__main__":
    main()
