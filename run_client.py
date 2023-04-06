from common.app.app import Client
import uuid
import logging
from client import client_state
from client.interface import run_interface

logging.basicConfig(format="%(pathname)s \t %(message)s")
log = logging.getLogger()
log.addHandler(logging.FileHandler("log/client.log"))
log.setLevel(logging.DEBUG)

c = Client(uuid.uuid4(), 6666)
c.set_state(client_state.InitState)
run_interface(c)
