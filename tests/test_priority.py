import pytest

from avyra import AsyncEventBus, EventBus
from tests.conftest import Event


@pytest.fixture
def async_bus() -> AsyncEventBus:
    b = AsyncEventBus()
    b.register(Event)
    return b


class TestSubscribePriority:
    def test_default_priority(self, bus: EventBus, results):
        bus.subscribe(Event.FOO, lambda e, p: results.append("default"))
        bus.emit(Event.FOO)
        assert results == ["default"]

    def test_explicit_priority(self, bus: EventBus, results):
        bus.subscribe(Event.FOO, lambda e, p: results.append("p10"), priority=10)
        bus.emit(Event.FOO)
        assert results == ["p10"]

    def test_priority_order_low_first(self, bus: EventBus, results):
        bus.subscribe(Event.FOO, lambda e, p: results.append("p10"), priority=10)
        bus.subscribe(Event.FOO, lambda e, p: results.append("p-5"), priority=-5)
        bus.subscribe(Event.FOO, lambda e, p: results.append("p0"), priority=0)
        bus.emit(Event.FOO)
        assert results == ["p-5", "p0", "p10"]

    def test_priority_order_negative_and_positive(self, bus: EventBus, results):
        bus.subscribe(Event.FOO, lambda e, p: results.append("p5"), priority=5)
        bus.subscribe(Event.FOO, lambda e, p: results.append("p-10"), priority=-10)
        bus.subscribe(Event.FOO, lambda e, p: results.append("p-1"), priority=-1)
        bus.emit(Event.FOO)
        assert results == ["p-10", "p-1", "p5"]

    def test_same_priority_preserves_registration_order(self, bus: EventBus, results):
        bus.subscribe(Event.FOO, lambda e, p: results.append("first"), priority=0)
        bus.subscribe(Event.FOO, lambda e, p: results.append("second"), priority=0)
        bus.subscribe(Event.FOO, lambda e, p: results.append("third"), priority=0)
        bus.emit(Event.FOO)
        assert results == ["first", "second", "third"]

    def test_all_same_priority(self, bus: EventBus, results):
        bus.subscribe(Event.FOO, lambda e, p: results.append("a"), priority=5)
        bus.subscribe(Event.FOO, lambda e, p: results.append("b"), priority=5)
        bus.subscribe(Event.FOO, lambda e, p: results.append("c"), priority=5)
        bus.emit(Event.FOO)
        assert results == ["a", "b", "c"]


class TestUnsubscribeWithPriority:
    def test_unsubscribe_removes_correct_subscriber(self, bus: EventBus, results):
        def a(e, p):
            results.append("a")

        def b(e, p):
            results.append("b")

        bus.subscribe(Event.FOO, a, priority=-1)
        bus.subscribe(Event.FOO, b, priority=1)
        bus.unsubscribe(Event.FOO, a)
        bus.emit(Event.FOO)
        assert results == ["b"]

    def test_unsubscribe_does_not_affect_other_priorities(self, bus: EventBus, results):
        def a(e, p):
            results.append("a")

        def b(e, p):
            results.append("b")

        def c(e, p):
            results.append("c")

        bus.subscribe(Event.FOO, a, priority=-10)
        bus.subscribe(Event.FOO, b, priority=0)
        bus.subscribe(Event.FOO, c, priority=10)
        bus.unsubscribe(Event.FOO, b)
        bus.emit(Event.FOO)
        assert results == ["a", "c"]

    def test_unsubscribe_high_priority_only(self, bus: EventBus, results):
        def first(e, p):
            results.append("first")

        def last(e, p):
            results.append("last")

        bus.subscribe(Event.FOO, first, priority=-100)
        bus.subscribe(Event.FOO, last, priority=100)
        bus.unsubscribe(Event.FOO, first)
        bus.emit(Event.FOO)
        assert results == ["last"]


class TestOnceWithPriority:
    def test_once_respects_priority(self, bus: EventBus, results):
        bus.subscribe(Event.FOO, lambda e, p: results.append("sub-p0"), priority=0)
        bus.once(Event.FOO, lambda e, p: results.append("once-p-5"), priority=-5)
        bus.subscribe(Event.FOO, lambda e, p: results.append("sub-p10"), priority=10)
        bus.emit(Event.FOO)
        assert results == ["once-p-5", "sub-p0", "sub-p10"]

    def test_once_fires_in_priority_then_gone(self, bus: EventBus, results):
        bus.once(Event.FOO, lambda e, p: results.append("once-p-1"), priority=-1)
        bus.subscribe(Event.FOO, lambda e, p: results.append("sub-p0"), priority=0)
        bus.emit(Event.FOO)
        assert results == ["once-p-1", "sub-p0"]
        bus.emit(Event.FOO)
        assert results == ["once-p-1", "sub-p0", "sub-p0"]


class TestOnDecoratorWithPriority:
    def test_on_decorator_default_priority(self, bus: EventBus, results):
        @bus.on(Event.FOO)
        def handler(event, payload):
            results.append("handler")

        bus.emit(Event.FOO)
        assert results == ["handler"]

    def test_on_decorator_with_priority(self, bus: EventBus, results):
        @bus.on(Event.FOO, priority=10)
        def late(event, payload):
            results.append("late")

        @bus.on(Event.FOO, priority=-10)
        def early(event, payload):
            results.append("early")

        bus.emit(Event.FOO)
        assert results == ["early", "late"]

    def test_on_decorator_priority_ordering(self, bus: EventBus, results):
        @bus.on(Event.FOO, priority=5)
        def c(event, payload):
            results.append("c")

        @bus.on(Event.FOO, priority=-5)
        def a(event, payload):
            results.append("a")

        @bus.on(Event.FOO, priority=0)
        def b(event, payload):
            results.append("b")

        bus.emit(Event.FOO)
        assert results == ["a", "b", "c"]


class TestPriorityWithMultipleEventTypes:
    def test_independent_priority_per_event(self, bus: EventBus, results):
        bus.subscribe(Event.FOO, lambda e, p: results.append("foo-p10"), priority=10)
        bus.subscribe(Event.FOO, lambda e, p: results.append("foo-p-5"), priority=-5)
        bus.subscribe(Event.BAR, lambda e, p: results.append("bar-p0"), priority=0)
        bus.subscribe(Event.BAR, lambda e, p: results.append("bar-p-20"), priority=-20)
        bus.emit(Event.FOO)
        bus.emit(Event.BAR)
        assert results == ["foo-p-5", "foo-p10", "bar-p-20", "bar-p0"]

    def test_subscribe_class_with_priority(self, bus: EventBus, results):
        bus.subscribe(Event, lambda e, p: results.append("p10"), priority=10)
        bus.subscribe(Event, lambda e, p: results.append("p-5"), priority=-5)
        bus.emit(Event.FOO)
        assert results == ["p-5", "p10"]


class TestPriorityEdgeCases:
    def test_very_large_priority_values(self, bus: EventBus, results):
        bus.subscribe(Event.FOO, lambda e, p: results.append("max"), priority=999999)
        bus.subscribe(Event.FOO, lambda e, p: results.append("min"), priority=-999999)
        bus.emit(Event.FOO)
        assert results == ["min", "max"]

    def test_priority_with_exception_subscriber(self, bus: EventBus, results):
        def crash(e, p):
            raise RuntimeError("boom")

        bus.subscribe(Event.FOO, crash, priority=-10)
        bus.subscribe(Event.FOO, lambda e, p: results.append("after-crash"), priority=0)
        bus.emit(Event.FOO)
        assert results == ["after-crash"]

    def test_priority_with_crash_does_not_break_ordering(self, bus: EventBus, results):
        def crash(e, p):
            raise ValueError("fail")

        bus.subscribe(Event.FOO, lambda e, p: results.append("p-10"), priority=-10)
        bus.subscribe(Event.FOO, crash, priority=-5)
        bus.subscribe(Event.FOO, lambda e, p: results.append("p0"), priority=0)
        bus.subscribe(Event.FOO, lambda e, p: results.append("p10"), priority=10)
        bus.emit(Event.FOO)
        assert results == ["p-10", "p0", "p10"]

    def test_duplicate_priority_with_once(self, bus: EventBus, results):
        bus.once(Event.FOO, lambda e, p: results.append("once-a"), priority=0)
        bus.once(Event.FOO, lambda e, p: results.append("once-b"), priority=0)
        bus.emit(Event.FOO)
        assert results == ["once-a", "once-b"]
        bus.emit(Event.FOO)
        assert results == ["once-a", "once-b"]

    def test_has_subscriber_works_with_priority(self, bus: EventBus):
        def handler(e, p):
            pass

        bus.subscribe(Event.FOO, handler, priority=42)
        assert bus.has_subscriber(Event.FOO, handler) is True
        bus.unsubscribe(Event.FOO, handler)
        assert bus.has_subscriber(Event.FOO, handler) is False


@pytest.mark.asyncio
class TestAsyncPriority:
    async def test_async_priority_order(self, async_bus: AsyncEventBus, results):
        async_bus.subscribe(Event.FOO, lambda e, p: results.append("p10"), priority=10)
        async_bus.subscribe(Event.FOO, lambda e, p: results.append("p-5"), priority=-5)
        async_bus.subscribe(Event.FOO, lambda e, p: results.append("p0"), priority=0)
        await async_bus.emit(Event.FOO)
        assert results == ["p-5", "p0", "p10"]

    async def test_async_mixed_sync_async_priority(self, async_bus: AsyncEventBus, results):
        def sync_handler(e, p):
            results.append("sync-p0")

        async def async_handler(e, p):
            results.append("async-p-5")

        async_bus.subscribe(Event.FOO, sync_handler, priority=0)
        async_bus.subscribe(Event.FOO, async_handler, priority=-5)
        await async_bus.emit(Event.FOO)
        assert results == ["async-p-5", "sync-p0"]

    async def test_async_once_priority(self, async_bus: AsyncEventBus, results):
        async_bus.subscribe(Event.FOO, lambda e, p: results.append("sub-p10"), priority=10)
        async_bus.once(Event.FOO, lambda e, p: results.append("once-p-5"), priority=-5)
        await async_bus.emit(Event.FOO)
        assert results == ["once-p-5", "sub-p10"]
        await async_bus.emit(Event.FOO)
        assert results == ["once-p-5", "sub-p10", "sub-p10"]

    async def test_async_on_decorator_priority(self, async_bus: AsyncEventBus, results):
        @async_bus.on(Event.FOO, priority=-10)
        def early(event, payload):
            results.append("early")

        @async_bus.on(Event.FOO, priority=10)
        def late(event, payload):
            results.append("late")

        await async_bus.emit(Event.FOO)
        assert results == ["early", "late"]
