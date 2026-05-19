# Python style

Baseline style rules. The authoritative external reference is the
[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html);
the rules below either match it or tighten it.

## Formatting

- **Formatter and linter:** `ruff` for both. Never hand-format. Run via
  `uv run ruff format` and `uv run ruff check --fix`.
- **Line length:** 100 cols. (Ruff default of 88 is too cramped for typed
  Python.)
- Trailing commas everywhere they're allowed — they make diffs smaller.

## Python version and imports

- **Python 3.11+** minimum. New projects on 3.12+.
- Start every module with `from __future__ import annotations`. It makes
  all type hints lazy strings and unlocks modern syntax on older
  interpreters.
- **Import order** (enforced by `ruff` / `isort`): stdlib → third-party
  → first-party → local. One blank line between groups.
- **No wildcard imports.** `from module import *` is banned. See
  `code-smells.md`.
- Prefer explicit relative imports inside a package
  (`from .domain import Order`), absolute imports across packages.

## Type hints

- **Mandatory** on every public function: arguments and return type.
- Private helpers get hints when the type isn't obvious to the reader.
- Use modern syntax: `list[str]`, `dict[str, int]`, `X | None`. Not
  `List[str]`, `Optional[X]`. (Requires `from __future__ import
  annotations`.)
- Use `typing.Protocol` for structural typing — prefer it to `abc.ABC`
  unless you need shared state or default implementations (see
  `design.md`).
- `mypy --strict` must pass. Run `uv run mypy src/`.
- `Any` is a code smell. If you must, narrow with `cast()` immediately
  and add a comment justifying it.

## Naming

- `snake_case` for functions, methods, variables, modules.
- `PascalCase` for classes (including `Protocol`s, dataclasses, enums).
- `UPPER_SNAKE_CASE` for module-level constants.
- `_leading_underscore` for non-public attributes (the only thing that
  conveys "private" in Python — `__name_mangling` is for inheritance
  collisions, not privacy).
- Descriptive over abbreviated: `user_count`, not `uc`. Boolean names
  are predicates: `is_active`, `has_payment`, `can_refund`.

## Docstrings (Google style)

```python
def calculate_area(radius: float) -> float:
    """Calculate the area of a circle.

    Args:
        radius: The radius of the circle. Must be non-negative.

    Returns:
        The area, calculated as ``π * radius²``.

    Raises:
        ValueError: If ``radius`` is negative.
    """
    if radius < 0:
        raise ValueError("radius must be non-negative")
    return math.pi * radius**2
```

- One-line summary. Blank line. Optional details. Sections (`Args`,
  `Returns`, `Raises`, `Yields`, `Examples`) as needed.
- Document the *contract*, not the implementation. "Returns the area"
  is documentation; "Multiplies radius by itself and then by pi" is the
  code talking back at the reader.
- Document every exception the function intentionally raises.

## Code structure

- Functions stay small and single-purpose. If you need "and" to
  describe what one does, split it.
- **Early returns / guard clauses** over deeply nested conditionals.
  No "arrow code".
- **List comprehensions:** keep them simple. One `for` and at most one
  `if`. If you need a nested loop or complex expression, write a real
  `for` loop — readability counts.
- **Named constants** for magic numbers and strings used for branching.
  Use `enum.Enum` (or `enum.StrEnum` on 3.11+) for finite sets of named
  values.
- Use `pathlib.Path`, never `os.path` string concatenation.
- Use `dataclasses` for plain structured data. Reach for `pydantic` only
  at the boundary (HTTP payloads, config files) where validation is the
  point — see `design.md`.
- Use `decimal.Decimal` (or integer cents) for money. Never `float`.

## Error handling

- Catch **specific** exceptions, never bare `except:` and never
  `except Exception:` (unless you re-raise after logging at a boundary).
- Define custom exception classes for your domain. Inherit from the
  closest stdlib base (`ValueError`, `LookupError`, etc.). One
  exception class per distinct failure mode.
- Document expected errors in the docstring `Raises:` section.
- Fail fast: validate inputs at function entry, then assume the type
  system is true.
- Do *not* use exceptions for ordinary control flow.

## Async

- Async functions are explicit — `async def` and `await`. Never hide
  async behind a property; properties are an implicit contract that the
  call is cheap and side-effect-free, and `await` violates both
  (see `design.md`).
- Don't mix sync and async in the same call chain. Pick a colour at the
  application service layer.

## Strings

- Prefer f-strings. Don't use `%`-formatting or `.format()` in new code.
- Use triple-quoted strings (`"""..."""`) for docstrings, never `'''`.

## Loose ends to avoid

- **Mutable default arguments** — never `def f(x=[])`. Use `None` and
  build inside.
- **`from x import *`** — never. Pollutes the namespace.
- **`is` for value comparison** — `is` is identity, `==` is equality.
  Use `is` only for `None`, `True`, `False`, and sentinels.
- **`for ... else`** — its semantics surprise readers. Use a flag or a
  helper function.
- **Catching `BaseException`** — it includes `KeyboardInterrupt` and
  `SystemExit`. You almost never want that.
