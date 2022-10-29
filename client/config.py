import dotenv
import os

path = dotenv.find_dotenv('.env')
dotenv.load_dotenv(dotenv_path=path)


class Config:
    host = os.environ.get('CLIENT_HOST')
    port = int(os.environ.get('CLIENT_PORT'))

    server_host = os.environ.get('SERVER_HOST')
    server_port = int(os.environ.get('SERVER_PORT'))
