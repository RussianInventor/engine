from app.app import Client
import uuid
from client import client_state

c = Client(uuid.uuid4())
c.set_state(client_state.InitState)
#c.connect('localhost', 6000, '999', 6001)
