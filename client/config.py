import dotenv
import os

path = dotenv.find_dotenv('.env')
dotenv.load_dotenv(dotenv_path=path)


class Keyboard:
    def __init__(self):
        self.key_dict = {}

    def set_key(self, key_code, function):
        self.key_dict[key_code] = function

    def get_key(self, key_code):
        return self.key_dict.get(key_code)


class Config:
    host = os.environ.get('CLIENT_HOST')
    port = int(os.environ.get('CLIENT_PORT'))

    server_host = os.environ.get('SERVER_HOST')
    server_port = int(os.environ.get('SERVER_PORT'))

    FPS = 30
    frame_duration = 1/FPS
