import logging
import socket
import json
import queue
import threading
import time
from abc import ABC, abstractmethod
from .messages import Message, MessageType


class User:

    def __init__(self, user_id):
        self.user_id = user_id


def read(sock):
    data = bytearray()
    while True:
        try:
            data += sock.recv(1024)
        except Exception as error:
            print(error)
        try:
            message = json.loads(data)
        except json.JSONDecodeError:
            pass
        except UnicodeDecodeError:
            pass
        else:
            break

    if 'title' in message.keys():
        return Message(connection=sock, **message)
    else:
        return message


class Connection:
    def __init__(self, id, listening_port, address):
        self.id = id

        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket.bind(('localhost', listening_port))

        self.sending_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sending_socket.connect(address)

        print(self.listening_socket.getsockname())
        print(self.sending_socket.getsockname())
        self.listen()

    def send(self, msg):
        self.sending_socket.send(msg.json().encode('utf- 8'))

    def read(self):
        msg = read(self.listening_socket)
        return msg

    def listen(self):
        self.listening_socket.listen()
        addr, conn = self.listening_socket.accept()


class App(ABC):
    def __init__(self, user_id, app):
        self.connections = {}

        self.input_messages = queue.PriorityQueue()
        self.output_messages = queue.PriorityQueue()

        self.game = None
        self.user = User(user_id)
        self.app = app

    @abstractmethod
    def get_sending_socket(self, receiver):
        pass

    def send_message(self, message: Message, connection=None, answer_wait=True, log_level="info"):
        if connection is None:
            connection: socket.socket = self.get_sending_socket(message.receiver)
        else:
            pass
        # getattr(logging, log_level)(f'send: {message.json()}')
        connection.send(message.json().encode('utf- 8'))
        if answer_wait:
            answer = read(connection)
#             getattr(logging, log_level)(f'answer: {answer.json()}')
            return answer

    def read_message(self, connection_id) -> Message:
        connection = self.connections.get(connection_id)
        return connection.read()


class Server(App):
    port_num = 4000
    backlog = 10

    def __init__(self, app, id, port):
        super().__init__(user_id=id, app=app)
        self.main_port = port
        self.receivers = {}  # {client_id: socket, ...} - receivers for world updates, server.py sends, they listen
        self.connections = {}  # {client_id: socket, ...} - both-ways connections

        self.listening_thread = threading.Thread(target=self.listen)
        # self.broadcasting_thread = threading.Thread(target=self.broadcast)

    def get_sending_socket(self, receiver):
        return self.connections.get(receiver)

    def listen(self):
        main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        main_socket.bind(('localhost', self.main_port))
        logging.debug(f'listen on port {self.main_port}...')
        main_socket.listen(self.backlog)
        while True:
            try:
                sock, address = main_socket.accept()
                logging.debug(f'accept {address}')
                self.new_connection(sock, address)
            except Exception as error:
                pass

    def listen_clients(self):
        logging.debug('listen clients')
        while True:
            for client_id, conn in self.connections.items():
                msg = read(conn)
                logging.info(f'get msg from {client_id}: {msg.json()}')
                self.app.state.handle_messages(msg=msg)

    def new_connection(self, sock, address):
        msg = read(sock)
        logging.info(msg)
        if isinstance(msg, Message) and msg.type == MessageType.CONNECT:
            logging.info(f'new connection from {address}')
            client_id = msg.author
            self.connections[client_id] = sock
            self.receivers[client_id] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            logging.debug(f'try to connect to {address[0]}:{msg.content.get("port")}')
            msg.answer({'result': 'success'})
            self.receivers[client_id].connect((address[0], msg.content.get("port")))
            self.app.clients[client_id] = 0
        else:
            print('fail')
            pass

    def send_update(self, chunks, objects):
        content = {"chunks": chunks, "objects": [obj for obj in objects if obj is not None]}
        for player_id, player_status in self.app.clients.items():
            if player_status == 1:
                new_message = Message(connection=self.get_sending_socket(self.app.game.players[0]),
                                      title=MessageType.WORLD_UPDATE,
                                      time=time.time(),
                                      content=content,
                                      author="server",
                                      receiver=player_id)
                self.send_message(new_message, self.receivers[player_id], answer_wait=False, log_level="debug")


class Client(App):
    def __init__(self, app, id, port):
        super().__init__(user_id=id, app=app)
        self.listening_port = port
        self.address_server = None
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def server_listen(self, connection):
        while True:
            msg = read(connection)
            logging.info(f'get msg from server: {msg.json()}')
            self.app.state.handle_message(msg=msg)

    def get_sending_socket(self, receiver=None):
        return self.connection

    def listen(self):
        logging.info('start listening...')
        self.listening_socket.bind(('localhost', self.listening_port))
        while True:
            self.listening_socket.listen()
            self.listening_socket.settimeout(2)
            try:
                conn, address = self.listening_socket.accept()
                logging.info(f'input connection from {address}')
                self.server_listen(conn)
                break
                # m = Message(self.listening_socket, 'test', time.time(), {'test': 'test'}, self.user.user_id, 'server.py')
                # self.send_message(m)
            except TimeoutError:
                if self.connection is None:
                    break
            except Exception as err:
                logging.error(err.with_traceback(None))
                break
        # self.listening_socket.close()
        # self.listening_socket = conn

    def connect(self, host, port, name, listening_port):
        logging.info(f'connecting to {host}:{port}...')
        listening_thread = threading.Thread(target=self.listen)
        listening_thread.start()
        msg = Message(connection=self.connection,
                      title='connect',
                      time=time.time(),
                      content={'port': self.listening_port},
                      author=name,
                      receiver='server.py')
        try:
            self.connection.connect((host, port))
            self.send_message(msg)
            result = True
            self.address_server = host, port
        except ConnectionRefusedError as err:
            logging.error(err)
            result = False
        return result
