# Pythonic patterns

This file is a recipe book. Pair it with `design.md` (the principles)
and `code-smells.md` (what each pattern fixes).

Python has first-class functions and structural typing, so most of the
Gang-of-Four patterns get a much lighter implementation here. Default to
the functional version.

## Value object

A frozen dataclass that validates its invariants in `__post_init__`.
Once you hold one, downstream code can trust it.

```python
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("amount must be non-negative")
        if len(self.currency) != 3 or not self.currency.isupper():
            raise ValueError("currency must be an ISO 4217 code")

    def __add__(self, other: Money) -> Money:
        if self.currency != other.currency:
            raise ValueError("cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)
```

Use one wherever you'd otherwise pass a primitive that has a constraint:
money, percentages, email addresses, ISO codes, timestamps with
timezone semantics, anything domain-meaningful.

## Functional Strategy (dispatch dictionary)

Instead of an abstract base class with N subclasses, use a `dict` mapping
keys to functions.

```python
from typing import Callable

Renderer = Callable[[Invoice], str]

RENDERERS: dict[str, Renderer] = {
    "pdf": render_pdf,
    "html": render_html,
    "plaintext": render_plaintext,
}

def render(invoice: Invoice, fmt: str) -> str:
    try:
        return RENDERERS[fmt](invoice)
    except KeyError as exc:
        raise UnsupportedFormat(fmt) from exc
```

If a strategy needs parameters, bind them with `functools.partial` or
return a closure.

## Policy pattern (kill the boolean flag)

When a function grows boolean parameters that flip its behaviour, split
the behaviour into composable policies.

```python
# Avoid:
def process_order(order, apply_discount=False, is_vip=False, ship_express=False):
    if apply_discount: ...
    if is_vip: ...
    if ship_express: ...
    return order

# Prefer:
from typing import Callable
OrderPolicy = Callable[[Order], Order]

def apply_vip_discount(order: Order) -> Order: ...
def express_shipping(order: Order) -> Order: ...

def process_order(order: Order, policies: list[OrderPolicy]) -> Order:
    for policy in policies:
        order = policy(order)
    return order

# Caller composes:
process_order(order, [apply_vip_discount, express_shipping])
```

Result: no flag combinatorics, no `if/elif` cascades, each policy is
trivially unit-testable, the set of policies is extensible.

## Context object (kill parameter bloat)

When a function honestly needs >4 arguments that travel together, group
them into a dataclass.

```python
@dataclass(frozen=True)
class ReportContext:
    period: DateRange
    currency: str
    tenant: TenantId
    locale: str
    include_drafts: bool

def build_report(ctx: ReportContext) -> Report: ...
```

Pair this with `Protocol`s on the consumer side so individual helpers
depend only on the fields they actually use:

```python
class PeriodProvider(Protocol):
    @property
    def period(self) -> DateRange: ...

def summarise(period_source: PeriodProvider) -> Summary: ...
```

## Unit of Work as a context manager

Wrap database transactions with `with` so commit/rollback is automatic
and impossible to forget.

```python
class UnitOfWork(Protocol):
    orders: OrderRepository
    def __enter__(self) -> UnitOfWork: ...
    def __exit__(self, exc_type, exc, tb) -> None: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...

# Use case:
def place_order(cmd: PlaceOrder, uow: UnitOfWork) -> OrderId:
    with uow:
        order = Order.from_command(cmd)
        uow.orders.add(order)
        uow.commit()
    return order.id
```

The use case is now linear, error-safe, and DB-agnostic.

## Composition Root

A single function (or module) that wires concrete implementations to
their abstractions. Everything else takes its dependencies as
arguments.

```python
# src/presentation/main.py
def build_app() -> FastAPI:
    db = SqlAlchemyEngine.from_env()
    uow_factory = lambda: SqlAlchemyUnitOfWork(db)
    place_order_use_case = PlaceOrderUseCase(uow_factory)

    app = FastAPI()
    register_order_routes(app, place_order_use_case)
    return app
```

No other module reads environment variables or instantiates database
clients. There is exactly one place to look when wiring changes.

## Result objects (errors-as-values)

When you want to avoid raising exceptions across layer boundaries (the
domain shouldn't raise an HTTP-flavoured exception):

```python
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")
E = TypeVar("E")

@dataclass(frozen=True)
class Ok(Generic[T]):
    value: T

@dataclass(frozen=True)
class Err(Generic[E]):
    error: E

Result = Ok[T] | Err[E]
```

Or use the [`returns`](https://github.com/dry-python/returns) library if
you want the full monadic toolkit. The point: domain functions return
their failures explicitly; the application layer maps them to HTTP /
CLI exit codes.

## Pub/sub via a dict of handlers

For in-process events, prefer a dictionary of handlers over a heavyweight
event-bus class.

```python
from collections import defaultdict
from typing import Callable

Handler = Callable[[object], None]
HANDLERS: dict[type, list[Handler]] = defaultdict(list)

def subscribe(event_type: type, handler: Handler) -> None:
    HANDLERS[event_type].append(handler)

def publish(event: object) -> None:
    for handler in HANDLERS[type(event)]:
        handler(event)
```

## When to reach for the textbook OOP version

There are cases where the classic ABC + concrete-classes version is the
right call: when you need shared state, when you need a default method
implementation, when you're publishing a framework / library and want
to enforce the interface at definition time. Use your judgement; the
default is the lightweight version.
