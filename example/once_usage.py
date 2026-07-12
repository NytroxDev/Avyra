"""Example showing one-shot subscriptions with once()."""

from enum import Enum, auto

from avyra import EventBus


class AppEvent(Enum):
    READY = auto()
    SHUTDOWN = auto()


def on_ready(event, payload):
    print("App is ready — this runs only once")


def on_shutdown(event, payload):
    print("Shutting down — cleaning up resources")
    raise RuntimeError("cleanup failed")  # still unsubscribed!


if __name__ == "__main__":
    bus = EventBus()
    bus.register(AppEvent)

    bus.once(AppEvent.READY, on_ready)
    bus.once(AppEvent.SHUTDOWN, on_shutdown)

    bus.emit(AppEvent.READY, None)   # on_ready fires
    bus.emit(AppEvent.READY, None)   # nothing — already unsubscribed

    failed = bus.emit(AppEvent.SHUTDOWN, None)
    bus.emit(AppEvent.SHUTDOWN, None)  # nothing — auto-unsub even after crash

    for _handler, exc in failed:
        print(f"  Caught: {exc}")
