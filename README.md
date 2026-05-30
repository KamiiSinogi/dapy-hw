# Dapy Template Project

A ready-to-use template for developing distributed algorithms with **dapy** and visualizing traces with **dapyview**.

The [dapy repository](https://github.com/xdefago/dapy) contains additional information.

## Prerequisites

- **Python 3.13+**
- **git** installed (required because dependencies are installed from GitHub)
- **uv** (recommended)

> If you do not have git installed: on macOS install Xcode Command Line Tools; on Windows install Git for Windows; on Linux install the `git` package from your distro.

## Quick Start (using the template on GitHub)

1. Go to https://github.com/xdefago/dapy-template
2. Click **Use this template** to create your own repository.
3. Clone your new repo and install dependencies:

### Using uv
```bash
uv sync
```
Continue directly at the verification of the installation.

> `uv sync` installs **dapyview** (trace viewer) automatically because this template includes the GUI runtime dependencies via `dapy[ui]`.

## Verify Installation

```bash
uv run python -c "import importlib.metadata as m; print(m.version('dapy'))"
```

## Project Structure

```
.
├── README.md
├── pyproject.toml
├── requirements.txt
├── requirements-json.txt
├── src/
│   ├── broadcast/             # Working example: flooding broadcast
│   │   ├── __init__.py
│   │   ├── run_bcast.py
│   │   └── algo/
│   │       ├── __init__.py
│   │       └── algorithm.py
│   └── my_algo/               # Your algorithm template
│       ├── __init__.py
│       ├── algorithm.py
│       └── run_my_algo.py
├── tests/
│   └── test_broadcast.py
└── traces/                    # Trace outputs
```

## Run the Example (Broadcast)

```bash
uv run run-bcast
```

This creates a trace file in traces/ and prints basic statistics.

### Visualize with dapyview

```bash
uv run dapyview traces/broadcast_trace.pkl
```

Why `uv run`?
- `uv` installs executables (like `dapyview`) inside the project’s `.venv/bin/` directory.
- `uv run ...` automatically uses that environment, so you don’t need to activate it or modify your PATH.

If you prefer a one-time setup, you can activate the venv and then run `dapyview` directly:
```bash
source .venv/bin/activate
dapyview traces/broadcast_trace.pkl
```

If you see `ModuleNotFoundError: No module named 'PySide6'`, run:
```bash
rm uv.lock
uv sync
```
This ensures the GUI dependencies are installed.

## Start Your Own Algorithm

1. Edit `src/my_algo/algorithm.py`
2. Uncomment and wire your algorithm in `src/my_algo/run_my_algo.py`
3. Run it:

```bash
uv run run-my-algo
```

NB: you can of course rename `my_algo` to a more explicit and informative name. To do this, you need to update the python file as well as adapt the `pyproject.toml` file with the new name.

## Dependency Notes (GitHub sources)

All dependencies use GitHub URLs (e.g., `dapy[ui] @ git+https://github.com/xdefago/dapy.git`).
Make sure:
- You have git installed
- Your network allows GitHub access (https)

If you cannot use GitHub dependencies, you can later replace them with a PyPI release when available.

## Tests

You can run tests if you installed `pytest` with the developper dependencies with `uv sync`.

```bash
uv run pytest
```

## Links

- dapy: https://github.com/xdefago/dapy
- dapyview guide: https://xdefago.github.io/dapy/dapyview-guide.html
- API docs: https://xdefago.github.io/dapy/api

---

## License

Use any license you prefer for your own repository.

## Appendix: Alternative installers (for advanced users)

If you already know what you're doing and prefer another tool, you can install
dependencies with your tool of choice:

- **pip**: `pip install -r requirements.txt`
- **poetry**: `poetry install`

Most users should ignore this appendix and just use `uv`.
