"""Simulated download manager with progress events."""

import time
from enum import Enum, auto

from avyra import EventBus


class DownloadEvent(Enum):
    STARTED = auto()
    PROGRESS = auto()
    DONE = auto()
    ERROR = auto()


def download_simulator(bus: EventBus, url: str):
    bus.emit(DownloadEvent.STARTED, {"url": url})

    for pct in range(0, 101, 25):
        time.sleep(0.5)
        bus.emit(DownloadEvent.PROGRESS, {"url": url, "pct": pct})
        if pct == 50:
            bus.emit(DownloadEvent.ERROR, {"url": url, "msg": "Connection lost"})
            return

    bus.emit(DownloadEvent.DONE, {"url": url})


if __name__ == "__main__":
    bus = EventBus()
    bus.register(DownloadEvent)

    bus.subscribe(DownloadEvent.STARTED, lambda e, p: print(f"[ ] {p['url']}"))
    bus.subscribe(DownloadEvent.PROGRESS, lambda e, p: print(f"    {p['pct']}%"))
    bus.subscribe(DownloadEvent.DONE, lambda e, p: print(f"[✓] {p['url']}"))
    bus.subscribe(DownloadEvent.ERROR, lambda e, p: print(f"[✗] {p['url']}: {p['msg']}"))

    download_simulator(bus, "https://example.com/file.zip")
