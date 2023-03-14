import socket
import json
import queue
import threading
import time
from .messages import Message



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
    return Message(connection=sock, **message)


class Connection:
    def __init__(self, id, listening_port, address):
        self.id = id

        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket.bind(('localhost', listening_port))

        self.sending_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sending_socket.connect(address)

        print(self.listening_socket.getsockname())

    def send(self, msg):
        self.sending_socket.send(msg.json().encode('utf-8'))

    def read(self):
        msg = read(self.listening_socket)
        return msg


class App:
    def __init__(self, id):
        self.connections = {}
        self.game = None
        self.id = id
        self.input_messages = queue.PriorityQueue()
        self.output_messages = queue.PriorityQueue()
        self.state = None

    def send_message(self, message):
        connection = self.connections.get(message.receiver)
        connection.send(message)
        answer = read(connection.sending_socket)
        return answer

    def read_message(self, connection_id) -> Message:
        connection = self.connections.get(connection_id)
        return connection.read()

    def set_state(self, state_cls):
        self.state = state_cls(self)


class Server(App):
    port_num = 4000
    backlog = 10

    def __init__(self, id):
        super().__init__(id)
        self.main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_thread = threading.Thread(target=self.listen)

    def run(self, server_port):
        self.main_socket.bind(('localhost', server_port))
        self.listening_thread.run()

    def listen(self):
        self.main_socket.listen(self.backlog)
        while True:
            try:
                sock, address = self.main_socket.accept()
                self.new_connection(sock, address)
            except Exception as error:
                print(error)

    def new_connection(self, sock, address):
        msg = read(sock)
        if msg.title == "connect":
            self.connections[msg.author] = Connection(id=msg.author,
                                                      listening_port=self.port_num + len(self.connections.keys()),
                                                      address=(address[0], msg.content['port']))


class Client(App):
    @property
    def connection(self):
        return self.connections['server']

    @connection.setter
    def connection(self, conn):
        self.connections['server'] = conn

    def connect(self, host, port, name, listening_port):
        try:
            self.connection = Connection(id=name,
                                         listening_port=listening_port,
                                         address=(host, port))
            self.connection.send(Message(connection=self.connection,
                                         title='connect',
                                         time=time.time(),
                                         content={'port': self.connection.listening_socket.getsockname()[1]},
                                         author=name,
                                         receiver='server'))
            return True
        except ConnectionRefusedError:
            return False
# conn = Connection('999', 5555, ('localhost', 4444))