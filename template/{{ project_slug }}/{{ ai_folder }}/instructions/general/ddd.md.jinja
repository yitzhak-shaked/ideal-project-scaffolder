# Domain-Driven Design

This project models its problem space using DDD. The vocabulary below is
**not optional** — it's how every architecture discussion, PR description,
and refactor on this codebase is framed. The physical layering rules live
in `architecture.md`; this file covers the *modelling* concepts you put
inside those layers.

Canonical references: Eric Evans, *Domain-Driven Design* (the "Blue Book");
Vaughn Vernon, *Implementing Domain-Driven Design* (the "Red Book"); Percival
& Gregory, *Architecture Patterns with Python* ("Cosmic Python") for the
Python-flavoured rendition.

## Strategic DDD — the big picture

### Ubiquitous language

Every domain concept has **one name**, used identically in conversation,
documentation, and code. If the business says "shipment", the class is not
called `OrderDelivery`. When the language drifts in code, the model has
drifted; rename.

The `BOOTSTRAP` block at the top of the agent file (`CLAUDE.md` /
`AGENTS.md`) reserves a slot for a domain glossary — fill it in early and
keep it accurate.

### Bounded context

A bounded context is a region in which one consistent model and language
applies. "Customer" in *Sales* and "Customer" in *Support* are different
concepts even if they share an ID — model them separately, translate at
the seam.

This project starts as a single bounded context. When you find yourself
arguing about which of two meanings of a noun is the "real" one, you've
discovered a new context — split.

### Core domain

The part of the system that is the actual reason for its existence gets
the most design attention. Supporting subdomains may use simpler patterns,
off-the-shelf solutions, or even external services. Don't gold-plate
non-core code.

## Tactical DDD — the building blocks

These live in `src/domain/`. None of them may import from a database
library, HTTP client, or anything in `infrastructure/`.

### Entity

An object defined by **identity**, not by its attributes. Two `Order`
instances with the same fields but different IDs are different orders.

- Identity is assigned once and never changes.
- Entities are *not* equal by value; equality is by ID.
- Entities hold and enforce their own invariants — never leave validation
  to "whoever calls me later".

### Value object

An object defined by its **attributes**, with no identity. `Money(amount,
currency)`, `EmailAddress(str)`, `DateRange(start, end)`.

- Immutable.
- Equality is by value.
- Validates invariants in its constructor. Once you hold one, it is
  guaranteed valid — downstream code never needs to recheck.
- Replaces primitives in domain signatures. Don't pass a bare `float` for
  money or a bare `str` for an email — see `python/code-smells.md`
  (Primitive Obsession).

### Aggregate

A cluster of entities and value objects that is treated as a single unit
for consistency. The aggregate has one entity at its head — the
**aggregate root** — and that's the only object the outside world is
allowed to reference.

- Invariants that span multiple objects belong to the aggregate.
- One transaction = one aggregate (across aggregates, prefer eventual
  consistency).
- Repositories return aggregates (always at the root), never internal
  members.
- Aggregates should be small. If yours has dozens of children, look for
  a missed bounded-context split.

### Domain service

A piece of pure domain logic that doesn't naturally belong to any single
entity or value object — e.g. an exchange-rate calculation that needs
inputs from two aggregates. Domain services are stateless.

### Domain event

A statement that something meaningful happened in the past:
`OrderPlaced`, `PaymentReceived`, `StockDepleted`. Past tense. Immutable.
Carries enough data to be processed independently.

Events are how loosely-coupled parts of the system react to each other.
The handlers live in `application/`; the events themselves are part of
the domain.

### Repository

An interface that pretends the aggregate lives in an in-memory collection:
`get(id) -> Aggregate`, `add(aggregate)`, `remove(aggregate)`. Declared in
`domain/`. Implemented in `infrastructure/`.

The domain code uses the repository **interface** — it never imports
SQLAlchemy, requests, redis, etc.

### Unit of work

A single transactional boundary over one or more repositories. Used as a
context manager: enter, do work, exit (commit on success, roll back on
error). Application services orchestrate work through it; domain code
never sees it.

### Application service / use case

The orchestrator. Takes a Command (input DTO), loads the right aggregate
through a repository, calls a method on it, persists via the unit of
work, optionally emits events. Application services contain *no*
business rules — they only coordinate.

## Reading the layers as DDD

| Layer | DDD building blocks |
| --- | --- |
| `presentation/` | Translates the outside world (HTTP, CLI) into Commands and Queries. No domain logic. |
| `application/` | Use cases / command handlers. Orchestrates aggregates via repositories and unit of work. |
| `domain/` | Entities, value objects, aggregates, domain services, domain events, repository **interfaces**. Pure. |
| `infrastructure/` | Repository **implementations**, DB sessions, HTTP clients, message brokers. |

## Anti-patterns

- **Anemic domain model** — entities that are just data bags with getters
  and setters, and all the logic in application services. The behaviour
  belongs on the entity that owns the invariant.
- **Primitive obsession** — using `float`, `str`, `int` for domain concepts
  that deserve a value object.
- **Leaky aggregates** — exposing internal children to the outside world,
  letting callers reach inside and break invariants.
- **One giant aggregate** — the whole model in one root. The aggregate
  boundary should be the smallest set of objects that need to change
  together to satisfy an invariant.
- **Repository per table** — repositories belong to *aggregates*, not
  database tables. A single aggregate may map across multiple tables; a
  single table may not have a repository at all.

## When you're about to add or change a feature

1. Name it in the ubiquitous language. If the name doesn't already exist,
   create it explicitly and add it to the domain glossary.
2. Decide: is this an invariant of an existing aggregate, a new aggregate,
   a domain service, or just an application-layer orchestration?
3. Sketch the operation as a Command (input) and the resulting state
   change or event.
4. Write the test first — see `tdd.md`.
5. Implement the domain change first (entity method, value object), then
   the application service, then the infrastructure adapter, then the
   presentation wiring.
