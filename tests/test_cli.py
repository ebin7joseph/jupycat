import base64
import json
import os
import tempfile

import pytest

from jupycat.cli import (
    cmd_fix_ids,
    cmd_img,
    cmd_list,
    cmd_search,
    cmd_show,
    fmt_outputs,
    load_notebook,
)

# ── Fixtures ──

SAMPLE_NB = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {},
    "cells": [
        {
            "cell_type": "markdown",
            "id": "md-0",
            "metadata": {},
            "source": ["# Title\n", "Some description"],
        },
        {
            "cell_type": "code",
            "id": "code-1",
            "metadata": {},
            "source": ["import numpy as np\n", "print('hello')"],
            "outputs": [
                {"output_type": "stream", "name": "stdout", "text": ["hello\n"]}
            ],
        },
        {
            "cell_type": "code",
            "id": "code-2",
            "metadata": {},
            "source": ["x = 42"],
            "outputs": [
                {
                    "output_type": "execute_result",
                    "data": {"text/plain": ["42"]},
                    "metadata": {},
                }
            ],
        },
        {
            "cell_type": "code",
            "metadata": {},
            "source": ["# no id cell"],
            "outputs": [],
        },
        {
            "cell_type": "code",
            "id": "img-cell",
            "metadata": {},
            "source": ["plt.plot([1,2,3])"],
            "outputs": [
                {
                    "output_type": "display_data",
                    "data": {
                        "image/png": base64.b64encode(b"fakepng").decode(),
                        "text/plain": ["<Figure>"],
                    },
                    "metadata": {},
                }
            ],
        },
        {
            "cell_type": "code",
            "id": "err-cell",
            "metadata": {},
            "source": ["1/0"],
            "outputs": [
                {
                    "output_type": "error",
                    "ename": "ZeroDivisionError",
                    "evalue": "division by zero",
                    "traceback": ["ZeroDivisionError: division by zero"],
                }
            ],
        },
    ],
}


@pytest.fixture
def nb_path(tmp_path):
    path = tmp_path / "test.ipynb"
    path.write_text(json.dumps(SAMPLE_NB))
    return str(path)


@pytest.fixture
def cells():
    return SAMPLE_NB["cells"]


# ── load_notebook ──


def test_load_notebook(nb_path):
    nb = load_notebook(nb_path)
    assert "cells" in nb
    assert len(nb["cells"]) == 6


def test_load_notebook_missing():
    with pytest.raises(FileNotFoundError):
        load_notebook("/nonexistent.ipynb")


# ── fmt_outputs ──


def test_fmt_outputs_stream(cells):
    assert fmt_outputs(cells[1]) == "hello\n"


def test_fmt_outputs_execute_result(cells):
    assert fmt_outputs(cells[2]) == "42"


def test_fmt_outputs_image(cells):
    # cell has both text/plain and image/png; text/plain takes priority
    assert fmt_outputs(cells[4]) == "<Figure>"


def test_fmt_outputs_error(cells):
    assert "ZeroDivisionError" in fmt_outputs(cells[5])


def test_fmt_outputs_empty(cells):
    assert fmt_outputs(cells[3]) == ""


# ── cmd_list ──


def test_cmd_list(cells, capsys):
    cmd_list(cells)
    out = capsys.readouterr().out
    assert "[mark]" in out
    assert "[code]" in out
    assert "# Title" in out
    assert "import numpy" in out
    lines = out.strip().split("\n")
    assert len(lines) == 6


# ── cmd_show ──


def test_cmd_show_source(cells, capsys):
    cmd_show(cells, 1)
    out = capsys.readouterr().out
    assert "import numpy as np" in out
    assert "--- output ---" not in out


def test_cmd_show_with_output(cells, capsys):
    cmd_show(cells, 1, show_output=True)
    out = capsys.readouterr().out
    assert "import numpy as np" in out
    assert "--- output ---" in out
    assert "hello" in out


def test_cmd_show_out_of_range(cells):
    with pytest.raises(SystemExit):
        cmd_show(cells, 99)


def test_cmd_show_negative(cells):
    with pytest.raises(SystemExit):
        cmd_show(cells, -1)


# ── cmd_search ──


def test_cmd_search_found(cells, capsys):
    cmd_search(cells, "numpy")
    out = capsys.readouterr().out
    assert "── cell 1 (code-1) ──" in out
    assert "import numpy" in out


def test_cmd_search_not_found(cells, capsys):
    cmd_search(cells, "zzz_no_match")
    err = capsys.readouterr().err
    assert "No cells matching" in err


def test_cmd_search_with_output(cells, capsys):
    cmd_search(cells, "numpy", show_output=True)
    out = capsys.readouterr().out
    assert "--- output ---" in out


def test_cmd_search_multiple(cells, capsys):
    cmd_search(cells, "import")
    out = capsys.readouterr().out
    # matches cell 1 ("import numpy") — only one match expected
    assert out.count("── cell") == 1


# ── cmd_img ──


def test_cmd_img_extracts(cells, tmp_path):
    cmd_img(cells, 4, str(tmp_path))
    files = list(tmp_path.glob("*.png"))
    assert len(files) == 1
    assert files[0].read_bytes() == b"fakepng"


def test_cmd_img_default_dir(cells, capsys):
    cmd_img(cells, 4, None)
    out = capsys.readouterr().out.strip()
    assert out.endswith(".png")
    assert os.path.exists(out)
    os.unlink(out)


def test_cmd_img_no_images(cells, capsys):
    cmd_img(cells, 2, None)
    err = capsys.readouterr().err
    assert "No images" in err


def test_cmd_img_out_of_range(cells):
    with pytest.raises(SystemExit):
        cmd_img(cells, 99, None)


# ── cmd_fix_ids ──


def test_fix_ids_adds_missing(tmp_path, capsys):
    path = tmp_path / "noids.ipynb"
    path.write_text(json.dumps(SAMPLE_NB))
    cmd_fix_ids(str(path))
    out = capsys.readouterr().out
    assert "Fixed 1 cell(s)" in out

    nb = json.loads(path.read_text())
    for cell in nb["cells"]:
        assert cell.get("id"), f"Cell missing id: {cell['source']}"


def test_fix_ids_preserves_existing(tmp_path, capsys):
    path = tmp_path / "withids.ipynb"
    path.write_text(json.dumps(SAMPLE_NB))
    cmd_fix_ids(str(path))

    nb = json.loads(path.read_text())
    assert nb["cells"][0]["id"] == "md-0"
    assert nb["cells"][1]["id"] == "code-1"
    assert nb["cells"][2]["id"] == "code-2"


def test_fix_ids_all_present(tmp_path, capsys):
    nb = json.loads(json.dumps(SAMPLE_NB))
    for i, cell in enumerate(nb["cells"]):
        cell["id"] = f"id-{i}"
    path = tmp_path / "allids.ipynb"
    path.write_text(json.dumps(nb))
    cmd_fix_ids(str(path))
    out = capsys.readouterr().out
    assert "All cells already have IDs" in out


# ── CLI integration ──


def test_main_list(nb_path, capsys, monkeypatch):
    from jupycat.cli import main

    monkeypatch.setattr("sys.argv", ["jupycat", nb_path])
    main()
    out = capsys.readouterr().out
    assert "[mark]" in out


def test_main_show(nb_path, capsys, monkeypatch):
    from jupycat.cli import main

    monkeypatch.setattr("sys.argv", ["jupycat", nb_path, "1"])
    main()
    out = capsys.readouterr().out
    assert "import numpy" in out


def test_main_search(nb_path, capsys, monkeypatch):
    from jupycat.cli import main

    monkeypatch.setattr("sys.argv", ["jupycat", nb_path, "-s", "numpy"])
    main()
    out = capsys.readouterr().out
    assert "── cell 1 (code-1) ──" in out


def test_main_fix_ids(tmp_path, capsys, monkeypatch):
    from jupycat.cli import main

    path = tmp_path / "fix.ipynb"
    path.write_text(json.dumps(SAMPLE_NB))
    monkeypatch.setattr("sys.argv", ["jupycat", str(path), "--fix-ids"])
    main()
    out = capsys.readouterr().out
    assert "Fixed" in out
