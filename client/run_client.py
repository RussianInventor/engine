import socket
import json
import threading
import time
import uuid


class Client:
    def __init__(self, host, port, listening_port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_port = listening_port
        self.id = uuid.uuid4().__str__()
        self.sending_thread = threading.Thread(target=self.sending)
        self.listening_thread = None
        self.input_connection = None

    def send(self, message):
        self.socket.send(message.encode("UTF-8"))
        print(message)

    def connect(self):
        self.socket.connect((self.host, self.port))
        message = {"title": "connect", "content": {"client_id": self.id, "port": self.listening_port}}
        self.send(json.dumps(message))
        response = self.socket.recv(1024)
        return response.decode("utf-8")

    def wait_connection(self):
        print('run listening')
        while True:
            try:
                self.input_connection, _ = self.socket.accept()
                self.listening_thread = threading.Thread(target=self.listen)
                self.listening_thread.start()
                break
            except Exception as error:
                print(error)

    def listen(self):
        while True:
            pass

    def sending(self):
        pass


def run():
    client = Client("localhost", 5000, 4001)
    result = client.connect()
    print(result)

    client.send(json.dumps({"title": "event", "content": {'time': time.time(), 'author': "world", 'other': {}}}))
    response = client.socket.recv(1024)
    print(json.loads(response.decode("utf-8")))
    client.socket.close()


t1 = threading.Thread(target=run)
# t2 = threading.Thread(target=run)

t1.start()
# t2.start()

t1.join()
# t2.join()
