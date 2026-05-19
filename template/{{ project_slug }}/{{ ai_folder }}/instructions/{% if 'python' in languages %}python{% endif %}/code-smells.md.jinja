# Python code smells

A taxonomy of Python anti-patterns this project actively refactors
against. Each entry: the smell, why it hurts, the cure.

When you spot one in existing code, fix it (or open an issue if the
blast radius is large). When you catch yourself writing one, stop.

## God Object

**Smell.** One class doing data validation, file I/O, business logic,
and presentation. Hundreds of lines. Many unrelated `self.x`.

**Why.** Violates single responsibility. Tests need elaborate setup.
Changes ripple unpredictably.

**Cure.** Extract each responsibility. Value objects own validation.
Repositories own persistence. Functions own pure transformations.
The God Object usually evaporates into 3–5 focused modules.

## Primitive Obsession

**Smell.** Domain concepts represented as raw `str`, `int`, `float`,
or `dict`. `def charge(user_id: str, amount: float, currency: str)`.

**Why.** Ambiguity — is `amount` cents or dollars? Validation has to
live at every call site. The type system can't help.

**Cure.** Value objects. `Money`, `EmailAddress`, `UserId`. See
`patterns.md`.

## Imprecise Types

**Smell.** `float` for money. Naïve `datetime` for "now". `str` for
JSON.

**Why.** `float` rounding errors compound across financial operations.
A timezone-naïve datetime silently uses local time. A JSON string
gets parsed at every layer.

**Cure.** `decimal.Decimal` or integer cents for money. Always
timezone-aware datetimes (`datetime.now(tz=UTC)`). Parse once at the
boundary, pass typed objects.

## Wrong Data Structure

**Smell.** Linear `list` lookups in hot paths. Repeated `if x in
some_list`. Building a dict from a list every iteration.

**Why.** O(n) where O(1) was available. Performance dies invisibly as
data grows.

**Cure.** `set` for membership checks. `dict` for keyed lookups.
`collections.Counter` for tallies. `collections.deque` for queues.

## Type Checking for Behaviour

**Smell.** A chain of `isinstance` checks dispatching different logic.

```python
def area(shape):
    if isinstance(shape, Circle):
        return math.pi * shape.r ** 2
    elif isinstance(shape, Square):
        return shape.side ** 2
    elif isinstance(shape, Triangle):
        ...
```

**Why.** Every new shape requires editing this function. Open-closed
principle is gone.

**Cure.** Polymorphism (method on the shape) or a dispatch dictionary
keyed on `type(shape)`. See `patterns.md` (Functional Strategy).

## Boolean Flag Parameters

**Smell.** `def process(x, *, fast=False, dry_run=False, retry=False)`
whose body is `if fast: ... else: ...`.

**Why.** Each flag doubles the combinatoric test surface. The function
now does several jobs.

**Cure.** Policy pattern (see `patterns.md`), or split into separate
functions with descriptive names.

## Deep Nesting / Arrow Code

**Smell.** Code that marches diagonally rightward across the screen
because of nested `if`/`for`/`with`.

**Why.** Cyclomatic complexity. Eye-tracking nightmare. Bugs hide in
the arrow.

**Cure.** Guard clauses with early returns. Extract inner loops to
named functions. Use `continue`/`return` to flatten.

## Wildcard Imports

**Smell.** `from module import *`.

**Why.** Pollutes the namespace. Tools can't trace where a name came
from. A new symbol added upstream can silently shadow yours.

**Cure.** Explicit imports. If the list is long, import the module
itself and use the qualified name.

## Catching and Ignoring Exceptions

**Smell.** `try: ... except Exception: pass`. `try: ... except: ...
log("oops")`.

**Why.** Real bugs vanish. The next maintainer cannot tell what
errors the code is *supposed* to recover from.

**Cure.** Catch the *specific* exception. Either handle it (with a
recovery path that's documented) or let it bubble. Bare `except:` is
banned — it also catches `KeyboardInterrupt`.

## Mutable Default Arguments

**Smell.** `def add_item(item, items=[]):`. Subsequent calls share the
same list. Mind-bending bugs.

**Why.** Python evaluates default arguments once at function
*definition* time. The list lives forever.

**Cure.** Use `None` and build inside.

```python
def add_item(item, items: list | None = None) -> list:
    items = list(items) if items is not None else []
    items.append(item)
    return items
```

## Unrelated Initialisations in `__init__`

**Smell.** `__init__` instantiates a database connection, an HTTP
client, and a metric registry — none of which the class itself created.

**Why.** Coupling to concrete implementations. Untestable without
patching.

**Cure.** Inject the dependencies in. The composition root wires them.
See `design.md` (Separate creation from use).

## Asymmetrical Code

**Smell.** A function that interleaves high-level business intent with
low-level string concatenation, file I/O, and HTTP retry logic.

**Why.** Forces the reader to context-switch between abstraction
levels mid-sentence.

**Cure.** Each function should operate at one level of abstraction.
Extract the low-level details to named helpers.

## Async Property

**Smell.** `@property` decorated on a method that awaits something.

**Why.** `@property` promises cheap, side-effect-free access. `await`
breaks both. The caller has no syntactic warning.

**Cure.** Make it an `async def` method. The `()` at the call site is
documentation.

## Hidden I/O

**Smell.** A method whose name suggests a calculation (`user.score()`),
which secretly hits the database.

**Why.** Loops that look O(n) become O(n) database round-trips.
Surprise latency.

**Cure.** Name the I/O. `user.fetch_score_from_db()`. Or, better: load
the data upfront in the use case and pass it in.

## Re-implementing the standard library

**Smell.** Hand-rolled `defaultdict`. A manual CSV parser. A bespoke
date-parser regex.

**Why.** The stdlib version is faster, correct, and one import away.

**Cure.** Search the stdlib first. `collections`, `itertools`,
`functools`, `pathlib`, `datetime`, `decimal`, `enum`, `dataclasses`,
`csv`, `json`, `tomllib`, `urllib.parse`.

## "Just in case" abstraction

**Smell.** An interface with one implementation, "in case we need to
swap it out later".

**Why.** YAGNI. The abstraction is rarely right when the second
implementation eventually arrives — and now you have one more layer to
read through every time.

**Cure.** Wait for the second concrete case. *Then* extract the
abstraction, informed by both.

## Working around the type checker

**Smell.** `# type: ignore` without a comment. `cast(Any, x)`.
`Any` in a public signature.

**Why.** Each one is a hole in the safety net. They accumulate.

**Cure.** Fix the underlying type. If you must suppress, add a comment
explaining what bothered mypy and why suppressing is safe.
