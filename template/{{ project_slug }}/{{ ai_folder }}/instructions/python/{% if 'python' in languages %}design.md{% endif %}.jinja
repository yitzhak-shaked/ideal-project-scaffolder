# Python design philosophy

This file encodes the design heuristics this codebase optimises for.
Heavily inspired by Arjan Egberts's *Software Designer Mindset* and the
ArjanCodes corpus. Pair this file with `patterns.md` (the concrete
recipes) and `code-smells.md` (what to refactor against).

## Foundational stance

- **Design starts before the first line of code.** Distil the model
  ruthlessly. The best refactor is removing code.
- **Design serves the end user.** Resist the engineer's instinct to
  build a generic, infinitely-configurable system when a small,
  hardcoded one would do.
- **Implementation and design run in parallel.** A crude prototype is a
  research instrument; let it teach you what the model should be.

## Functions vs classes — choose deliberately

> Use **functions** when the code is action-focused.
> Use **classes** when the code is state-focused.

Default to functions. Reach for a class when you have genuine internal
state that multiple instances need, that gets cloned, updated, or
passed around. Symptoms that you reached too soon:

- A class with `__init__` and one method.
- A class whose methods are all `@staticmethod`. That should be a
  module of free functions.
- A "Manager" / "Helper" / "Utility" class. Almost always: a module
  of functions.

## Composition over inheritance

Inheritance is one of the strongest, most brittle forms of coupling.
Default to **composition**: assemble behaviour by injecting collaborators
defined by a `Protocol`. Shallow, narrow inheritance hierarchies are
sometimes fine; mixins and multiple inheritance almost never are.

```python
# Avoid: rigid taxonomy.
class Employee: ...
class SalariedEmployee(Employee): ...
class HourlyEmployee(Employee): ...

# Prefer: behaviour injected as a dependency.
class Contract(Protocol):
    def compute_payment(self) -> Money: ...

@dataclass(frozen=True)
class Employee:
    name: str
    id: EmployeeId
    contract: Contract  # ← swap implementations freely
```

## Separate creation from use (Dependency Injection)

Objects rarely instantiate their own dependencies. Pass them in
through the constructor (or function argument). The benefits:

- Testable without monkey-patching.
- Replaceable without surgery.
- Honest about coupling: every dependency is visible at the call site.

**Composition root.** All real wiring lives at exactly one place: the
entry point (`presentation/server.py`, `presentation/cli.py`, the
FastAPI app factory, `__main__`). The domain layer is *ignorant* of how
its dependencies are built.

For complex applications with many wirings, consider a DI framework
(`dishka`, `dependency-injector`, FastAPI's built-in `Depends`). For
small ones, plain constructor injection is enough.

## Abstract base classes vs Protocols

Python offers two abstraction mechanisms. **Default to `Protocol`.**

| | `abc.ABC` | `typing.Protocol` |
| --- | --- | --- |
| Subtyping | Nominal (must inherit) | Structural (must match shape) |
| Coupling | Higher (concrete must know the ABC) | Lower (abstraction defined next to use) |
| Shared state / default methods | Yes | No |
| Use when | You need shared implementation. | You need an interface for decoupling. |

Define the `Protocol` next to where it's *used* (in the domain or
application layer), not next to where it's implemented. The implementer
doesn't even need to know the Protocol exists — that's the point.

## Properties vs methods — the hidden contract

`@property` is not a syntactic sugar for "method with no arguments". It
is a contract with the caller:

- The operation is **cheap** (constant or near-constant time).
- The operation has **no side effects**.
- The operation cannot fail in surprising ways (no network, no I/O).

If any of these is false, write a method. **Never write an async
property** — `await` implies I/O, which violates the contract.

## Data-first design

> Resolve the data before the methods.

- **Dataclasses** (`@dataclass(frozen=True)` by default) for internal
  domain types — entities, value objects.
- **Pydantic** for the *boundary*: parsing HTTP payloads, validating
  config files, anywhere untrusted input enters. Keep Pydantic out of
  the domain — it drags in a dependency the domain shouldn't have.
- Translate Pydantic models into dataclasses (or the entity's
  factory method) as input crosses from `presentation/` into
  `application/`.

## Make invalid states unrepresentable

Use the type system to eliminate edge cases instead of writing tests
for them.

- `enum.Enum` (or `StrEnum`) for finite sets of named values, not raw
  strings.
- Frozen dataclasses with validation in `__post_init__` for value
  objects (a `Money` that cannot be negative, an `Email` that cannot
  be malformed).
- `decimal.Decimal` (or integer cents) for money. Never `float`.
- `pathlib.Path` for filesystem paths, not `str`.

If a function can't fail because its inputs are *typed* such that the
failure mode doesn't exist, you don't need a test for that failure
mode. Design out the edge case rather than asserting against it.

## Three-layer pattern (web apps)

For FastAPI / Flask / Django-style web apps, follow Clean / Hexagonal
architecture (already encoded in `general/architecture.md`):

- **Routers** (`presentation/`) — HTTP, parsing, the composition root.
- **Operations / Use cases** (`application/`) — business logic
  orchestration. Depends only on `domain/` protocols.
- **Repositories** (`infrastructure/`) — DB / external system adapters
  implementing `domain/` interfaces.

The middle layer must be ignorant of FastAPI *and* of SQLAlchemy. If
your use case imports either, the layering is wrong.

## Heuristics in a hurry

- If two pieces of code look alike but represent different domain
  concepts, **leave the duplication**. DRY is about reasons to change,
  not visual similarity.
- If you're about to add a boolean flag parameter, pause and read
  `patterns.md` (Policy pattern).
- If you're about to write `isinstance(x, T)` to choose behaviour,
  pause and use polymorphism or a dispatch table.
- If your function has more than ~4 arguments, group them into a
  context object.
- If a comment starts with "this is a hack because", file an issue and
  link it from the comment.
