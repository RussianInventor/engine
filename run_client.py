import socket
import json
import threading
import time
import uuid
from client.config import Config
from common.connection_utils import read_message

def run():
    client = Client(host=Config.server_host,
                    port=Config.server_port,
                    listening_port=Config.port)

    client.connect()

    client.send(json.dumps({"title": "event", "content": {'time': time.time(), 'author': "world", 'other': {}}}))
    response = client.sending_socket.recv(1024)
    print(json.loads(response.decode("utf-8")))
    client.sending_socket.close()


t1 = threading.Thread(target=run)
# t2 = threading.Thread(target=run)

t1.start()
# t2.start()

t1.join()
# t2.join()
