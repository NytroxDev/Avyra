"""Simple chat system using the event bus."""

from enum import Enum, auto

from avyra import EventBus


class ChatEvent(Enum):
    MESSAGE = auto()
    JOIN = auto()
    LEAVE = auto()


class ChatRoom:
    def __init__(self):
        self.bus = EventBus()
        self.bus.register(ChatEvent)
        self.users = []

    def join(self, username: str):
        self.users.append(username)
        self.bus.emit(ChatEvent.JOIN, {"user": username})

    def leave(self, username: str):
        self.users.remove(username)
        self.bus.emit(ChatEvent.LEAVE, {"user": username})

    def send(self, username: str, text: str):
        self.bus.emit(ChatEvent.MESSAGE, {"user": username, "text": text})


if __name__ == "__main__":
    room = ChatRoom()

    room.bus.subscribe(ChatEvent.JOIN, lambda e, p: print(f">> {p['user']} joined"))
    room.bus.subscribe(ChatEvent.LEAVE, lambda e, p: print(f"<< {p['user']} left"))
    room.bus.subscribe(ChatEvent.MESSAGE, lambda e, p: print(f"<{p['user']}> {p['text']}"))

    room.join("Alice")
    room.join("Bob")
    room.send("Alice", "Hey Bob!")
    room.send("Bob", "Hi Alice!")
    room.leave("Bob")
