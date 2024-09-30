from pydantic import BaseModel, Field
from typing import List, Annotated
import time
from enum import Enum
from dataclasses import dataclass


class MessageType(Enum):
    CONNECT = "connect"
    GET_GAMES = "get_world"
    GET_GAMES_RESPONSE = "get_games_response"
    RUN_GAME = "run_game"
    CREATE_GAME = "create_world"
    WORLD_LIST = "world_list"
    DELETE_GAME = "delete_world"
    WORLD_UPDATE = "world_update"
    CLIENT_READY = "client_ready"
    RESULT = 'result'


class GameInfo(BaseModel):
    id: str | None
    name: str
    owner: str
    private: bool


class ResultResponse(BaseModel):
    result: str
    error: str | None = None
    details: str | None = None


########################################################################################################################
class ConnectRequest(BaseModel):
    port: int


########################################################################################################################

class GetGamesResponse(BaseModel):
    games: List[GameInfo]


########################################################################################################################
class CreateGameRequest(BaseModel):
    game: GameInfo


class CreateGameResponse(BaseModel):
    game: GameInfo


########################################################################################################################
class RunGameRequest(BaseModel):
    world_id: str


class RunGameResponse(BaseModel):
    world: dict
    chunks: list
    objects: list


########################################################################################################################
class DeleteGameRequest(BaseModel):
    game_id: str


########################################################################################################################
class WorldUpdate(BaseModel):
    chunks: list
    objects: list


########################################################################################################################
class Message(BaseModel):
    type: MessageType
    time: float = Field(default_factory=time.time)
    author: str
    receiver: str

    content: (None | ResultResponse | ConnectRequest | GetGamesResponse |
              CreateGameRequest | CreateGameResponse |
              RunGameRequest | RunGameResponse |
              DeleteGameRequest | WorldUpdate) = None
