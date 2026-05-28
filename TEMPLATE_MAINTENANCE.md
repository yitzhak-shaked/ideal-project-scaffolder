# Template Maintenance Manual

How to extend this scaffolder. The template is intentionally simple — almost
all logic lives in `copier.yml` (the questionnaire) and in Jinja conditionals
inside template files. There is no custom rules engine.

## Closed-world design

This scaffolder produces projects that ship with their own curated tool
surface. The intent: a developer running an agent inside a rendered
project should see the same skills, conventions, and folders regardless of
what plugins they have installed globally.

Concretely:

- **Skills are vendored**, not assumed. Tier-1 and selected Tier-2 skills
  from `obra/superpowers-skills` are copied into
  `template/{{ project_slug }}/{{ ai_folder }}/skills/` at refresh time
  (see "Refreshing vendored skills" below).
- **Global plugins that overlap with vendored skills are silenced** at
  project scope via `enabledPlugins` in
  `template/{{ project_slug }}/.claude/settings.json.jinja`. Project
  settings override user settings per-key, so plugins listed there with
  `false` are disabled inside this project even when the user has them
  enabled globally.
- **MCP servers and LSP plugins are deliberately left alone** — they're
  "connectors" the user controls, not opinionated workflow plugins.

If a new well-known plugin emerges that overlaps with our vendored skills,
add it to the `enabledPlugins` map in `.claude/settings.json.jinja`.

## Layout

```
copier.yml                          # The questionnaire
README.md                           # User-facing quickstart
TEMPLATE_MAINTENANCE.md             # This file
_hooks/post_generation.py           # Post-render cleanup
scripts/refresh-vendored-skills.py  # Re-pull upstream superpowers skills
template/                           # Everything below is rendered into the target project
```

Files in `template/` ending in `.jinja` are processed; the suffix is stripped
from the output filename. Filenames themselves are Jinja-evaluated — a
filename that renders to the empty string is skipped, which is how
conditional file emission works.

## Supported agents

- **Claude Code** (canonical: `CLAUDE.md`; generic: `AGENTS.md` + redirect)
- **GitHub Copilot CLI** (canonical: `.github/copilot-instructions.md`;
  generic: `AGENTS.md` + redirect)
- **Universal** (just `AGENTS.md`)

Cursor was dropped in May 2026: it lacks a CLI mature enough to drive the
plugin-governance / spec-kit setup steps this scaffolder relies on.

## Adding a new question

1. Edit `copier.yml` and add a new variable block. Pick `type: bool` for
   yes/no, `type: str` with `choices:` for picklists, `multiselect: true`
   for multi-select.
2. Reference the answer in any template file with `{{ variable_name }}` or
   gate sections with `{% if variable_name == '...' %}…{% endif %}`.

## Adding a new language

1. Add the language to the `languages` choices in `copier.yml`.
2. Add a manifest template under `template/`, conditional on the new
   language being selected. Example:
   ```
   template/{% if 'golang' in languages %}go.mod{% endif %}.jinja
   ```
3. Add a per-language section to `template/.gitignore.jinja` and
   `template/Justfile.jinja` inside `{% if 'golang' in languages %} … {% endif %}`.
4. Add a coding conventions section to
   `template/{{ ai_folder }}/instructions/coding-conventions.md.jinja`.
5. If relevant, add a CI step to `template/.github/workflows/ci.yml.jinja`.

## Adding a new MCP server

1. Add the option to the `mcp_servers` choices in `copier.yml`.
2. Add a JSON stanza to `template/.mcp.json.jinja` and
   `template/.vscode/mcp.json.jinja`, gated by
   `{% if 'your-server' in mcp_servers %}…{% endif %}`.
3. If it needs environment variables, add them (commented) to
   `template/.env.example.jinja`.

## Adding a new instruction file

Instructions are split by audience:

- `template/{{ ai_folder }}/instructions/general/` — language-agnostic
  rules (always loaded).
- `template/{{ ai_folder }}/instructions/python/` — Python-specific.

**Gating rule (important):** language subtrees use **plain folder names**
(`python/`, `rust/`, …) and gate **each file inside** with a conditional
filename, e.g.
`python/{% if 'python' in languages %}style.md{% endif %}.jinja`.

Do **not** gate the folder name itself (e.g.
`{% if 'python' in languages %}python{% endif %}/`). Conditional directory
names render unreliably across Copier versions and on Windows. Per-file
gating is the proven pattern. There is a `.gitkeep` in each language
folder so Copier always creates the directory; the post-generation hook
prunes empty `instructions/` and `skills/` children as a safety net.

To add a file:

1. Create `template/{{ ai_folder }}/instructions/<bucket>/your-topic.md.jinja`.
2. Add a link to it in:
   - the relevant `README.md.jinja` inside that bucket (the human-facing index), and
   - the agent file templates (`CLAUDE.md.jinja` uses `@`-mentions;
     `AGENTS.md.jinja` and `.github/copilot-instructions.md.jinja` use
     plain markdown links).
3. If the file should only render when a particular question was
   answered a particular way, gate its filename (not its content):
   `template/.../{% if condition %}your-topic.md{% endif %}.jinja`.

## Adding a new project-local skill or subagent

- **Skill:** `template/{{ ai_folder }}/skills/<skill-name>/SKILL.md.jinja`.
  Must have YAML frontmatter with `name` and `description`. The
  description is the primary trigger — make it specific and "pushy"
  about when to invoke. Optional `scripts/`, `references/`, `assets/`
  subdirectories per the Anthropic skill format.
- **Subagent:** `template/{{ ai_folder }}/agents/<agent-name>.md.jinja`.
  Must have YAML frontmatter with `name` and `description`. The body
  is the role prompt.
- Language- or domain-specific skills/agents: gate the *filename* with
  Jinja, never the folder name.

## Refreshing vendored skills (upstream superpowers updates)

The Tier-1 / Tier-2 superpowers skills under
`template/{{ project_slug }}/{{ ai_folder }}/skills/` are vendored at a
pinned tag. To bump:

1. Edit the `superpowers_skills_tag` default in `copier.yml`.
2. Run:
   ```
   python scripts/refresh-vendored-skills.py
   ```
   The script clones `obra/superpowers-skills` at the pinned tag and
   re-copies the curated skill directories, wrapping each `SKILL.md`
   body in `{% raw %}` / `{% endraw %}` so Copier treats it as literal.
   To work offline against a local checkout (e.g. the plugin cache),
   pass `--source <path>`.
3. Review the diff, run smoke tests, commit.

The Tier-1 / Tier-2 lists live inside the script. To vendor a different
skill, add its name to the `TIER_1` list (always rendered) or `TIER_2`
map (rendered only when the named quiz var is true).

`ATTRIBUTION.md.jinja` is regenerated automatically from the upstream
LICENSE every time the script runs.

## The `{{ ai_folder }}` directory

`ai_folder` is computed in `copier.yml` from `ai_agent` + `agent_file_style`:
- Claude canonical → `.claude/`
- Anything else → `.ai/`

Everything under `template/{{ ai_folder }}/` is rendered into that
agent-appropriate location. References inside agent files use
`{{ '{{ ai_folder }}' }}/instructions/...` so links survive the rename.

`.claude/settings.json` is the **exception**: it's rendered into the
literal `.claude/` directory (not `{{ ai_folder }}`) because that's where
Claude Code looks regardless of how the rest of the project is named.

## Adding a new top-level agent

Currently `ai_agent` accepts `claude`, `copilot`, `universal`. To add another:

1. Add the choice to `ai_agent` in `copier.yml`.
2. Update `ai_folder`'s computation if the agent has a native folder name.
3. Create a conditional template file at the path that agent expects.
4. Mirror the section structure of the existing agent files (BOOTSTRAP block,
   instructions link, MCP note).
5. If the agent has a CLI that supports per-project plugin governance,
   render a settings file equivalent to `.claude/settings.json`.

## Post-generation hook

`_hooks/post_generation.py` runs after Copier renders. It does three things:

1. Strips `.gitkeep` sentinels from directories that ended up with real content.
2. Prunes empty children under `instructions/` and `skills/` parents (so an
   unselected language doesn't leave an empty folder behind).
3. Prunes empty top-level hidden dirs (`.claude/`, `.github/`, `.vscode/`,
   `.ai/`) whose conditional contents all skipped.

If you need additional cleanup, add it there — keep it idempotent and safe
to rerun. The hook no longer does the underscore-prefix rename that older
versions did; DDD folders (`src/domain/`, etc.) ship with explanatory
`README.md` files so they're never empty.

## Canonical artifact locations

The rendered project's `{{ ai_folder }}/instructions/general/architecture.md`
has a "Where things live" table that names a canonical home for every
markdown artifact (plans, specs, design notes, etc.) and forbids creating
new top-level folders. This is the single durable convention rule. Don't
duplicate it in `CLAUDE.md` / `AGENTS.md` — keep that file's "Source
layout" section a one-paragraph pointer back to `architecture.md`.

## Testing changes

After editing the template, smoke-test renders into temp directories:

```sh
uvx copier copy --defaults . /tmp/scaffold-smoke-1
uvx copier copy . /tmp/scaffold-smoke-2   # interactive, exercise different answers
```

Diff the outputs against expectations. Things worth checking:

- `src/{domain,application,infrastructure,presentation}/README.md` exist
  and are not empty.
- `.claude/settings.json` is present (Claude / Universal renders).
- `.claude/skills/` (or `.ai/skills/`) contains the Tier-1 skills plus
  whichever Tier-2 skills the quiz answers selected.
- No `.cursorrules` is ever produced.
- No `specs/` is pre-rendered; `just sdd-init` is what creates it when
  `use_spec_kit` is true.
