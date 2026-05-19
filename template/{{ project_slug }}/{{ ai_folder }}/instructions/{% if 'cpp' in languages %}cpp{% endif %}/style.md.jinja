# C/C++ style

External references: the
[C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
and the
[Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html).

## Formatting

- **`clang-format` with the project's `.clang-format`** — never
  hand-format. Run via `clang-format -i` or your editor on save.
  Suggested base: Google style with `IndentWidth: 4`, `ColumnLimit:
  100`, `DerivePointerAlignment: false`, `PointerAlignment: Left`.
- **`clang-tidy`** for static analysis. Suggested checks include
  `cppcoreguidelines-*`, `modernize-*`, `readability-*`, `performance-*`,
  `bugprone-*` (drop or refine specific checks per project as
  needed).

## Standard

- **C++20 minimum** (concepts, ranges, `<format>`, modules where
  supported). C++23 if your toolchain supports it well.
- Compile with `-std=c++20 -Wall -Wextra -Wpedantic -Werror`. Add
  `-Wshadow -Wconversion -Wnon-virtual-dtor` for stricter projects.
- For C code: **C17** minimum; same `-Werror` discipline.

## Naming (Core Guidelines NL.5, NL.10)

- `lower_snake_case` for functions, methods, variables, namespaces,
  file names.
- `UpperCamelCase` for types — classes, structs, enums, type aliases,
  concepts.
- `SCREAMING_SNAKE_CASE` for macros. **Macros are last resort.** Use
  `constexpr` constants and `inline` functions instead where possible.
- `kCamelCase` for compile-time constants and `enum class` enumerators
  (Google convention) *or* `SCREAMING_SNAKE_CASE` — pick one and be
  consistent within a project.
- Member variables: trailing underscore (`name_`). Don't use `m_`
  prefix in new code; the modern convention is the trailing
  underscore.
- Predicates: `is_*`, `has_*`, `can_*`. Return `bool`.

## Header hygiene

- **Header guards via `#pragma once`** (universally supported across
  modern compilers).
- **One class per header** where possible. The header's filename matches
  the class name in `snake_case`: `class OrderRepository` lives in
  `order_repository.hpp`.
- **Include what you use.** Don't lean on transitive includes — they
  break when the upstream header rearranges its includes.
- Order of includes:
  1. The corresponding `.hpp` of this `.cpp` (proves the header is
     self-contained).
  2. C / C++ standard library headers (`<vector>`, `<string>`).
  3. Third-party library headers (`<absl/...>`).
  4. Project headers.
  Separated by blank lines. clang-format with `IncludeIsMainRegex`
  can enforce this.
- Headers must be **self-contained** — they `#include` everything they
  reference and compile when included first.

## Modules (C++20)

If the toolchain supports modules well (e.g. recent MSVC, recent
Clang + libc++, GCC 15+), prefer modules over headers for new code.
The pattern is the same — one module per logical unit — but
compilation is faster and macro leakage stops.

For mixed legacy projects, keep modules for new code and convert
incrementally.

## RAII — the bedrock rule

Every resource you acquire is owned by an object whose destructor
releases it.

- **No raw `new`/`delete` outside of resource-managing classes.**
  Use `std::make_unique<T>(...)` and `std::make_shared<T>(...)`.
- **No raw owning pointers** in interfaces. Function signatures
  express ownership with the type:
  - `std::unique_ptr<T>` — sole owner; transfers on move.
  - `std::shared_ptr<T>` — shared owner; reference counted.
  - `T*` (raw) — *non-owning* observer, may be null.
  - `T&` — *non-owning* reference, never null.
  - `std::span<T>` / `std::string_view` — non-owning view.
- **No `delete[]` ever** — use `std::vector` / `std::array` /
  `std::unique_ptr<T[]>`.
- **No `delete` ever** in normal code — `unique_ptr` does it for you.
- **Files, locks, sockets, anything finalisable** — wrap in an RAII
  type that handles release in its destructor.

## Value semantics by default

- Prefer values to references-to-values where the type is small or
  cheap to move. Return by value; the compiler elides the copy (RVO
  / NRVO).
- Mark functions `const` aggressively (member functions, parameters,
  locals).
- `noexcept` on functions that genuinely can't throw — it unlocks
  optimisations and signals intent. Move constructors should be
  `noexcept` whenever possible.

## Smart pointer cheat-sheet

| Want | Use |
| --- | --- |
| Solo ownership | `std::unique_ptr<T>` (the default smart pointer). |
| Shared ownership | `std::shared_ptr<T>` (when it's genuinely shared). |
| Weak observer of a shared resource | `std::weak_ptr<T>`. |
| Non-owning, non-null | `T&`. |
| Non-owning, may be null | `T*` or `std::optional<T*>` for explicit nullability semantics. |
| Borrow of a sequence | `std::span<T>`. |
| Borrow of a string | `std::string_view`. |

## Error handling

- **Exceptions** are the project default for exceptional conditions
  (programmer-detected invariants, network/file errors). Catch
  specifically; don't `catch (...)` except at the outermost boundary
  with a logging-and-rethrow.
- For embedded or interface-restricted code paths where exceptions
  aren't acceptable: `std::expected<T, E>` (C++23) or `tl::expected`
  for C++20.
- **Never** use `errno` style return codes in new C++ code unless
  you're explicitly bridging to a C API.
- Validate at the boundary (`presentation/`); inner layers trust their
  inputs.

## `const`-correctness

- Member functions that don't modify state: `const`.
- Function parameters that are non-modifying references: `const T&`
  (or `T` by value if small).
- Local variables that don't change: `const`.
- `constexpr` where computation is genuinely compile-time.
- `consteval` (C++20) for functions that *must* be evaluated at
  compile time.

## Loose ends to avoid

- `using namespace std;` at file scope. Never. Inside function scope,
  rarely.
- `using namespace ...;` in headers. Never — it leaks into every
  includer.
- C-style casts (`(int)x`). Use `static_cast`, `dynamic_cast`,
  `const_cast`, `reinterpret_cast` — and prefer none of the last two
  unless absolutely necessary.
- C-style strings (`char*`) in interfaces. `std::string_view` or
  `std::string`.
- Manual array bounds. `std::array<T, N>` or `std::vector<T>`.
- `printf` in C++ code. `std::format` (C++20) or `std::println`
  (C++23).
- Hand-rolled `enum`s (unscoped) for new code. Use `enum class`.
- Default arguments in virtual functions. They don't behave the way
  most readers expect.

## Build hygiene

- Treat compiler warnings as errors. `-Werror` (or `/WX` on MSVC).
- Enable sanitisers in debug/CI: `-fsanitize=address,undefined` for
  most builds; `-fsanitize=thread` for concurrency.
- Run `clang-tidy` in CI. Fail the build on new findings.
