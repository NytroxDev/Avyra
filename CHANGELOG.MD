# Changelog

## 1.2.0

- **`subscribe(event_type, function, priority=0)`** : new optional ``priority`` parameter controls dispatch order. Lower values execute first, default is ``0`` ([5b5742c](https://github.com/Nytrox/avyra/commit/5b5742c)).
- **`on(event_type, priority=0)`** : decorator now accepts ``priority`` — ``@bus.on(Event.FOO, priority=-10)`` runs before default subscribers ([5b5742c](https://github.com/Nytrox/avyra/commit/5b5742c)).
- **`once(event_type, function, priority=0)`** : one-shot subscriptions also respect priority ordering ([5b5742c](https://github.com/Nytrox/avyra/commit/5b5742c)).
- **`_get_sub()`** : subscriber snapshot now sorts by priority before returning — stable sort preserves registration order for equal priorities ([5b5742c](https://github.com/Nytrox/avyra/commit/5b5742c)).
- **`emit()`** : subscribers are dispatched in priority order (previously registration order only) ([5b5742c](https://github.com/Nytrox/avyra/commit/5b5742c)).
- **Docstrings** : updated ``subscribe``, ``on``, ``once``, ``emit`` with ``priority`` parameter docs and Args sections ([926363a](https://github.com/Nytrox/avyra/commit/926363a)).
- **Test suite** : 25 new tests covering priority ordering, unsubscribe with priority, once + priority, decorator priority, async priority, edge cases (crash mid-dispatch, extreme values, duplicate priorities) ([a64c392](https://github.com/Nytrox/avyra/commit/a64c392)).

## 1.1.0

- Unified type annotations (``Union[...]``/``Optional[...]`` → ``X | Y``).
- Replace dynamic ``_original`` attribute with ``functools.wraps`` (``__wrapped__``).
- Add ``py.typed`` marker for PEP 561 compliance.
- Add ``__init__.py`` to ``core/`` package.
- Add ``ruff`` and ``mypy`` configuration.
- Add missing async test coverage.
- Rewrite ``test_init`` to use public API.
- Add GitHub Actions CI (Python 3.8–3.14 matrix).
- Add ``CONTRIBUTING.md``, ``CODE_OF_CONDUCT.md``, ``SECURITY.md``.
- Add ``GUIDE.md`` with practical usage patterns.

## 1.0.0

- Typed events via ``Enum`` members (not strings).
- Thread-safe subscriber management with ``threading.RLock()``.
- ``subscribe``, ``unsubscribe``, ``has_subscriber``, ``clear``.
- ``emit`` with snapshot dispatch — returns ``list[(subscriber, exception)]``.
- ``once`` — one-shot subscription, auto-unsubscribes even on crash.
- ``register`` — add event types after creation.
- ``@bus.on()`` decorator shorthand for ``subscribe``.
- ``AsyncEventBus`` — same API, supports sync and async subscribers.
- Zero dependencies — pure Python.
