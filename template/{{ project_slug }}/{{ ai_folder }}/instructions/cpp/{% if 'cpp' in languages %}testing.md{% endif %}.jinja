# C/C++ testing

Pair with `../general/tdd.md` (the cycle and the four pillars) and
`../general/testing.md` (where each kind of test lives).

## Framework: GoogleTest or Catch2

Pick **one** and stick with it.

- **GoogleTest** — battle-tested, large ecosystem, integrates well
  with CMake and CTest. Use this for most C++ projects.
- **Catch2** — header-only (or single-include), expressive macros
  like `REQUIRE(x == y)` that print the actual values on failure.
  Use when you want zero build-system friction.

This file uses GoogleTest examples; Catch2 has equivalents
(`TEST_CASE`, `SECTION`, `REQUIRE`).

## Layout

```
src/
├── order.hpp
├── order.cpp
tests/
├── unit/
│   ├── CMakeLists.txt
│   └── order_test.cpp
├── integration/
│   └── orders_repo_test.cpp
└── e2e/
    └── checkout_test.cpp
```

CMake registers tests so `ctest` discovers them:

```cmake
# tests/unit/CMakeLists.txt
add_executable(unit_tests order_test.cpp ...)
target_link_libraries(unit_tests PRIVATE myproject GTest::gtest_main)
include(GoogleTest)
gtest_discover_tests(unit_tests)
```

## Running

| Action | Recipe | Underlying |
| --- | --- | --- |
| All tests | `just cpp-test` | `ctest --test-dir build --output-on-failure` |
| One test by regex | — | `ctest --test-dir build -R 'pattern' -V` |
| Verbose | — | `ctest --test-dir build --verbose` |
| With sanitisers | — | configure with the `asan` preset, then `ctest --preset asan` |

For TDD loops, build and test together:

```sh
cmake --build --preset default && ctest --preset default
```

Some editors (CLion, VS Code with CMake Tools) re-run on file save.

## Anatomy of a test

```cpp
#include <gtest/gtest.h>
#include "order.hpp"

TEST(OrderRefund, MarksAsRefundedWhenPaid) {
    // Arrange
    auto order = Order::placed(items(), money(100, "USD"));
    order.mark_paid();

    // Act
    const auto result = order.refund("customer requested");

    // Assert
    ASSERT_TRUE(result.has_value());
    EXPECT_EQ(order.status(), OrderStatus::Refunded);
    EXPECT_NE(order.refunded_at(), std::nullopt);
}
```

- AAA layout; blank lines between phases.
- One state-changing call in Act.
- One logical outcome in Assert; multiple `EXPECT_*`s checking facets
  of it are fine.
- `ASSERT_*` aborts the test on failure (use when later asserts would
  segfault); `EXPECT_*` continues (default choice).

## Naming

`TEST(SuiteName, TestName)` where:

- `SuiteName` = the unit under test (`OrderRefund`, `MoneyParser`).
- `TestName` = `<DoesWhat>When<Condition>` in PascalCase, or the
  full sentence form.

Examples:

- `TEST(OrderRefund, RaisesWhenUnpaid)`
- `TEST(EmailNormalise, LowercasesDomain)`
- `TEST(MoneyAdd, FailsAcrossCurrencies)`

## Test fixtures

Use `TEST_F(Fixture, Name)` for shared setup:

```cpp
class OrderRefundFixture : public ::testing::Test {
protected:
    void SetUp() override {
        order_ = Order::placed(items(), money(100, "USD"));
        order_.mark_paid();
    }
    Order order_;
};

TEST_F(OrderRefundFixture, MarksAsRefunded) {
    order_.refund("...");
    EXPECT_EQ(order_.status(), OrderStatus::Refunded);
}
```

Use sparingly — a factory function (`a_paid_order()`) is usually
clearer than a fixture class.

## Parametrize

`TEST_P` for value-parameterised tests:

```cpp
struct MoneyValidationCase {
    std::int64_t amount;
    std::string  currency;
    bool         expect_valid;
};

class MoneyValidation : public ::testing::TestWithParam<MoneyValidationCase> {};

TEST_P(MoneyValidation, Validates) {
    const auto& tc = GetParam();
    auto r = Money::create(tc.amount, tc.currency);
    EXPECT_EQ(r.has_value(), tc.expect_valid);
}

INSTANTIATE_TEST_SUITE_P(MoneyCases, MoneyValidation, ::testing::Values(
    MoneyValidationCase{   0, "USD", true  },
    MoneyValidationCase{  10, "USD", true  },
    MoneyValidationCase{  -1, "USD", false },
    MoneyValidationCase{  10, "usd", false },
    MoneyValidationCase{  10, "XX",  false }
));
```

## Property-based testing

Use `rapidcheck` (integrates with GoogleTest via `rapidcheck-gtest`):

```cpp
RC_GTEST_PROP(Money, AdditionIsCommutative,
              (std::int64_t a, std::int64_t b)) {
    RC_PRE(a >= 0 && b >= 0 && a < 1'000'000 && b < 1'000'000);
    auto m1 = Money::usd_cents(a);
    auto m2 = Money::usd_cents(b);
    RC_ASSERT(m1 + m2 == m2 + m1);
}
```

For Catch2 + property-based, use the `rapidcheck-catch` integration.

## Sanitisers in test runs

CI must run the test suite with:

- **AddressSanitizer (ASan)** + **UBSan** — catches memory and UB
  bugs that don't otherwise manifest.
- **ThreadSanitizer (TSan)** — separate run for threading-heavy code.

Configure via the `asan` / `tsan` preset (see `tooling.md`). A
green ASan/UBSan/TSan run is non-negotiable before merging.

## Mocking — classical school, sparingly

Same rule as the rest of the codebase: **mock only out-of-process
dependencies**.

- For in-process collaborators: parameterise on a concept or
  pure-abstract interface, and pass a hand-written in-memory
  implementation in tests.
- For DB / HTTP / clock / filesystem: a fake implementation or
  GoogleMock.

```cpp
class InMemoryOrderRepository : public OrderRepository {
public:
    std::optional<Order> find(OrderId id) const override {
        auto it = orders_.find(id);
        return it == orders_.end() ? std::nullopt : std::make_optional(it->second);
    }
    void save(const Order& o) override { orders_[o.id()] = o; }
private:
    mutable std::unordered_map<OrderId, Order> orders_;
};
```

GoogleMock is available for the genuinely-needed mocks; lean on real
fakes first.

## What to test

| Layer | Coverage style |
| --- | --- |
| `domain` | High. Every invariant, edge case, error. |
| `application` | Integration tests against in-memory adapters. |
| `infrastructure` | Integration tests against a real instance via a container or local install. |
| `presentation` | Small set of e2e tests through the public CLI/HTTP/hardware boundary. |

## What NOT to test

- Trivial accessors / getters with no logic.
- Third-party library internals — test *your usage*.
- Implementation details that would force the test to change every
  refactor (private functions, internal struct fields, hashing
  internals).

## TDD with C++

The full ritual (mirrors `../general/tdd.md`):

1. `ctest -R 'refund_unpaid' -V` — red.
2. Write the simplest implementation that turns it green.
3. `cmake --build --preset default && ctest --preset default` —
   green everywhere.
4. Refactor with the suite as the safety net.
5. Commit.

Tools like [`watchexec`](https://github.com/watchexec/watchexec) can
rebuild and test on every save:

```sh
watchexec -e cpp,hpp -- 'cmake --build --preset default && ctest --preset default'
```
