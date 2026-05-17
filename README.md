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

**2. Generate a project.** The last argument is the destination directory —
**use the name you want your project to have**, the scaffolder will pre-fill
`project_name` from it:

```sh
uvx copier copy --trust gh:yitzhak-shaked/ideal-project-scaffolder <your-project-name>
```

Examples:

```sh
uvx copier copy --trust gh:yitzhak-shaked/ideal-project-scaffolder hello-rust
# creates ./hello-rust/ and defaults project_name to "hello-rust"
```

Or from a local clone:

```sh
uvx copier copy --trust /path/to/ideal-project-scaffolder my-cool-app
```

You'll be asked a short series of questions (languages, domain, AI agent,
MCP servers, …). When it finishes, the new project is ready to open in your
editor.

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
