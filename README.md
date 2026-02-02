# Building the docs

## Prerequisites

- Python >= 3.11
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
uv venv
uv sync --extra docs
```

## Build

```bash
uv run sphinx-build -b html docs docs/_build
```

## Preview

```bash
uv run python -m http.server 8000 --directory docs/_build
```

Open [http://localhost:8000](http://localhost:8000).
