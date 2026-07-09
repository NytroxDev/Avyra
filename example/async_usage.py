"""Example showing AsyncEventBus with mixed sync/async subscribers."""

import asyncio
from enum import Enum, auto

from avyra import AsyncEventBus


class TaskEvent(Enum):
    SUBMITTED = auto()
    PROGRESS = auto()
    COMPLETED = auto()


async def main():
    bus = AsyncEventBus()
    bus.register(TaskEvent)

    # Sync subscriber
    bus.subscribe(TaskEvent.SUBMITTED, lambda e, p: print(f"  [sync] Task submitted: {p['id']}"))

    # Async subscriber
    async def on_progress(event, payload):
        await asyncio.sleep(0.05)
        print(f"  [async] {payload['pct']}%")

    bus.subscribe(TaskEvent.PROGRESS, on_progress)

    # One-shot async subscriber
    async def on_completed(event, payload):
        print(f"  [once] Task {payload['id']} done!")

    bus.once(TaskEvent.COMPLETED, on_completed)

    print("Emitting events...")
    await bus.emit(TaskEvent.SUBMITTED, {"id": 42})

    for pct in range(0, 101, 25):
        await bus.emit(TaskEvent.PROGRESS, {"pct": pct})

    await bus.emit(TaskEvent.COMPLETED, {"id": 42})
    await bus.emit(TaskEvent.COMPLETED, {"id": 42})  # already unsubscribed — silent


if __name__ == "__main__":
    asyncio.run(main())
