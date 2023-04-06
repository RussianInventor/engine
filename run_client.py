import logging
import uuid
from app.app import Client
from client import client_state
from client.interface import run_interface

logging.basicConfig(format="%(pathname)s \t %(message)s")
log = logging.getLogger()
log.addHandler(logging.FileHandler("log/client.log"))
log.setLevel(logging.DEBUG)

c = Client(uuid.uuid4())
c.set_state(client_state.InitState)
run_interface(c)
