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

**2. Generate a project** — `.` as the destination is the recommended
usage. The scaffolder asks for the project name as the first question
and creates a folder of that name inside your current directory:

```sh
uvx copier copy --trust gh:yitzhak-shaked/ideal-project-scaffolder .
```

Or from a local clone:

```sh
uvx copier copy --trust /path/to/ideal-project-scaffolder .
```

You'll be asked a short series of questions (project name, languages,
domain, AI agent, MCP servers, …). When it finishes, a new folder named
after your project (slugified — `"My Cool App"` → `my-cool-app/`)
appears in the current directory, ready to open.

> You can also pass any other directory as the destination
> (`uvx copier copy --trust gh:... ~/projects`) and the new project
> folder will be created inside it.

**3. (If you picked MCP servers)** Inside the new project, set up env vars
and verify in one command:

```sh
cp .env.example .env     # then fill in any required tokens
just mcp                 # diagnostic: tells you what's missing and how to fix it
```

`just mcp` is the single-command MCP-setup workflow. It checks the required
runtimes (npx, uvx), reports missing env vars, and lists any one-time
setup commands (e.g. `npx playwright install` for the Playwright server).

## What you get

- An agent file (`CLAUDE.md`, `.cursorrules`, `.github/copilot-instructions.md`,
  or `AGENTS.md`) configured for your agent of choice. It links to the
  per-domain instruction set under the agent workspace folder.
- An agent workspace folder — named `.claude/` for Claude canonical, `.cursor/`
  for Cursor canonical, `.ai/` otherwise — containing `instructions/`
  (`coding-conventions.md` per chosen language, `architecture.md`,
  `testing.md`, `security.md`), `skills/` (starter project skills), and
  `agents/` (subagent definitions).
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
