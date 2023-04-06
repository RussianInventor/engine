import os
try:
    os.mkdir("log")
except FileExistsError:
    pass
