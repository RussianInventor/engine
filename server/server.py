import socket
import json
import queue
from common.events import Event
import threading


class Client:
    def __init__(self, address, input_connection, listen_port, server):
        self.address = address
        self.input_connection = input_connection
        self.output_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.output_connection.connect((self.address[0], listen_port))
        self.thread = threading.Thread(target=server.handle_client, args=(self,))


class Server:
    backlog = 20

    def __init__(self, host, port):
        self.to_clients = None
        self.from_client = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(self.backlog)
        self.clients = {}

    def set_from_queue(self, queue):
        self.from_client = queue

    def set_to_queue(self, queue):
        self.to_clients = queue

    def broadcast(self):
        while True:
            try:
                connection, address = self.socket.accept()
                self.handle_client(connection, address)
            except Exception as error:
                print(error)

    def read_message(self, connection):
        data = bytearray()
        while True:
            try:
                data += connection.recv(1024)
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
        return message

    def handle_connection(self, connection, address):
        message = self.read_message(connection)
        print('message: ', message)

        if message["title"] == "connect":
            self.clients[message['content']['client_id']] = Client(address=address,
                                                                   input_connection=connection,
                                                                   listen_port=message['content']['port'],
                                                                   server=self)
            connection.send(json.dumps({"success": True}).encode("utf-8"))
        else:
            connection.send(json.dumps({"success": False,
                                        "error": 'Не получены данные для подключения'}).encode("utf-8"))
            print('Не получены данные для подключения')

    def handle_client(self, client: Client):
        message = self.read_message(client.input_connection)
        print('message: ', message)

        if message["title"] == "event":
            self.create_event(message)
            client.input_connection.send(json.dumps({"success": True}).encode("utf-8"))

    def create_event(self, message):
        self.from_client.put((message['time'], Event(**message)))

    def listen(self):
        print('run listening')
        while True:
            try:
                connection, address = self.socket.accept()
                self.handle_connection(connection, address)
            except Exception as error:
                print(error)


#server = Server("localhost", 4000)
#server.listen()
