# C/C++ code smells

Anti-patterns this project refactors against. Each entry: the smell,
why it hurts, the cure.

## Raw `new` / `delete`

**Smell.** `auto* x = new Foo(...);` anywhere outside the body of a
resource-managing class.

**Why.** Leaks on early return / exception. Manual lifetime
management always loses to a destructor.

**Cure.** `std::make_unique<Foo>(...)`. If shared, `std::make_shared`.
Never `delete`.

## Raw owning pointers in interfaces

**Smell.** `Foo* create_foo();` where the caller is supposed to
`delete` the result.

**Why.** The interface doesn't say "you own this". Half the callers
forget.

**Cure.** Return `std::unique_ptr<Foo>`. Ownership is in the type.

## Naked `using namespace std;` in headers

**Smell.** `using namespace std;` at file scope, especially in a
header.

**Why.** Pollutes every translation unit that includes the header.
Future renames collide silently.

**Cure.** Qualify (`std::`). Inside function scope, narrow `using`
declarations are OK.

## Old-style enums

**Smell.** `enum Status { PLACED, PAID, SHIPPED };` (unscoped).

**Why.** Implicitly converts to int. Names leak into the enclosing
scope. Mixing enums is silent.

**Cure.** `enum class Status { Placed, Paid, Shipped };`. Explicit
scope; no implicit conversion.

## C-style casts

**Smell.** `(int)x`.

**Why.** Could be any of `static_cast`, `const_cast`, `reinterpret_cast`,
or a combination. Reviewers can't tell which.

**Cure.** `static_cast<int>(x)` (or `narrow_cast` for explicit
narrowing). Use the narrowest cast that compiles.

## Primitive obsession

**Smell.** Functions taking `std::uint64_t`, `double`, `const
std::string&` for domain concepts (user IDs, money amounts, emails).

**Why.** Argument swap → silent bug. Validation has to be at every
call site.

**Cure.** Strong types (`patterns.md`). `struct UserId { ... };`
costs nothing at runtime.

## Stringly-typed status

**Smell.** `if (order.status == "paid")` — string comparison
everywhere.

**Why.** Typos compile. Renaming a status is a grep-and-pray.

**Cure.** `enum class Status` or `std::variant` for status-with-data.

## God class

**Smell.** A class with 40 member functions doing data validation,
file I/O, business logic, and presentation.

**Why.** Violates SRP. Tests need elaborate fixtures. Every change
ripples.

**Cure.** Extract responsibilities by name from the DDD vocabulary:
`OrderRepository`, `OrderValidator`, `OrderRenderer`. See
`general/ddd.md`.

## Manual lock/unlock

**Smell.** `mutex.lock(); ... mutex.unlock();`.

**Why.** Early return / exception between them leaves the mutex
locked.

**Cure.** `std::lock_guard<std::mutex> g(mutex);` or `std::scoped_lock
g(m1, m2);`.

## Hand-rolled retry / try-finally for cleanup

**Smell.** `try { ... } catch (...) { release(x); throw; } release(x);`.

**Why.** Reinvents RAII. Easy to get wrong.

**Cure.** Wrap `x`'s release in an RAII type's destructor. The
language already does this for you.

## `printf` / `iostream` mixed with `std::format`

**Smell.** Three formatting styles in the same codebase.

**Why.** Inconsistent output, harder to maintain, format-string
vulnerabilities (`printf`).

**Cure.** `std::format` (C++20) and `std::println` (C++23)
everywhere. Drop `iostream` operators for formatted output.

## Macros for constants / functions

**Smell.** `#define PI 3.14`, `#define MAX(a, b) ((a) > (b) ? (a) : (b))`.

**Why.** No type safety. Double-evaluation of arguments. No namespace
respect. Bizarre error messages.

**Cure.** `constexpr double pi = 3.14;` and an inline function or
template. Macros are last resort.

## Catching all exceptions

**Smell.** `try { ... } catch (...) { /* log */ }` or
`catch (const std::exception&) { /* swallow */ }`.

**Why.** Hides bugs. The caller sees half-applied state.

**Cure.** Catch the *specific* exception type. Either handle it (with
a recovery path) or let it propagate.

## Long parameter lists

**Smell.** A function with 8 parameters.

**Why.** Unreadable at the call site. Easy to mix up.

**Cure.** Group into a struct that's also a domain concept. Or split
the function (each subset of params signals a different responsibility).

## Default arguments on virtual functions

**Smell.**

```cpp
class Base { public: virtual void f(int x = 10) = 0; };
class Derived : public Base { public: void f(int x = 20) override; };
```

**Why.** The default comes from the *static* type at the call site,
the implementation from the *dynamic* type. Surprising.

**Cure.** No default arguments on virtual functions. Provide overloads
or `optional` parameters.

## Slicing

**Smell.** `Base b = derived_instance;`.

**Why.** Only the base part is copied; the derived state is lost.

**Cure.** Pass by reference or pointer (`const Base&`,
`std::unique_ptr<Base>`). Mark base classes `Base(const Base&) = delete`
to forbid copy.

## Returning references to locals

**Smell.** `std::string& foo() { std::string s = "..."; return s; }`.

**Why.** Dangling reference. Use is undefined behaviour.

**Cure.** Return by value. RVO/NRVO elides the copy.

## Unused `[[nodiscard]]`

**Smell.** A function returning `std::expected<T, E>` (or any
must-check value) that callers ignore.

**Why.** Errors silently dropped.

**Cure.** Mark the function `[[nodiscard]]`. Compiler will warn at
unused call sites.

## `auto` everywhere, even when type clarifies

**Smell.** `auto x = something_that_might_be_a_string_or_a_view();`.

**Why.** Reader can't tell. Slight type drift goes unnoticed.

**Cure.** `auto` for obvious or unutterable types (iterators, lambdas);
named type when it makes the local less ambiguous.

## Premature `final` / `override` confusion

**Smell.** Forgetting `override` on a method that's supposed to
override a virtual.

**Why.** Silently creates a new method when the base signature
changes. Tests pass; runtime calls the wrong thing.

**Cure.** Always `override` (or `final` if you mean to forbid further
override). The compiler then enforces the signature.
