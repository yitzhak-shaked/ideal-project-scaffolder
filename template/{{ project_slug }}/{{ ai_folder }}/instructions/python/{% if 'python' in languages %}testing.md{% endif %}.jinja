# Python testing

Pair this with `../general/tdd.md` (the cycle and the four pillars) and
`../general/testing.md` (where each kind of test lives).

## Runner: pytest, always via uv

```sh
uv run pytest                              # everything
uv run pytest tests/unit/                  # one tree
uv run pytest -k "refund and not slow"     # keyword filter
uv run pytest -x                           # stop on first failure
uv run pytest --lf                         # rerun last failures
uv run pytest --cov=src --cov-report=term-missing
```

## Test layout

The repository-wide layout is in `../general/testing.md`. For Python
specifically:

```
tests/
├── conftest.py        # session-wide fixtures
├── unit/              # fast, pure, no I/O
├── integration/       # cross-module + real adapters (DB in container, etc.)
├── e2e/               # through the public boundary (HTTP, CLI)
└── performance/       # benchmarks (pytest-benchmark or similar)
```

`conftest.py` files cascade — a `conftest.py` inside `tests/integration/`
provides fixtures only to that subtree.

## Anatomy of a test

```python
def test_order_refund_when_paid_marks_as_refunded():
    # Arrange
    order = a_paid_order(total=Money(Decimal("100"), "USD"))

    # Act
    order.refund(reason="customer requested")

    # Assert
    assert order.status is OrderStatus.REFUNDED
    assert order.refunded_at is not None
```

- Three phases, blank-line-separated: **Arrange / Act / Assert**.
- *One* state-changing call in the Act block. If you need two, that's
  two tests.
- *One* logical outcome in the Assert block. Multiple asserts that
  verify facets of the same outcome are fine.

## Naming

A test name is a sentence:

```
test_<unit>_<condition>_<expected>
```

Examples:

- `test_email_normalisation_lowercases_the_domain`
- `test_refund_when_order_is_unpaid_raises_invalid_state`
- `test_paginate_returns_empty_page_when_offset_past_end`

If the name doesn't fit, the test is doing too much. Split it.

## Fixtures

Use `@pytest.fixture` for shared arrange-phase setup. Keep them small,
named after the *thing* they produce, not the *action*:

```python
@pytest.fixture
def paid_order() -> Order:
    order = Order.placed(items=[an_item()], total=Money(Decimal("50"), "USD"))
    order.mark_paid()
    return order

def test_refunded_after_payment(paid_order: Order):
    paid_order.refund()
    assert paid_order.status is OrderStatus.REFUNDED
```

- Prefer **factory functions** (`a_paid_order(...)`) for test data that
  needs variations. Fixtures for stateful setup (DB session, temp dir).
- **Scope** judiciously: `function` (default) for isolation, `module`
  or `session` for expensive setup.
- Yield fixtures for setup + teardown:

  ```python
  @pytest.fixture
  def temp_repo():
      repo = InMemoryOrderRepository()
      yield repo
      repo.clear()
  ```

## Parametrize for input sweeps

```python
@pytest.mark.parametrize("amount,currency,expect_valid", [
    (Decimal("0"),  "USD", True),
    (Decimal("10"), "USD", True),
    (Decimal("-1"), "USD", False),
    (Decimal("10"), "usd", False),
    (Decimal("10"), "XX",  False),
])
def test_money_validation(amount, currency, expect_valid):
    if expect_valid:
        Money(amount, currency)
    else:
        with pytest.raises(ValueError):
            Money(amount, currency)
```

Parametrize is the easy lever before you reach for `hypothesis`.

## Property-based testing with Hypothesis

When you can describe the *property* of the answer rather than enumerate
inputs:

```python
from hypothesis import given, strategies as st

@given(st.decimals(min_value=0, max_value=10**6, places=2))
def test_money_addition_is_commutative(amount):
    a = Money(amount, "USD")
    b = Money(Decimal("1"), "USD")
    assert a + b == b + a
```

Hypothesis hunts edge cases (zero, max int, weird Unicode) you would
never have thought of. Use it on value objects, parsers, and pure
functions in `domain/`.

Install via: `uv add --dev hypothesis`.

## Mutation testing (when you want to grade the tests themselves)

Coverage tells you which lines ran. Mutation testing tells you whether
the assertions actually caught anything. `mutmut` mutates a `>` to a
`<`, `True` to `False`, etc., then reruns your tests. If the suite still
passes, the test is asleep.

```sh
uv add --dev mutmut
uv run mutmut run --paths-to-mutate src/domain/
uv run mutmut results
```

Don't run this on every commit — it's slow. Run it occasionally on the
modules you most care about.

## Mocking — classical school, sparingly

This codebase follows the **classical** school of unit testing (see
`../general/tdd.md`):

- **Mock only out-of-process dependencies** — DBs, HTTP, queues, the
  filesystem, the clock.
- For in-process collaborators, use the real implementation, or a
  hand-written **fake** (an in-memory repository implementing the same
  `Protocol`).
- If a test needs 10+ lines of `unittest.mock.patch`, the code is over-
  coupled. Refactor with dependency injection (see `design.md`).

```python
# Good: in-memory fake implementing the repository protocol
class InMemoryOrderRepository:
    def __init__(self) -> None:
        self._orders: dict[OrderId, Order] = {}
    def get(self, id: OrderId) -> Order | None:
        return self._orders.get(id)
    def add(self, order: Order) -> None:
        self._orders[order.id] = order

def test_place_order_persists_it():
    repo = InMemoryOrderRepository()
    use_case = PlaceOrderUseCase(repo)
    cmd = a_place_order_command()

    use_case.execute(cmd)

    assert repo.get(cmd.order_id) is not None
```

## Test what?

| Layer | Coverage style |
| --- | --- |
| `domain/` | High. Every invariant, every edge case, every error path. Pure functions love unit tests. |
| `application/` (use cases) | Integration tests against real / fake adapters. Prefer fakes over mocks. |
| `infrastructure/` (adapters) | Integration tests that hit a real instance of the external system (in a container). |
| `presentation/` | Small number of e2e tests proving wiring is correct. Don't recover the full behaviour set up here — rely on lower layers. |

## What NOT to test

- Trivial getters/setters with no logic.
- Pydantic model instantiation (test the *validation behaviour you
  care about*, not that the field exists).
- Third-party library internals.
- Implementation details that would force the test to change every
  refactor.

## Useful pytest plugins

- `pytest-cov` — coverage.
- `pytest-xdist` — parallel runs (`uv run pytest -n auto`).
- `pytest-randomly` — randomise test order, surface order-dependence
  bugs.
- `pytest-timeout` — kill tests that hang.
- `pytest-benchmark` — performance regression tests.
- `pytest-asyncio` — for `async def` tests.

Add via `uv add --dev <plugin>`.

## TDD with pytest in this repo

The full ritual (mirrors `../general/tdd.md`):

1. `uv run pytest tests/unit/test_thing.py::test_new_behaviour` — red.
2. Write the simplest implementation that turns it green.
3. `uv run pytest` (whole suite) — green everywhere.
4. Refactor with the test as the safety net.
5. Commit. Move to the next test on the list.

Use `uv run pytest --lf -x` to iterate — runs only the last-failed
tests and stops on the first failure.
