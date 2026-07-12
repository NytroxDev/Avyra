# Getting Started with Avyra

This guide walks you through the most common patterns for using Avyra.

---

## Installation

```bash
pip install avyra
```

---

## Basic Usage

Define your events as an ``Enum``, create a bus, register the events, and subscribe:

```python
from enum import Enum, auto
from avyra import EventBus

class UserEvent(Enum):
    LOGIN = auto()
    LOGOUT = auto()

bus = EventBus()
bus.register(UserEvent)

def on_login(event, payload):
    print(f"{payload} logged in")

bus.subscribe(UserEvent.LOGIN, on_login)
bus.emit(UserEvent.LOGIN, "Alice")  # >> Alice logged in
```

---

## Subscribing to All Events

Pass the ``Enum`` class instead of a member to subscribe to every event in that class:

```python
bus.subscribe(UserEvent, on_login)  # fires for LOGIN and LOGOUT
```

---

## The ``@bus.on()`` Decorator

Shorthand for ``subscribe``:

```python
@bus.on(UserEvent.LOGIN)
def on_login(event, payload):
    print(f"{payload} logged in")
```

Works with classes too:

```python
@bus.on(UserEvent)
def on_any(event, payload):
    print(f"Event: {event.name}, payload: {payload}")
```

---

## One-Shot Subscriptions

``once`` fires at most once, then auto-unsubscribes — even if the handler raises:

```python
bus.once(UserEvent.LOGIN, on_first_login)

bus.emit(UserEvent.LOGIN, "Alice")  # fires
bus.emit(UserEvent.LOGIN, "Bob")    # silent
```

---

## Error Handling

``emit`` never raises. If a subscriber crashes, the exception is caught
and the remaining subscribers still run. Failed calls are returned:

```python
def bad_handler(event, payload):
    raise RuntimeError("oops")

bus.subscribe(UserEvent.LOGIN, bad_handler)
bus.subscribe(UserEvent.LOGIN, on_login)

failed = bus.emit(UserEvent.LOGIN, "Charlie")

for handler, exc in failed:
    print(f"{handler} failed: {exc}")
```

---

## Unsubscribing

```python
bus.subscribe(UserEvent.LOGIN, on_login)
bus.unsubscribe(UserEvent.LOGIN, on_login)
```

Unsubscribing from the class removes the handler from all members:

```python
bus.unsubscribe(UserEvent, on_login)
```

---

## Checking Subscribers

```python
if bus.has_subscriber(UserEvent.LOGIN, on_login):
    print("subscribed")
```

---

## Clearing Subscribers

Remove all subscribers for one event or an entire class:

```python
bus.clear(UserEvent.LOGIN)  # one event
bus.clear(UserEvent)        # all members
```

---

## Async Usage

``AsyncEventBus`` has the same API but supports both sync and async subscribers:

```python
import asyncio
from avyra import AsyncEventBus

class TaskEvent(Enum):
    START = auto()
    DONE = auto()

async def main():
    bus = AsyncEventBus()
    bus.register(TaskEvent)

    # sync subscriber
    bus.subscribe(TaskEvent.START, lambda e, p: print("started"))

    # async subscriber
    async def on_done(event, payload):
        await asyncio.sleep(0.1)
        print("done")

    bus.subscribe(TaskEvent.DONE, on_done)

    await bus.emit(TaskEvent.START, None)
    await bus.emit(TaskEvent.DONE, None)

asyncio.run(main())
```

``once`` works the same way with async handlers:

```python
async def on_startup(event, payload):
    await init_db()

bus.once(TaskEvent.START, on_startup)
```

---

## Thread Safety

Avyra is safe to use from multiple threads. Subscribe, unsubscribe, and
emit can be called concurrently without data races:

```python
import threading

def worker(bus, event):
    bus.emit(event, "data")

threads = [
    threading.Thread(target=worker, args=(bus, UserEvent.LOGIN))
    for _ in range(10)
]

for t in threads:
    t.start()
for t in threads:
    t.join()
```

The subscriber list is protected by a ``threading.RLock``, and ``emit``
iterates over a snapshot copy so concurrent modifications never affect
an in-flight dispatch.

---

## Common Patterns

### Chat Room

```python
class ChatEvent(Enum):
    JOIN = auto()
    LEAVE = auto()
    MESSAGE = auto()

bus = EventBus()
bus.register(ChatEvent)

@bus.on(ChatEvent.JOIN)
def on_join(event, payload):
    print(f">> {payload['user']} joined")

@bus.on(ChatEvent.MESSAGE)
def on_message(event, payload):
    print(f"<{payload['user']}> {payload['text']}")

bus.emit(ChatEvent.JOIN, {"user": "Alice"})
bus.emit(ChatEvent.MESSAGE, {"user": "Alice", "text": "Hello!"})
```

### Download Manager

```python
class DownloadEvent(Enum):
    STARTED = auto()
    PROGRESS = auto()
    DONE = auto()
    ERROR = auto()

bus = EventBus()
bus.register(DownloadEvent)

@bus.on(DownloadEvent.PROGRESS)
def on_progress(event, payload):
    print(f"{payload['pct']}%")

@bus.on(DownloadEvent.ERROR)
def on_error(event, payload):
    print(f"Failed: {payload['msg']}")

failed = bus.emit(DownloadEvent.PROGRESS, {"url": "file.zip", "pct": 75})
```

---

## Next Steps

- See the full [API Reference](DOCUMENTATION.md) for parameter types and return values.
- Check the [examples](example/) directory for runnable scripts.
