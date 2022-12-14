import socket
import json
import queue
import threading
import time

from messages import Message


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
    return Message(**message.items())


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
    def __init__(self):
        self.connections = {}
        self.game = None
        self.input_messages = queue.PriorityQueue()
        self.output_messages = queue.PriorityQueue()

    def send_message(self, connection_id, message):
        connection = self.connections.get(connection_id)
        connection.send(message)

    def read_message(self, connection_id) -> Message:
        connection = self.connections.get(connection_id)
        return connection.read()


class Server(App):
    port_num = 4000
    backlog = 10

    def __init__(self):
        super().__init__()
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
        self.connection = Connection(id=name,
                                     listening_port=listening_port,
                                     address=(host, port))
        self.connection.send(Message(title='connect',
                                     time=time.time(),
                                     content={'port': self.connection.listening_socket.getsockname()[1]},
                                     author=name,
                                     receiver='server'))

# conn = Connection('999', 5555, ('localhost', 4444))