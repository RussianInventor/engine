from app.app import Client
import uuid
import logging
from client import client_state
from client.interface import run_interface
fhs = logging.FileHandler("log/client.log")
logging.getLogger("client").addHandler(fhs)
c = Client(uuid.uuid4())
c.set_state(client_state.InitState)
run_interface(c)
