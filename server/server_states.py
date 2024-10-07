import logging
import threading
import traceback
from abc import ABC, abstractmethod

from client.client_state import GamingState
from common.exchange import messages, Message
from common import model, world as world_base
from sqlalchemy import or_
import uuid

from common.exchange.messages import MessageType, GetGamesResponse, ResultResponse, GameInfo
from server.server import ServerApp
from server.data_base import new_session
from server.game import Game
from common.generation import procedure_generation


class State(ABC):
    def __init__(self, app: ServerApp):
        self.app = app

    @abstractmethod
    def handle_message(self, msg: messages.Message):
        pass


class IdleState(State):
    def handle_message(self, msg: messages.Message):
        logging.info(f'handle message: {msg.type}: {msg.content}')
        if msg.type == messages.MessageType.RUN_GAME:
            with new_session() as session:
                q = session.query(model.World)
                q = q.filter(model.World.id == msg.content["world_id"])
                world = q.first()
                content = {"world": world.get_dict(), "chunks": [], "objects": []}
                q = session.query(model.Chunk)
                q = q.filter(model.Chunk.world_id == msg.content["world_id"])
                q = q.order_by(model.Chunk.y, model.Chunk.x)
                content["chunks"] = [i.get_dict() for i in q.all()]
                q = session.query(model.Object)
                q = q.filter(model.Object.world_id == msg.content["world_id"])
                content["objects"] = [i.get_dict() for i in q.all()]
                msg.answer(content=content)
            self.app.set_state(GamingState, world_id=msg.content["world_id"], starter_id=msg.author)

        if msg.type == messages.MessageType.GET_GAMES:
            with new_session() as session:
                q = session.query(model.GameInfo)
                q = q.filter(or_(model.GameInfo.private == False,
                                 model.GameInfo.owner == msg.author))
                games = q.all()
            self.app.exchanger.answer(
                msg=Message(
                    type=MessageType.GET_GAMES_RESPONSE,
                    author='server',
                    receiver=msg.author,
                    content=GetGamesResponse(
                        games=[GameInfo(id=g.game_id,
                                        name=g.game_name,
                                        owner=g.owner,
                                        private=g.private) for g in games]
                    )),
                receiver=msg.author)
            # msg.answer(
            #     content={"worlds": [{c.name: i.__getattribute__(c.name) for c in i.__table__.c} for i in worlds]})
            # self.exchange.send_message(message.author, answer)

        if msg.type == messages.MessageType.CREATE_GAME:
            world_id = str(uuid.uuid4())
            new_game = model.GameInfo(game_id=uuid.uuid4(),
                                      game_name=msg.content.game.name,
                                      world_ids=[world_id],
                                      players=[],
                                      private=msg.content.game.private,
                                      owner=msg.content.game.owner)

            new_world = model.World(id=world_id,
                                    type='ground',
                                    name='ground world',
                                    size=msg.content.game.size)

            with new_session(expire_on_commit=False) as session:
                session.add(new_game)
                session.add(new_world)
                session.flush()
                for x in range(new_world.size):
                    for y in range(new_world.size):
                        session.add(model.Chunk(uuid.uuid4(), new_world.id,
                                                x, y, model.Biome.FIELD))
                try:
                    session.commit()
                except Exception as err:
                    self.app.exchanger.answer(msg=Message(type=MessageType.RESULT,
                                                          author="server",
                                                          receiver=msg.author,
                                                          content=ResultResponse(result='fail',
                                                                                 error=str(err),
                                                                                 details=traceback.format_exc())))
                    logging.error(str(err))
                    logging.error(traceback.format_exc())
                else:
                    self.app.exchanger.answer(msg=Message(type=MessageType.RESULT,
                                                          author="server",
                                                          receiver=msg.author,
                                                          content=ResultResponse(result='success')))
                    # msg.answer(content={c.name: new_world.__getattribute__(c.name) for c in new_world.__table__.c})
                procedure_generation(new_world)
        if msg.type == messages.MessageType.DELETE_GAME:
            game_id = msg.content.game_id

            with new_session() as session:
                try:
                    game_info = session.query(model.GameInfo).filter(model.GameInfo.game_id == game_id).first()

                    session.query(model.Object).filter(model.Object.world_id.in_(game_info.world_ids.)).delete()
                    session.query(model.Chunk).filter(model.Chunk.world_id.in_(game_info.world_ids)).delete()
                    session.query(model.World).filter(model.World.id.in_(model.GameInfo.world_ids)).delete()
                    session.delete(session.query(model.GameInfo).filter(game_id == game_id).first())
                    session.commit()
                    self.app.exchanger.answer(msg=Message(type=MessageType.RESULT,
                                                          author="server",
                                                          receiver=msg.author,
                                                          content=ResultResponse(result='success')))
                except Exception as err:
                    self.app.exchanger.answer(msg=Message(type=MessageType.RESULT,
                                                          author="server",
                                                          receiver=msg.author,
                                                          content=ResultResponse(result='fail',
                                                                                 error=str(err),
                                                                                 details=traceback.format_exc())))


class GamingState(State):
    def __init__(self, app, world_id, starter_id):
        super().__init__(app=app)
        with new_session() as session:
            world = world_base.World.from_db(session, world_id)
        self.app.game = Game(self.app, [starter_id], world)
        self.app.game.load_a_non_i()
        self.app.run_game()

    def handle_message(self, msg: messages.Message):
        if msg.type == messages.MessageType.CLIENT_READY:
            self.app.clients[msg.author] = 1
