# Changelog

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
