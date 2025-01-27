import math
from common.exchange import messages
from common import blueprint_game_objects


class Player:
    def __init__(self, obj: blueprint_game_objects.Creature, world, app):
        self.world = world
        self.obj = obj
        self.app = app

    @property
    def x(self):
        return self.obj.x

    @property
    def y(self):
        return self.obj.y

    @property
    def v_x(self):
        return self.obj.v_x

    @property
    def v_y(self):
        return self.obj.v_y

    @v_x.setter
    def v_x(self, val):
        self.obj.v_x = val

    @v_y.setter
    def v_y(self, val):
        self.obj.v_y = val

    @property
    def step(self):
        return 1

    def create_stick(self):
        self.app.exchanger.send_message(messages.Message(type=messages.MessageType.CLIENT_UPDATE,
                                                         author=self.app.exchanger.user.user_id,
                                                         receiver="server",
                                                         content=messages.ClientUpdate(command=messages.Command.create_stick)),
                                        answer_wait=False)

    def down(self):
        self.app.exchanger.send_message(messages.Message(type=messages.MessageType.CLIENT_UPDATE,
                                                         author=self.app.exchanger.user.user_id,
                                                         receiver="server",
                                                         content=messages.ClientUpdate(command=messages.Command.down)),
                                        answer_wait=False)

    def up(self):
        self.app.exchanger.send_message(messages.Message(type=messages.MessageType.CLIENT_UPDATE,
                                                         author=self.app.exchanger.user.user_id,
                                                         receiver="server",
                                                         content=messages.ClientUpdate(command=messages.Command.up)),
                                        answer_wait=False)

    def right(self):
        self.app.exchanger.send_message(messages.Message(type=messages.MessageType.CLIENT_UPDATE,
                                                         author=self.app.exchanger.user.user_id,
                                                         receiver="server",
                                                         content=messages.ClientUpdate(command=messages.Command.right)),
                                        answer_wait=False)

    def left(self):
        self.app.exchanger.send_message(messages.Message(type=messages.MessageType.CLIENT_UPDATE,
                                                         author=self.app.exchanger.user.user_id,
                                                         receiver="server",
                                                         content=messages.ClientUpdate(command=messages.Command.left)),
                                        answer_wait=False)

    def stop_x(self):
        self.app.exchanger.send_message(messages.Message(type=messages.MessageType.CLIENT_UPDATE,
                                                         author=self.app.exchanger.user.user_id,
                                                         receiver="server",
                                                         content=messages.ClientUpdate(command=messages.Command.stop_x)),
                                        answer_wait=False)

    def stop_y(self):
        self.app.exchanger.send_message(messages.Message(type=messages.MessageType.CLIENT_UPDATE,
                                                         author=self.app.exchanger.user.user_id,
                                                         receiver="server",
                                                         content=messages.ClientUpdate(command=messages.Command.stop_y)),
                                        answer_wait=False)
