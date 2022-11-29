import dotenv
import os

path = dotenv.find_dotenv('.env')
dotenv.load_dotenv(dotenv_path=path)


class Config:
    host = os.environ.get('SERVER_HOST')
    port = int(os.environ.get('SERVER_PORT'))

    tick_duration = 0.01
