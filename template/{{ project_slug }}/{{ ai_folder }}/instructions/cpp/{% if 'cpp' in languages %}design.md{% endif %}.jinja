# C/C++ design philosophy

The C++ design heuristics this project follows. The single most useful
reference is the
[C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
(Stroustrup & Sutter). When in doubt, look up the relevant rule there
and follow it.

## RAII is the foundation

Every resource — memory, file handle, socket, lock, GPU buffer,
database connection — is **owned by an object** whose destructor
releases it. The compiler runs the destructor; you don't.

- New allocations: `std::make_unique<T>(...)`. No raw `new`.
- Shared ownership (rarely needed): `std::make_shared<T>(...)`.
- Files: `std::ofstream` / `std::ifstream` (RAII out of the box).
- Locks: `std::lock_guard<std::mutex>` / `std::scoped_lock`. Never
  manual `lock()` / `unlock()`.
- Custom resources: write a small RAII wrapper. The destructor is the
  release. The copy/move semantics encode the ownership rules (often:
  delete copy, default move).

If you're writing `try` / `catch` to release a resource, you want an
RAII type.

## Value semantics where possible

A C++ value behaves like an `int`: copying makes an independent copy,
moving transfers contents. Reach for value semantics first; reach for
references/pointers when you have a specific reason.

- Return by value. The compiler elides the copy.
- Pass small / cheap-to-move values by value (`std::string`,
  `std::vector`, your own value-like types).
- Pass larger non-modifying inputs by `const T&`.
- Pass output parameters as return values (or as `T&` if it's the
  natural API).

## Express ownership in the type

Function signatures should make ownership obvious:

| Signature | Means |
| --- | --- |
| `std::unique_ptr<T>` (returned) | "I'm giving you sole ownership." |
| `std::unique_ptr<T>` (param) | "Give me sole ownership." (Use sparingly — usually `T&&` or by value is enough.) |
| `std::shared_ptr<T>` | "We share ownership." |
| `T*` | Non-owning observer; may be null. |
| `T&` | Non-owning reference; never null. |
| `std::span<T>` | Non-owning view of a contiguous range. |
| `std::string_view` | Non-owning view of a string. |

Raw pointers in interfaces are *never* owning in this codebase. If
you receive a `T*`, you don't free it.

## Make invalid states unrepresentable

Use the type system to eliminate edge cases.

- **`enum class`** instead of `int` flags or naked strings.
- **`std::optional<T>`** for "value may be absent". Don't use sentinel
  values (`-1`, `nullptr`, empty string).
- **`std::variant<T, U, V>`** for sum types — `std::visit` with an
  exhaustive overload set.
- **`std::expected<T, E>`** (C++23) or `tl::expected` (C++20) for
  "may succeed or fail with these specific errors".
- **Strong typedefs / strong types** — wrap primitives that mean a
  specific thing.

```cpp
struct UserId  { std::uint64_t value; auto operator<=>(const UserId&) const = default; };
struct OrderId { std::uint64_t value; auto operator<=>(const OrderId&) const = default; };

void charge(UserId user, OrderId order);
// charge(order_id, user_id);  // compile error — types mismatch
```

For value objects with invariants (Money, Email, Percentage), validate
in the constructor; once constructed, callers don't re-check.

## Composition over inheritance

- Inheritance is a tool, not a default. Most "use inheritance" instincts
  are actually composition + an interface.
- **Public inheritance = is-a, only**. Anything else is the wrong tool.
- **No deep hierarchies.** Two levels is plenty; three is a smell.
- **No multiple inheritance** of state-bearing classes. Inheriting
  multiple interfaces (pure abstract classes) is fine.
- Virtual destructor on any class meant to be used polymorphically.
  Otherwise mark it `final` to forbid inheritance.

For polymorphism, prefer:

1. **`std::variant` + `std::visit`** — closed set, no allocations,
   compile-time exhaustive.
2. **Concepts** (C++20) — open set, static dispatch, no virtual cost.
3. **`std::function` / type erasure** — open set, dynamic dispatch,
   one heap allocation.
4. **Classic virtual hierarchy** — open set, simple, vtable cost,
   familiar.

Pick the lightest one that matches the problem.

## Concepts (C++20)

Concepts replace SFINAE and ad-hoc template tricks. They make
template parameters self-documenting and error messages readable.

```cpp
template <typename T>
concept Repository = requires(T t, OrderId id, Order o) {
    { t.find(id) } -> std::convertible_to<std::optional<Order>>;
    { t.save(o) } -> std::same_as<void>;
};

template <Repository R>
class PlaceOrderUseCase {
    R& repo_;
public:
    explicit PlaceOrderUseCase(R& repo) : repo_(repo) {}
    OrderId execute(const PlaceOrderCommand& cmd);
};
```

The compiler will tell the caller what's missing in plain English
instead of dumping a template instantiation trace.

## Const-correctness is design

- Member functions that don't modify state: `const`.
- Reference parameters that aren't modified: `const T&`.
- Locals that don't change: `const`.
- `constexpr` where the value is genuinely compile-time.
- `noexcept` on functions that can't throw — both for optimisation
  and for honest documentation.

## Clean Architecture mapping

The DDD layering from `general/architecture.md`:

| Layer | C++ expression |
| --- | --- |
| `domain` | Value types and entities. Pure header + source. `#include` only the standard library. Interfaces as **pure abstract classes** or **concepts** that the domain *needs from the world*. |
| `application` | Use case classes. Templates / generics on `Repository` etc. |
| `infrastructure` | Concrete `class SqlOrderRepository : public OrderRepository` (or satisfying the concept). Imports the DB driver. |
| `presentation` | `main.cpp`, the HTTP framework, CLI parser. Wires concrete types into the application. |

The DI is performed at the entry point. `main()` is the composition
root.

## When to PIMPL

The **Pointer to IMPLementation** idiom (PIMPL) hides implementation
details behind an opaque pointer.

Use when:
- You need a stable ABI across versions.
- The class's implementation needs a heavy header (e.g. database client)
  that you don't want to leak to consumers.
- Build times suffer because of header dependencies.

Don't use as the default — it adds a heap allocation and an
indirection. See `patterns.md`.

## Concurrency

- **Default to no shared mutable state.** Prefer message-passing
  (`std::jthread` + queue) over shared variables.
- When you must share, use `std::mutex` + `std::lock_guard`
  / `std::scoped_lock`. Never `lock()` / `unlock()` by hand.
- `std::atomic<T>` for genuinely atomic ops (counters, flags). Don't
  build complex protocols on raw atomics.
- TSan in CI for any code that uses threads.

## Performance hygiene (not premature)

- Don't allocate in hot loops. Reserve / reuse.
- Move semantics over copies for big objects (`std::move`).
- `std::span` and `std::string_view` for non-owning ranges — accept
  contiguous data without owning it.
- Iterators are usually preferable to indices.
- Profile before optimising. The first surprise is almost always *not*
  where you expected.
