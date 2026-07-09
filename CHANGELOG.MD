# Changelog

## 2.0.0

- **`EventBus()` / `AsyncEventBus()` now take no arguments** — bus starts empty.
- **`register()` method** to add event types after creation.
- **`@bus.on()` decorator** shorthand for ``subscribe``.
- **`_iter_members` now accepts `list[Enum]`** for flexibility.
- **`pyproject.toml`** with hatchling build backend, ready for PyPI.
- Documentation updated with decorator reference.
- 70 tests (up from 56).

## 1.0.0

- Add `once`, `has_subscriber`, `clear` methods.
- `emit` returns list of failed subscribers with exceptions.
- Accept `Enum` class anywhere a member is expected.
- Prevent duplicate subscriptions.
- Thread-safe snapshot dispatch.
