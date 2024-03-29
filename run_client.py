from client.client import ClientApp
import logging
from client import client_state
from client.config import Config


f = open("log/client.log", mode="w")
f.close()
logging.basicConfig(format="%(pathname)s %(lineno)s:\t%(message)s", filemode="w")
log = logging.getLogger()
log.addHandler(logging.FileHandler("log/client.log"))
log.setLevel(logging.DEBUG)

c = ClientApp(Config.id, 6666)
c.set_state(client_state.InitState)
c.run()
