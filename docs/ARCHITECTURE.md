# Scaffolder architecture

How `ideal-project-scaffolder` is designed and why. Audience: anyone
extending the scaffolder. For day-to-day "how do I add a new question /
language / MCP server", see [TEMPLATE_MAINTENANCE.md](../TEMPLATE_MAINTENANCE.md).

## Goal

Produce projects whose tool surface is **independent of the user's
globally-installed agent plugins**. Two developers cloning the same
rendered project and running the same agent must see the same skills,
conventions, and folder layout. The user's globally-installed plugins
must neither shadow the project's curated skills nor inject competing
conventions.

That goal forces three design moves: closed-world skills, closed-world
plugin governance, and a single enforced layout contract.

## Closed-world principle

The scaffolder ships its own curated skill set under
`template/{{ project_slug }}/{{ ai_folder }}/skills/`. Globally-installed
plugins that overlap with that set are silenced at project scope.
Concretely, when `ai_agent` is `claude` or `universal`, the scaffolder
emits `.claude/settings.json` with:

```json
{
  "enabledPlugins": {
    "superpowers@claude-plugins-official": false,
    "claude-md-management@claude-plugins-official": false,
    "claude-code-setup@claude-plugins-official": false,
    "commit-commands@claude-plugins-official": false
  }
}
```

Project settings override user settings per-key, so listing a plugin as
`false` disables it inside the project even when the user has it on
globally. Four plugins are masked:

| Plugin | Why masked |
| --- | --- |
| `superpowers` | Same Tier-1 / Tier-2 skills are vendored locally; running both surfaces would inject duplicates with subtly different content. |
| `claude-md-management` | The scaffolded `CLAUDE.md` / `AGENTS.md` is a thin skeleton that points into the instruction tree; the plugin would rewrite it against its own template. |
| `claude-code-setup` | The scaffolder *is* the project setup; the plugin would re-recommend its own hooks/skills. |
| `commit-commands` | The vendored skills already cover commit / push / PR flows. |

MCP servers and LSP plugins are **deliberately** left enabled — those
are connectors the user owns, not opinionated workflow tooling.

## Skill governance

Vendored skills live under
`template/{{ project_slug }}/{{ ai_folder }}/skills/`. Two tiers:

- **Tier 1** — always rendered. Plain `SKILL.md.jinja` filename. Lists
  the core engineering discipline (TDD, systematic debugging, verification
  before completion, writing plans, executing plans, requesting /
  receiving code review, writing skills, finishing a development branch).
- **Tier 2** — filename gated by a Copier flag (`include_brainstorming`,
  `enable_worktrees`, `enable_parallel_agents`). Filename pattern:
  `{% if <flag> %}SKILL.md{% endif %}.jinja`. The post-generation hook
  prunes the surrounding skill directory if `SKILL.md` is absent.

Source of truth: `obra/superpowers-skills`, pinned to a tag inside
`copier.yml` (`superpowers_skills_tag`). Refresh tooling lives in
`scripts/refresh-vendored-skills.py`. The script (a) reads the pinned tag,
(b) clones or reuses a local checkout, (c) copies each skill directory
verbatim with the SKILL.md body wrapped in `{% raw %}` / `{% endraw %}`
so Copier treats it as literal text, and (d) regenerates
`ATTRIBUTION.md.jinja` from the upstream LICENSE. To bump the tag, edit
`copier.yml`, run the script, review the diff, commit.

In addition to vendored skills, the scaffolder ships **project-local**
skills (small, narrow recipes like `tdd-cycle`, `design-review`,
`refactor-code-smell`, `lint-and-format`, `run-tests`, `update-changelog`,
plus language-gated ones like `python-uv-setup`). Those are hand-written
inside `template/.../skills/` and are not synced from upstream.

## Layout contract

The single source of truth for "where does X live" is the rendered
project's
`{{ ai_folder }}/instructions/general/architecture.md` — specifically
its "Where things live" table. Every markdown artifact (source code,
tests, tactical plans, feature specs, design notes, architecture docs,
manuals) has exactly one canonical home. The agent instruction files
(`CLAUDE.md` / `AGENTS.md` / `.github/copilot-instructions.md`) point at
the table rather than restating it.

The table ends with: **Do not create new top-level folders.** This is the
durable convention rule that prevents agents from spawning parallel
`plans/`, `specs/`, `design/` trees as side effects of unrelated skills.
When a genuinely new artifact type appears, the workflow is "add a row to
the table, then create the folder" — not the reverse.

## Layout enforcement mechanics

Three mechanisms cooperate to keep the layout intact:

1. **Per-layer README.md inside `src/` and `tests/`.** Each layer ships
   with a short `README.md.jinja` explaining what belongs there. This
   replaces the old `_e2e/`-style underscore-prefix scheme for empty
   directories. Side effect: layers are never empty, so `.gitkeep`
   sentinels are unnecessary in those locations.

2. **`.gitkeep` sentinel + post-generation pruning** for *gated*
   directories (language-specific instruction folders, optional skill
   folders). The directory name is plain (`python/`, `rust/`, …) and
   each file inside is filename-gated by a Copier conditional. A
   `.gitkeep` ships so Copier always creates the directory. After
   render, `_hooks/post_generation.py` walks the tree:
   - Strips stale `.gitkeep` from any directory that ended up with real
     content.
   - Deletes the directory entirely when only the sentinel remains (the
     associated language / skill was not selected).
   - Deletes half-rendered skill directories that lost their `SKILL.md`
     to a conditional but kept support files.
   - Prunes top-level hidden directories (`.claude/`, `.github/`, `.ai/`)
     that ended up hollow because every conditional inside them skipped.

3. **Closed-world plugin governance** (above) — prevents external
   plugins from re-creating parallel folder trees inside the rendered
   project.

## Agent matrix

| Agent | Style | Files emitted |
| --- | --- | --- |
| Claude Code | canonical | `CLAUDE.md`, `.claude/{settings.json,skills/,agents/,instructions/}`, `.mcp.json` |
| Claude Code | generic | `AGENTS.md` + redirect `CLAUDE.md`, `.ai/...`, `.mcp.json` |
| GitHub Copilot CLI | canonical | `.github/copilot-instructions.md`, `.ai/...`, `.vscode/mcp.json` |
| GitHub Copilot CLI | generic | `AGENTS.md` + redirect copilot-instructions, `.ai/...`, `.vscode/mcp.json` |
| Universal | — | `AGENTS.md`, `.ai/...`, `.mcp.json` |

`ai_folder` is computed in `copier.yml`:
- `.claude/` when `ai_agent == 'claude'` and `agent_file_style == 'canonical'`
- `.ai/` otherwise

`.claude/settings.json` is the **one exception**: it always renders into
the literal `.claude/` directory (never into `.ai/`) because Claude Code
only looks there.

**Cursor was dropped.** Cursor's CLI is not mature enough to drive the
plugin-governance and spec-kit setup steps the scaffolder relies on. The
agent matrix only includes editors with a usable headless CLI.

## SDD opt-in (spec-kit)

The scaffolder offers Spec-Driven Development as an opt-in via the
`use_spec_kit` Copier flag. When enabled:

- `general/sdd.md` is rendered (explains how SDD layers above DDD + TDD).
- `Justfile` exposes a `sdd-init` recipe that runs
  `specify init --here --ai <agent> --integration-options "--skills"`.

The scaffolder does **not** pre-render `.specify/` or `specs/`. Those
folders belong to spec-kit; the scaffolder yields ownership of them once
`just sdd-init` runs. The "Where things live" table reserves
`specs/<feature-slug>/` for spec-kit even when the flag is off, so an
agent can never legitimately put feature specs anywhere else.

When `use_spec_kit` is off, the lighter vendored `writing-plans` skill
covers tactical planning (output → `docs/plans/YYYY-MM-DD-<slug>.md`).

## Rejected alternatives

- **Post-generation calls the chosen CLI agent to mutate config.**
  Considered: have the hook shell out to `claude` / `gh copilot` after
  render to enforce settings programmatically. Rejected: introduces a
  runtime dependence on the chosen CLI being present, authenticated, and
  the right version; static `.claude/settings.json` achieves the same
  enforcement with zero failure modes.
- **Keep Cursor as a supported agent.** Rejected: no CLI mature enough
  to drive the plugin-governance and spec-kit setup steps. Keeping it
  would mean shipping a degraded, half-managed Cursor experience.
- **Conditional directory names** (`{% if 'python' in languages %}python{% endif %}/`).
  Rejected: cross-platform unreliability (Copier + Windows path edge
  cases). The proven pattern is plain directory names + per-file
  conditional filenames + `.gitkeep` sentinel + post-generation prune.
- **One opinionated skill set, no opt-out.** Rejected: Tier-2 skills
  (brainstorming, worktrees, parallel agents) have real cost in context
  and discipline. Solo projects and library work usually don't need
  them; making them opt-in keeps the default surface lean.

## File-by-file overview

```
copier.yml                          # Questionnaire + computed vars + banner + post-copy message
README.md                           # User-facing quickstart
TEMPLATE_MAINTENANCE.md             # How to extend (per-task playbook)
docs/ARCHITECTURE.md                # This file — design rationale
_hooks/post_generation.py           # Render-time tree-cleaning hook
scripts/refresh-vendored-skills.py  # Pull upstream superpowers @ pinned tag
template/{{ project_slug }}/        # Everything below is rendered into the new project
```

Inside `template/{{ project_slug }}/`:

```
.claude/settings.json.jinja                   # Plugin governance (Claude/universal)
.mcp.json.jinja                                # Project-scope MCP servers (Claude/universal)
.vscode/mcp.json.jinja                         # Same, for Copilot
.github/copilot-instructions.md.jinja          # Copilot canonical agent file
.github/workflows/ci.yml.jinja                 # Optional starter CI
AGENTS.md.jinja                                # Universal / generic-style agent file
CLAUDE.md.jinja                                # Claude canonical agent file
Justfile.jinja                                 # Task runner + agent helpers + sdd-init
{{ ai_folder }}/agents/                        # Subagent definitions
{{ ai_folder }}/instructions/general/          # Language-agnostic rules (always loaded)
{{ ai_folder }}/instructions/<lang>/           # Per-language rules (filename-gated)
{{ ai_folder }}/skills/                        # Vendored Tier-1 + Tier-2 + project-local
src/{domain,application,infrastructure,presentation}/README.md.jinja
tests/{unit,integration,e2e,performance}/README.md.jinja
scripts/mcp_check.py.jinja                     # `just mcp` diagnostic
```

`{{ ai_folder }}` resolves to `.claude/` or `.ai/` based on the agent
choice; `.claude/settings.json` is the exception that always lands in
`.claude/`.
