from abc import ABC, abstractmethod


class State(ABC):
    def __init__(self, app):
        self.app = app

    @abstractmethod
    def handle_messages(self):
        pass


class IdleState(State):
    def handle_messages(self):



class GamingState(State):
    def handle_messages(self):



