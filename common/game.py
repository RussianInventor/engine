import queue


class Player:
    def __init__(self, id, connection):
        self.id = id
        self.connection = connection

    def send_command(self, command):
        pass


class Game:
    EVENTS_UPDATE_LIMIT = 100

    def __init__(self, players, world):
        self.world = world
        self.players = players
        self.events = queue.PriorityQueue()
        self.message = queue.PriorityQueue()

    def update(self):
        while True:
            for _ in range(0, self.EVENTS_UPDATE_LIMIT):
                if self.events.empty():
                    break
                _, event = self.events.get()
                print(event.time, event.author, event.other)

