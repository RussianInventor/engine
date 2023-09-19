import dotenv
import os

path = dotenv.find_dotenv('.env')
dotenv.load_dotenv(dotenv_path=path)


class Config:
    host = os.environ.get('SERVER_HOST')
    port = int(os.environ.get('SERVER_PORT'))
    db_url = os.environ.get('DB_URL')
    game_db_url = os.environ.get('GAME_DB_URL')

    tick_duration = 0.01
