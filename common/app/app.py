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
    print(message)
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
    def __init__(self, user_id):
        self.connections = {}
        self.state = None

        self.input_messages = queue.PriorityQueue()
        self.output_messages = queue.PriorityQueue()

        self.game = None
        self.user = User(user_id)

    @abstractmethod
    def get_sending_socket(self, receiver):
        pass

    def send_message(self, message: Message):
        connection = self.get_sending_socket(message.receiver)
        connection.send(message.json().encode('utf- 8'))
        answer = read(connection)
        return answer

    def read_message(self, connection_id) -> Message:
        connection = self.connections.get(connection_id)
        return connection.read()

    def set_state(self, state_cls):
        self.state = state_cls(self)


class Server(App):
    port_num = 4000
    backlog = 10

    def __init__(self, id, port):
        super().__init__(id)
        self.main_port = port
        self.receivers = {}  # {client_id: socket, ...} - receivers for world updates, server sends, they listen
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
                print(error)

    def listen_clients(self):
        for client_id, conn in self.connections.items():
            msg = read(conn.listening_socket)
            print(f'get msg from {client_id}: {msg}')

    def new_connection(self, sock, address):
        msg = read(sock)
        if isinstance(msg, Message) and msg.type == MessageType.CONNECT:
            logging.info(f'new connection from {address}')
            client_id = msg.author
            self.connections[client_id] = sock
            self.receivers[client_id] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            logging.debug(f'try to connect to {address[0]}:{msg.content.get("port")}')
            self.receivers[client_id].connect((address[0], msg.content.get("port")))
        else:
            print('fail')
            pass


class Client(App):
    def __init__(self, id, port):
        super().__init__(id)
        self.listening_port = port
        self.address_server = None
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
            except TimeoutError:
                if self.connection is None:
                    break
            except Exception as err:
                logging.error(err.with_traceback(None))
                break
        self.listening_socket.close()
        self.listening_socket = conn

    def connect(self, host, port, name, listening_port):
        logging.info(f'connecting to {host}:{port}...')
        listening_thread = threading.Thread(target=self.listen)
        listening_thread.start()
        try:
            self.connection.connect((host, port))
            self.connection.send(Message(connection=self.connection,
                                         title='connect',
                                         time=time.time(),
                                         content={'port': self.listening_port},
                                         author=name,
                                         receiver='server').json().encode('utf- 8'))
            result = True
            self.address_server = host, port
        except ConnectionRefusedError as err:
            logging.error(err)
            result = False
        return result
