import sys


excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook
from common.app.app import Client
import uuid
import logging
from client import client_state
from client.interface import run_interface
from client.config import Config


f = open("log/client.log", mode="w")
f.close()
logging.basicConfig(format="%(pathname)s %(lineno)s:\t%(message)s", filemode="w")
log = logging.getLogger()
log.addHandler(logging.FileHandler("log/client.log"))
log.setLevel(logging.DEBUG)

c = Client(Config.id, 6666)
c.set_state(client_state.InitState)
run_interface(c)
