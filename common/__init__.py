import logging
import os
try:
    os.mkdir("log")
except FileExistsError:
    pass

logging.basicConfig(#filename="log.log",
                    filemode="w",
                    format="%(pathname)s \t %(message)s",
                    level=logging.DEBUG)
fhc = logging.FileHandler("log/client.log")
fhs = logging.FileHandler("log/server.log")
logging.getLogger("client").addHandler(fhc)
logging.getLogger("server").addHandler(fhs)
