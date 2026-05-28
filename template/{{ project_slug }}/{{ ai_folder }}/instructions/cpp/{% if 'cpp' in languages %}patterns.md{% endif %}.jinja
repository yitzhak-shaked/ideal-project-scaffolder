# C/C++ patterns

Recipes. Pair with `design.md` (the principles) and `code-smells.md`
(what each pattern fixes).

## Strong type (newtype)

Wrap a primitive in a `struct` that's a different type.

```cpp
struct UserId  { std::uint64_t value; auto operator<=>(const UserId&) const = default; };
struct OrderId { std::uint64_t value; auto operator<=>(const OrderId&) const = default; };

void charge(UserId user, OrderId order);
```

Zero runtime cost. Eliminates argument-swap bugs and makes overload
resolution helpful.

For value objects with invariants, validate at construction:

```cpp
class Email {
    std::string value_;
    explicit Email(std::string v) : value_(std::move(v)) {}
public:
    static std::expected<Email, std::string> parse(std::string s);
    std::string_view view() const noexcept { return value_; }
};
```

Constructor is private; only `parse` (which validates) builds one.

## RAII guards

```cpp
class TransactionGuard {
    Database* db_;
    bool committed_ = false;
public:
    explicit TransactionGuard(Database& db) : db_(&db) { db_->begin(); }
    ~TransactionGuard() { if (!committed_) db_->rollback(); }
    void commit() { db_->commit(); committed_ = true; }

    TransactionGuard(const TransactionGuard&)            = delete;
    TransactionGuard& operator=(const TransactionGuard&) = delete;
};
```

Use for: locks, transactions, files, temporary buffers,
instrumentation timers. The pattern is "destructor releases".

## `std::variant` + `std::visit` for closed sums

```cpp
struct Placed   { TimePoint at; };
struct Paid     { TimePoint at; Money amount; };
struct Shipped  { TimePoint at; TrackingId tracking; };
struct Refunded { TimePoint at; std::string reason; };

using OrderEvent = std::variant<Placed, Paid, Shipped, Refunded>;

std::string describe(const OrderEvent& e) {
    return std::visit([]<typename T>(const T& v) -> std::string {
        if constexpr (std::is_same_v<T, Placed>)   return "placed";
        else if constexpr (std::is_same_v<T, Paid>) return "paid";
        else if constexpr (std::is_same_v<T, Shipped>)  return "shipped";
        else if constexpr (std::is_same_v<T, Refunded>) return "refunded";
    }, e);
}
```

Adding a fifth variant fails to compile here — exactly what you want.

## Concepts-based interfaces

Instead of a virtual base class:

```cpp
template <typename T>
concept OrderRepository = requires(T t, OrderId id, Order o) {
    { t.find(id) } -> std::same_as<std::optional<Order>>;
    { t.save(o)  } -> std::same_as<void>;
};

template <OrderRepository R>
OrderId place_order(const PlaceOrderCommand& cmd, R& repo);
```

Static dispatch. No vtable. Caller types are checked at compile time
with clear error messages.

Use a virtual interface instead when you genuinely need runtime
polymorphism (e.g. plugin systems).

## PIMPL

Hide heavy implementation behind an opaque pointer.

```cpp
// foo.hpp
class Foo {
public:
    Foo();
    ~Foo();                              // out-of-line so Impl is complete
    Foo(Foo&&) noexcept;
    Foo& operator=(Foo&&) noexcept;

    void do_thing();
private:
    struct Impl;
    std::unique_ptr<Impl> p_;
};

// foo.cpp
struct Foo::Impl { /* heavy guts */ };
Foo::Foo()                          : p_(std::make_unique<Impl>()) {}
Foo::~Foo()                         = default;
Foo::Foo(Foo&&) noexcept            = default;
Foo& Foo::operator=(Foo&&) noexcept = default;
void Foo::do_thing()                { p_->do_thing(); }
```

Use sparingly — it adds an allocation and an indirection. Use when
you need ABI stability or your header pulls in heavy dependencies.

## NVI — Non-Virtual Interface

Public functions are non-virtual; they call private virtual hooks.
Gives a stable public surface while subclasses customise behaviour.

```cpp
class Logger {
public:
    void log(std::string_view msg) {
        const auto prefixed = "[" + timestamp() + "] " + std::string(msg);
        do_log(prefixed);
    }
    virtual ~Logger() = default;
private:
    virtual void do_log(std::string_view msg) = 0;
};
```

The base class controls cross-cutting concerns (the timestamp); the
subclass implements the I/O.

## Range-based + algorithms

```cpp
auto active_users(std::span<const User> users) {
    return users | std::views::filter([](const User& u) { return u.is_active; })
                 | std::views::transform([](const User& u) { return u.id; });
}
```

C++20 ranges replace most hand-rolled loops. They're lazy, composable,
and unambiguous about side effects.

## Composition root

```cpp
int main() {
    Config cfg = Config::from_env();
    SqlOrderRepository repo(cfg.database_url);           // concrete
    auto place_order = PlaceOrderUseCase{repo};          // generic over Repository
    return run_http_server(cfg.port, place_order);
}
```

`main()` is the only place that knows the concrete types.

## Builder for many parameters

```cpp
class HttpClientBuilder {
public:
    HttpClientBuilder& with_base_url(URL u)   { url_ = std::move(u); return *this; }
    HttpClientBuilder& with_timeout(Duration d) { timeout_ = d; return *this; }
    HttpClientBuilder& with_retries(int n)    { retries_ = n; return *this; }
    HttpClient build() &&;                     // && — call only on rvalue, prevents reuse
private:
    std::optional<URL> url_;
    std::optional<Duration> timeout_;
    int retries_ = 3;
};
```

Combine with type-state (templates on a `Stage` tag) when required
fields must be enforced statically.

## CRTP — sparingly

Curiously Recurring Template Pattern is for mixing in static behaviour:

```cpp
template <typename T>
class Comparable {
public:
    bool operator!=(const T& other) const { return !(static_cast<const T&>(*this) == other); }
};

class Money : public Comparable<Money> { /* defines == */ };
```

C++20 makes most CRTP uses obsolete — `operator<=>` defaults handle
the comparison case above for free. Use CRTP only when there's no
modern equivalent.
