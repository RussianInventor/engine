class App:
    def __init__(self):
        self.state = None

    def set_state(self, state_cls, **kwargs):
        self.state = state_cls(self, **kwargs)

    def handle_message(self, msg):
        self.state.handle_message(msg)
