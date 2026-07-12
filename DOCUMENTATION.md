# Avyra Documentation

Full API reference for `avyra` v1.0.0.

---

## `EventBus()`

Create an event bus with no registered events. Use :meth:`register` to add event types.

```python
bus = EventBus()
bus.register(Message)            # all members
bus.register([Message.SENT])     # specific members only
```

---

## `register(event_types)`

Register additional event types after creation. Already-registered members are silently skipped.

| Parameter     | Type                       | Description                                      |
|---------------|----------------------------|--------------------------------------------------|
| `event_types` | `Enum \| type[Enum] \| list[Enum]` | An ``Enum`` member, class, or list of members. |

```python
bus.register(Message)            # all members of Message
bus.register([Message.SENT])     # specific members
```

---

## `subscribe(event_type, function)`

Register *function* for *event_type*.

| Parameter    | Type                 | Description                                      |
|--------------|----------------------|--------------------------------------------------|
| `event_type` | `Enum \| type[Enum]` | Member or class (subscribes to **all** members). |
| `function`   | `Subscriber`         | `Callable[[Enum, object \| None], None]`         |

Raises `ValueError` if already subscribed or unknown event type.

```python
bus.subscribe(Message.SENT, handler)
bus.subscribe(Message, handler)          # all members
```

---

## `on(event_type)` *(decorator)*

Decorator shorthand for :meth:`subscribe`.

| Parameter    | Type                 | Description                                      |
|--------------|----------------------|--------------------------------------------------|
| `event_type` | `Enum \| type[Enum]` | Member or class (subscribes to **all** members). |

```python
@bus.on(Message.SENT)
def handler(event, payload):
    ...

@bus.on(Message)                      # all members
def handler_all(event, payload):
    ...
```

---

## `unsubscribe(event_type, function)`

Remove *function* from *event_type*.

| Parameter    | Type                 | Description                                                                |
|--------------|----------------------|----------------------------------------------------------------------------|
| `event_type` | `Enum \| type[Enum]` | Member or class (removes from **all** members).                            |
| `function`   | `Subscriber`         | The registered callable or original function (works with `once` wrappers). |

Raises `ValueError` if not found.

```python
bus.unsubscribe(Message.SENT, handler)
bus.unsubscribe(Message, handler)        # all members
```

---

## `emit(event, payload=None) → list[tuple[Subscriber, Exception]]`

Dispatch *event* to all subscribers.

| Parameter | Type             | Description                               |
|-----------|------------------|-------------------------------------------|
| `event`   | `Enum`           | The member identifying the event.         |
| `payload` | `object \| None` | Optional data passed to every subscriber. |

If a subscriber raises, the exception is caught and remaining
subscribers are still called. Returns a list of `(subscriber, exception)`
for every failed call.

```python
failed = bus.emit(Message.SENT, data)
for handler, exc in failed:
    print(f"{handler} failed with {exc}")
```

---

## `once(event_type, function)`

One-shot subscription. *function* fires at most once, then is
automatically unsubscribed — even if it raises.

| Parameter    | Type                 | Description                               |
|--------------|----------------------|-------------------------------------------|
| `event_type` | `Enum \| type[Enum]` | Member or class (one wrapper per member). |
| `function`   | `Subscriber`         | The callable to invoke once.              |

The wrapper uses ``functools.wraps`` so ``has_subscriber`` and
``unsubscribe`` recognise it by the original function (via ``__wrapped__``).

```python
bus.once(Message.CONNECTED, on_connected)
```

---

## `has_subscriber(event_type, function) → bool`

Check whether *function* is registered.

| Parameter    | Type                 | Description               |
|--------------|----------------------|---------------------------|
| `event_type` | `Enum \| type[Enum]` | Member or class.          |
| `function`   | `Subscriber`         | The callable to look for. |

Returns `True` only if **every** resolved member has the function
(directly or inside a `once` wrapper).

```python
bus.has_subscriber(Message.SENT, handler)  # True / False
```

---

## `clear(event_type)`

Remove all subscribers for *event_type*.

| Parameter    | Type                 | Description                               |
|--------------|----------------------|-------------------------------------------|
| `event_type` | `Enum \| type[Enum]` | Member or class (clears **all** members). |

Raises `ValueError` if unknown.

```python
bus.clear(Message.SENT)
bus.clear(Message)                     # clear everything
```

---

## AsyncEventBus

`AsyncEventBus` exposes the **same API** as `EventBus` (`subscribe`,
`unsubscribe`, `once`, `has_subscriber`, `clear`), but its `emit` and
`once` support **both sync and async** subscribers.

```python
from avyra import AsyncEventBus

bus = AsyncEventBus()
bus.register(Message)

# sync subscriber — called directly
bus.subscribe(Message.SENT, lambda e, p: print(p))

# async subscriber — awaited
async def on_read(event, payload):
    await process(payload)

bus.subscribe(Message.READ, on_read)

# emit is async
await bus.emit(Message.SENT, "hello")
```

### `emit(event, payload=None)`

```python
async def emit(self, event, payload=None) -> list[tuple[Subscriber, Exception]]:
```

Sync subscribers are called with `sub(event, payload)`.  Async
subscribers are called and then ``await``\ ed.  Exceptions are caught
and returned identically to `EventBus.emit`.

### `once(event_type, function)`

Works with both sync and async functions.  The auto-unsubscribe is
guaranteed even if the function raises.

```python
async def on_startup(event, payload):
    await init_db()

bus.once(AppEvent.STARTUP, on_startup)
await bus.emit(AppEvent.STARTUP, None)   # fires once
await bus.emit(AppEvent.STARTUP, None)   # silent
```

---

## Internal Helpers

### `_get_sub(event_type) → list[Subscriber] | None`

Return a lock-safe shallow copy of the subscriber list for a single
member. Returns `None` if no subscribers exist.

### `_original_sub(func) → Subscriber`

Return the original function behind a `once` wrapper, or *func* itself.

---

## Thread Safety

- All mutations (`subscribe`, `unsubscribe`, `clear`) are serialised
  with a `threading.RLock()`.
- `emit` iterates over a snapshot copy so concurrent subscribe/unsubscribe
  never affect in-flight dispatch.

```python
# safe from any thread
bus.subscribe(Message.SENT, handler)
bus.emit(Message.SENT, data)
```

---

## Type Aliases

### Sync

```python
Subscriber = Callable[[Enum, object | None], None]
```

### Async

```python
Subscriber = Callable[[Enum, object | None], None] \
           | Callable[[Enum, object | None], Awaitable[None]]
```
