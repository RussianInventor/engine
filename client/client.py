import socket
import json
import threading
import time
import uuid
from common.connection_utils import read_message



class Client:
    def __init__(self, host, port, listening_port):
        self.host = host
        self.port = port
        self.sending_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_port = listening_port
        self.id = uuid.uuid4().__str__()
        self.sending_thread = threading.Thread(target=self.sending)
        self.listening_thread = None
        self.input_connection = None
        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket.bind(('localhost', self.listening_port))
        self.to_server = None
        self.from_server = None

    def send(self, message):
        self.sending_socket.send(message.encode("UTF-8"))
        print(f'send: {message}')

    def connect(self):
        self.sending_socket.connect((self.host, self.port))
        message = {"title": "connect", "content": {"client_id": self.id, "port": self.listening_port}}
        self.send(json.dumps(message))
        response = self.sending_socket.recv(1024)
        print(response.decode("utf-8"))
        self.wait_connection()

    def wait_connection(self):
        print('run listening')
        self.listening_socket.listen()
        while True:
            self.input_connection, _ = self.listening_socket.accept()
            self.send(json.dumps({"success": True}))
            self.listening_thread = threading.Thread(target=self.listen)
            self.listening_thread.start()

    def listen(self):
        while True:
            msg = read_message(self.input_connection)
            print(msg)

    def sending(self):
        while True:
            if not self.to_server.empty():
                msg = self.to_server.get()
                self.send(json.dumps(msg))
