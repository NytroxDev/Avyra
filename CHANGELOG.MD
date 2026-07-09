# Changelog

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
