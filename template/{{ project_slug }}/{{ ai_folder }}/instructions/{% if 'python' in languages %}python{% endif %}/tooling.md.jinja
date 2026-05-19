# Python tooling

This project uses [`uv`](https://docs.astral.sh/uv/) for everything that
touches the Python environment. **Never invoke `python`, `pip`,
`virtualenv`, `pyenv`, `poetry`, or `pipx` directly.** Always go through
`uv`.

## Why uv

`uv` resolves and installs dependencies orders of magnitude faster than
pip+venv, manages the Python interpreter itself, locks transitive
dependencies deterministically, and runs commands inside the project's
environment without any "activate the venv first" ceremony. It replaces
`pip`, `pip-tools`, `pipx`, `virtualenv`, `pyenv`, and most of `poetry`.

## The commands you actually need

| Action | Command | Notes |
| --- | --- | --- |
| Initialise a new project | `uv init` | Creates `pyproject.toml`, `.python-version`, `README.md`. |
| Install all deps from the lockfile | `uv sync` | Idempotent. Creates / updates `.venv/`. |
| Add a runtime dependency | `uv add <pkg>` | Edits `pyproject.toml` and `uv.lock`, installs. |
| Add a dev dependency | `uv add --dev <pkg>` | E.g. `uv add --dev pytest`. |
| Remove a dependency | `uv remove <pkg>` | Reverse of `uv add`. |
| Run a command | `uv run <cmd> [args]` | Runs in the project env without activating it. |
| Refresh the lockfile | `uv lock` | Re-resolves transitive deps. Usually automatic. |
| Upgrade one package | `uv lock --upgrade-package <pkg>` | Upgrades just that one and its transitives. |
| Upgrade everything | `uv lock --upgrade` | Within version constraints in pyproject. |

## The rule

> **If you need to run any Python command in this project, prefix it
> with `uv run`.**

Examples:

```sh
uv run pytest                  # run tests
uv run pytest -k refund        # run one test
uv run pytest --watch          # via pytest-watch / ptw
uv run ruff format .           # format
uv run ruff check . --fix      # lint + auto-fix
uv run mypy src/               # type-check
uv run python script.py        # ad-hoc script
uv run python -c "import this" # one-off REPL command
```

`uv run` ensures the lockfile is up to date and the environment matches
the lockfile *before* running. You will never hit "wrong package version"
problems.

## What gets committed

- `pyproject.toml` — yes.
- `uv.lock` — **yes**. Commit it for libraries *and* applications. It
  pins transitive dependencies for reproducible builds and CI.
- `.python-version` — yes. Pins the interpreter.
- `.venv/` — **no**. Add to `.gitignore`.

## The toolchain

This project standardises on the Astral / Pythonista stack:

| Tool | Purpose | Command |
| --- | --- | --- |
| `uv` | Env + deps + interpreter | `uv ...` |
| `ruff` | Lint + format | `uv run ruff format .`, `uv run ruff check .` |
| `mypy` | Static type-check (strict mode) | `uv run mypy src/` |
| `pytest` | Test runner | `uv run pytest` |
| `pytest-cov` | Coverage | `uv run pytest --cov=src` |
| `hypothesis` | Property-based testing | (used via pytest) |
| `mutmut` | Mutation testing | `uv run mutmut run` |
| `pre-commit` | Local hooks (optional but recommended) | `uv run pre-commit run --all-files` |

## Justfile recipes

Prefer the project's `Justfile` recipes over remembering subcommand
syntax:

- `just py-test` — run tests.
- `just py-fmt` — format with ruff.
- `just py-lint` — lint with ruff.
- `just py-typecheck` — type-check with mypy.

`just test` and `just lint` run all languages.

## Anti-patterns

- ❌ `python -m pip install <pkg>` — use `uv add <pkg>`.
- ❌ `python script.py` — use `uv run python script.py`.
- ❌ `pytest` (bare) — use `uv run pytest`.
- ❌ Asking the user to "activate the venv" — `uv run` doesn't need that.
- ❌ Editing `uv.lock` by hand — let `uv lock` regenerate it.
- ❌ `requirements.txt`, `setup.py`, `setup.cfg`, `Pipfile` — this
  project uses `pyproject.toml` only.
