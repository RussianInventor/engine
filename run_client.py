from app.app import Client
import uuid
from client import client_state
from client.interface import run_interface

c = Client(uuid.uuid4())
c.set_state(client_state.InitState)
run_interface(c)
#c.connect('localhost', 6000, '999', 6001)
