from pydantic import BaseModel, Field
from typing import List
import time
from enum import Enum


class MessageType(Enum):
    CONNECT = "connect"
    GET_WORLD = "get_world"
    GET_WORLD_RESPONSE = "get_world_response"
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
    size: int


class ResultResponse(BaseModel):
    result: str
    error: str | None = None
    details: str | None = None


########################################################################################################################
class ConnectRequest(BaseModel):
    port: int


########################################################################################################################

class GetWorldResponse(BaseModel):
    worlds: List[dict]


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

    content: (None | ResultResponse | ConnectRequest | GetWorldResponse |
              CreateGameRequest | CreateGameResponse |
              RunGameRequest | RunGameResponse |
              DeleteGameRequest | WorldUpdate) = None
