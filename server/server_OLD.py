import socket
import json
import queue
from common.events import Event
from common.connection_utils import read_message
import threading
from common.game import Game
from common.world import World


class Client:
    def __init__(self, id, address, input_connection, listen_port, server):
        self.id = id
        self.address = address
        self.listen_port = listen_port
        self.server = server
        self.input_connection = input_connection
        self.output_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_thread = None

    def connect(self):
        self.output_connection.connect((self.address[0], self.listen_port))
        self.listening_thread = threading.Thread(target=self.server.listen_client, args=(self,))


class Server:
    backlog = 20

    def __init__(self, host, port):
        self.to_clients = None
        self.from_client = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.host = host
        self.port = port
        self.socket.listen(self.backlog)
        self.clients = {}
        self.game = None

    def set_from_queue(self, queue: queue.PriorityQueue):
        self.from_client = queue

    def set_to_queue(self, queue: queue.PriorityQueue):
        self.to_clients = queue

    def broadcast(self):
        while True:
            if not self.to_clients.empty():
                msg = self.to_clients.get()
                for client_id, client in self.clients.items():
                    client.input_connection.send(json.dumps(msg))

    def handle_connection(self, connection, address):
        message = read_message(connection)
        print('message: ', message)

        if message["title"] == "connect":
            print(f'get connection message from {address}')
            self.send(connection=connection, msg=json.dumps({"success": True}))
            self.clients[message['content']['client_id']] = Client(id=message['content']['client_id'],
                                                                   address=address,
                                                                   input_connection=connection,
                                                                   listen_port=message['content']['port'],
                                                                   server=self)
            self.clients[message['content']['client_id']].connect()
        else:
            self.send(connection=connection, msg=json.dumps({"success": False,
                                                             "error": 'Не получены данные для подключения'}))
            print('Не получены данные для подключения')

    def listen_client(self, client: Client):
        message = read_message(client.input_connection)
        print('message: ', message)

        if message["title"] == "start":
            self.run_game(world_id=message['content']['world_id'],
                          player_id=client.id,
                          new=message["title"]['new'])

        if message["title"] == "event":
            self.create_event(message)
            self.send(connection=client.input_connection, msg=json.dumps({"success": True}))

    def run_game(self, player_id, new, world_id=None):
        if new:
            world = World()
        else:
            # TODO load world from db by id
            world = None
        self.game = Game(players=[player_id],
                         world=world)
        threading.Thread(target=self.game.update).start()

    def create_event(self, message):
        self.from_client.put((message['time'], Event(**message)))

    def listen(self):
        print(f'run server at {self.host}:{self.port}')
        while True:
            try:
                connection, address = self.socket.accept()
                self.handle_connection(connection, address)
            except Exception as error:
                print(error)

    def send(self, msg, connection):
        connection.send(msg.encode("UTF-8"))
        print(f'send: {msg}')

#server = Server("localhost", 4000)
#server.listen()
