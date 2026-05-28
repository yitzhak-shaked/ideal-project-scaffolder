# Template Maintenance Manual

How to extend this scaffolder. The template is intentionally simple — almost
all logic lives in `copier.yml` (the questionnaire) and in Jinja conditionals
inside template files. There is no custom rules engine.

## Layout

```
copier.yml                # The questionnaire
README.md                 # User-facing quickstart
TEMPLATE_MAINTENANCE.md   # This file
_hooks/post_generation.py # Post-render cleanup (underscore empty dirs)
template/                 # Everything below is rendered into the target project
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
- `template/{{ ai_folder }}/instructions/{% if 'python' in languages %}python{% endif %}/`
  — Python-specific. The folder name is itself a Jinja gate; the whole
  subtree is skipped if Python isn't selected.
- New languages should mirror the Python pattern: create a sibling
  folder gated by `'<lang>' in languages` and populate it with the
  same shape (`zen.md`/style/tooling/design/patterns/code-smells/testing).

To add a file:

1. Create `template/{{ ai_folder }}/instructions/<bucket>/your-topic.md.jinja`.
2. Add a link to it in:
   - the relevant `README.md.jinja` inside that bucket (the human-facing index), and
   - the agent file templates (`CLAUDE.md.jinja` uses `@`-mentions;
     `AGENTS.md.jinja`, `.cursorrules.jinja`, and
     `.github/copilot-instructions.md.jinja` use plain markdown links).
3. If the file should only render when a particular question was
   answered a particular way, gate its filename (not its content):
   `template/.../{% if condition %}your-topic.md{% endif %}.jinja`.

## Adding a new skill or subagent

- **Skill:** `template/{{ ai_folder }}/skills/<skill-name>/SKILL.md.jinja`.
  Must have YAML frontmatter with `name` and `description`. The
  description is the primary trigger — make it specific and "pushy"
  about when to invoke. Optional `scripts/`, `references/`, `assets/`
  subdirectories per the Anthropic skill format.
- **Subagent:** `template/{{ ai_folder }}/agents/<agent-name>.md.jinja`.
  Must have YAML frontmatter with `name` and `description`. The body
  is the role prompt.
- Language- or domain-specific skills/agents: gate the *folder or
  filename* with Jinja (e.g.
  `template/.../skills/{% if 'python' in languages %}python-uv-setup{% endif %}/SKILL.md.jinja`).

## The `{{ ai_folder }}` directory

`ai_folder` is computed in `copier.yml` from `ai_agent` + `agent_file_style`:
- Claude canonical → `.claude/`
- Cursor canonical → `.cursor/`
- Anything else → `.ai/`

Everything under `template/{{ ai_folder }}/` is rendered into that
agent-appropriate location. References inside agent files use
`{{ '{{ ai_folder }}' }}/instructions/...` so links survive the rename.

## Adding a new agent

1. Add the choice to `ai_agent` in `copier.yml`.
2. Create a conditional template file at the path that agent expects, e.g.
   `template/{% if ai_agent == 'newagent' and agent_file_style == 'canonical' %}.newagent.md{% endif %}.jinja`.
3. Mirror the section structure of the existing agent files (BOOTSTRAP block,
   instructions link, MCP note).

## Post-generation hook

`_hooks/post_generation.py` runs after Copier renders. It only does one
thing: walks the output tree and renames empty directories (or directories
containing only `.gitkeep`) to `_<name>/`. If you need additional cleanup
work after generation, add it there — keep it idempotent and safe to rerun.

## Testing changes

After editing the template, smoke-test renders into temp directories:

```sh
uvx copier copy --defaults . /tmp/scaffold-smoke-1
uvx copier copy . /tmp/scaffold-smoke-2   # interactive, exercise different answers
```

Diff the outputs against expectations and inspect the agent file, MCP config,
and language manifests to confirm conditionals fire correctly.
