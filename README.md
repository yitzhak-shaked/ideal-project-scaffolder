# ideal-project-scaffolder

A Copier-based meta-template for spinning up AI-ready project workspaces. One
questionnaire produces a tailored scaffold: per-language manifests, an agent
instruction file in the convention your chosen agent expects, preconfigured
MCP servers, per-domain instruction files, and the usual DDD source / test
layout.

## Quickstart

**1. Install `uv` (one time):**

- macOS / Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

**2. Generate a project** into an empty directory:

```sh
uvx copier copy gh:<your-user>/ideal-project-scaffolder ./my-new-project
```

Or from a local clone:

```sh
uvx copier copy /path/to/ideal-project-scaffolder ./my-new-project
```

You will be asked a short series of questions (languages, domain, AI agent,
MCP servers, …). When it finishes, the new project is ready to open in your
editor.

## What you get

- An agent file (`CLAUDE.md`, `.cursorrules`, `.github/copilot-instructions.md`,
  or `AGENTS.md`) configured for your agent of choice. It links to the
  per-domain instruction set under `.ai/instructions/`.
- `.ai/instructions/` containing `coding-conventions.md` (per chosen language),
  `architecture.md`, `testing.md`, `security.md`.
- A preconfigured `.mcp.json` (or `.vscode/mcp.json`) with the MCP servers you
  selected.
- Language manifests for every language you ticked (`Cargo.toml`,
  `pyproject.toml`, `package.json`, `CMakeLists.txt`).
- DDD `src/{application,domain,infrastructure,presentation}` and full
  `tests/{unit,integration,e2e,performance}` layout. Empty dirs are
  underscore-prefixed (`_e2e/`) so they're visibly inert until you fill them.
- `Justfile`, `.gitignore`, `.env.example`, optional `.github/workflows/ci.yml`,
  and `.vscode/` settings.

## Extending the template

See [TEMPLATE_MAINTENANCE.md](TEMPLATE_MAINTENANCE.md) for how to add a new
question, language, MCP server, or instruction file.
