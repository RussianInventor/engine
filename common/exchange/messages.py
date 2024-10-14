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
    RUN_GAME_RESPONSE = "run_game_response"

    CREATE_GAME = "create_world"
    DELETE_GAME = "delete_world"


    WORLD_UPDATE = "world_update"
    CLIENT_READY = "client_ready"
    RESULT = 'result'


class GameInfo(BaseModel):
    id: str | None
    name: str
    owner: str
    private: bool


class World(BaseModel):
    id: str
    type: str
    name: str
    size: int


class Chunk(BaseModel):
    id: str
    world_id: str
    x: int
    y: int
    biome: str


class Object(BaseModel):
    id: str
    world_id: str
    data: str
    cls: str


########################################################################################################################


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
    world_size: int


class CreateGameResponse(BaseModel):
    game: GameInfo


########################################################################################################################
class RunGameRequest(BaseModel):
    game_id: str


class RunGameResponse(BaseModel):
    world: World
    chunks: List[Chunk]
    objects: List[Object]


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
