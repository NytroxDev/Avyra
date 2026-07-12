# Avyra

> **v1.0.0** : Lightweight, thread-safe publish-subscribe event bus.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![Tests](https://img.shields.io/badge/tests-82%20passed-green)](tests/)
[![PyPI](https://img.shields.io/badge/pypi-avyra-blue)](https://pypi.org/project/avyra/)

```bash
pip install avyra
```

```python
from enum import Enum, auto
from avyra import EventBus

class Message(Enum):
    SENT = auto()
    READ = auto()

bus = EventBus()
bus.register(Message)

@bus.on(Message.SENT)
def handler(event, payload):
    print(f"Sent: {payload}")

bus.emit(Message.SENT, "Hello!")
```

- **Typed events** : `Enum` members, not strings.
- **Thread-safe** : RLock-protected mutations, snapshot dispatch.
- **Zero dependencies** : pure Python.

**[Guide →](GUIDE.md)**  |  **[Documentation →](DOCUMENTATION.md)**  |  **[Changelog →](CHANGELOG.MD)**  |  **[License →](LICENSE)**

## Why Avyra?

Avyra provides a lightweight event system without external dependencies,
designed for applications where components need to communicate without
direct coupling.

### Tests

```bash
python -m pytest tests/ -v
```

82 tests covering subscribe, unsubscribe, emit, once, has_subscriber,
clear, register, edge cases, and thread safety.

### Examples

```bash
python example/chat.py
python example/downloader.py
python example/once_usage.py
python example/async_usage.py
```
