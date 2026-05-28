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

**3. (If you picked MCP servers)** Inside the new project:

```sh
cp .env.example .env     # then fill in any required tokens
just mcp                 # diagnostic: tells you what's missing and how to fix it
```

`just mcp` checks runtimes (npx, uvx), reports missing env vars, and lists
one-time setup commands (e.g. `npx playwright install`).

**For Claude Code users:** project-scoped MCP servers in `.mcp.json` require
a one-time **approval** before Claude will load them. Start a session in
the project directory:

```sh
claude
```

Claude prompts: *"`.mcp.json` contains N MCP servers. Allow?"* — answer yes.
The approval is saved to `.claude/settings.local.json` and persists. Until
you do this, `claude mcp list` will only show your account-level
(`claude.ai *`) servers, not the project ones.

## What you get

- An agent file (`CLAUDE.md`, `.github/copilot-instructions.md`, or
  `AGENTS.md`) configured for your agent of choice (Claude Code, GitHub
  Copilot CLI, or Universal). Cursor is not supported.
- An agent workspace folder — `.claude/` for Claude canonical, `.ai/`
  otherwise — containing `instructions/` (coding conventions per chosen
  language, architecture, testing, security), `skills/` (a curated set
  of skills vendored from `obra/superpowers-skills` — TDD, systematic
  debugging, verification, writing/executing plans, code-review,
  optionally brainstorming and worktree/parallel-agent skills — plus
  project-local task skills), and `agents/` (subagent definitions).
- A preconfigured `.mcp.json` (or `.vscode/mcp.json`) with the MCP servers
  you selected.
- A project-scope `.claude/settings.json` that silences globally-installed
  Claude Code plugins which overlap with the vendored skills (superpowers,
  claude-md-management, claude-code-setup, commit-commands). MCP servers
  and LSP plugins are left alone.
- Language manifests for every language you ticked (`Cargo.toml`,
  `pyproject.toml`, `package.json`, `CMakeLists.txt`).
- DDD `src/{application,domain,infrastructure,presentation}` and full
  `tests/{unit,integration,e2e,performance}` layout, each layer with a
  `README.md` that explains what belongs there.
- `Justfile`, `.gitignore`, `.env.example`, optional `.github/workflows/ci.yml`,
  and `.vscode/` settings.

## Optional: Spec-Driven Development

If you answered "yes" to **Use Spec-Driven Development (SDD) via
GitHub spec-kit?** during the questionnaire, the rendered Justfile
ships a `sdd-init` recipe. Run it once to overlay spec-kit's slash
commands and `.specify/` infrastructure:

```sh
just sdd-init
```

This installs spec-kit's CLI and runs `specify init --here --ai <agent>
--integration-options "--skills"`, which lands the `/speckit.*` commands
and `speckit-*` skills inside `.claude/skills/` alongside the vendored
superpowers skills. spec-kit creates `.specify/memory/constitution.md`
and `specs/<feature>/` natively; the scaffolder does not pre-render
either.

## Extending the template

See [TEMPLATE_MAINTENANCE.md](TEMPLATE_MAINTENANCE.md) for how to add a new
question, language, MCP server, instruction file, or vendored skill.
