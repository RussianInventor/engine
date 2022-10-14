import socket
import json
import queue
from common.events import Event


class Server:
    backlog = 20

    def __init__(self, host, port):
        self.to_clients = None
        self.from_client = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(self.backlog)

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

    def handle_client(self, connection, address):
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
        print(message)
        if message["title"] == "event":
            self.create_event(message)
            connection.send(json.dumps({"success": True}).encode("utf-8"))
            print(f"Пришло от: {address}")
        elif message["title"] == "connect":
            connection.send(json.dumps({"success": True}).encode("utf-8"))
            print(f"Пришло от: {address}")

    def create_event(self, message):
        self.from_client.put((message['time'], Event(**message)))

    def listen(self):
        while True:
            try:
                connection, address = self.socket.accept()
                self.handle_client(connection, address)
            except Exception as error:
                print(error)


#server = Server("localhost", 4000)
#server.listen()
