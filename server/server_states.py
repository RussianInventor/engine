import logging
import threading
import traceback
from abc import ABC, abstractmethod
from common.exchange import messages
from common import model, world as world_base
from sqlalchemy import or_
import uuid
from server.data_base import new_session
from server.game import Game
from common.generation import procedure_generation


class State(ABC):
    def __init__(self, app):
        self.app = app

    @abstractmethod
    def handle_message(self, msg: messages.Message):
        pass


class IdleState(State):
    def handle_message(self, msg: messages.Message):
        logging.info(f'handle message: {msg.title}: {msg.content}')
        if msg.title == messages.MessageType.RUN_GAME:
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

        if msg.title == messages.MessageType.GET_WORLD:
            with new_session() as session:
                q = session.query(model.World)
                q = q.filter(or_(model.World.private == False,
                                 model.World.owner == msg.author))
                worlds = q.all()
                msg.answer(
                    content={"worlds": [{c.name: i.__getattribute__(c.name) for c in i.__table__.c} for i in worlds]})
                # self.exchange.send_message(message.author, answer)

        if msg.title == messages.MessageType.CREATE_WORLD:
            world_id = str(uuid.uuid4())
            new_world = model.World(world_id)
            new_world.type = msg.content["type"]
            new_world.owner = msg.content["owner"]
            new_world.private = msg.content["private"]
            new_world.name = msg.content["name"]
            new_world.size = msg.content["size"]
            new_chunks = []
            with new_session(expire_on_commit=False) as session:
                session.add(new_world)
                session.flush()
                for x in range(msg.content["size"]):
                    for y in range(msg.content["size"]):
                        session.add(model.Chunk(uuid.uuid4(), new_world.id,
                                                x, y, model.Biome.FIELD))
                try:
                    session.commit()
                except Exception as err:
                    msg.answer(content={'error': str(err), 'details': traceback.format_exc()})
                    logging.error(str(err))
                    logging.error(traceback.format_exc())
                else:
                    msg.answer(content={c.name: new_world.__getattribute__(c.name) for c in new_world.__table__.c})
                procedure_generation(new_world)
        if msg.title == messages.MessageType.DELETE_WORLD:
            with new_session() as session:
                try:
                    session.query(model.Object).filter(model.Object.world_id == msg.content["id"]).delete()
                    session.query(model.Chunk).filter(model.Chunk.world_id == msg.content["id"]).delete()
                    session.delete(session.query(model.World).filter(model.World.id == msg.content["id"]).first())
                    session.commit()
                    msg.answer(content={"result": "success"})
                except Exception as err:
                    msg.answer(content={"result": str(err), "details": traceback.format_exc()})


class GamingState(State):
    def __init__(self, app, world_id, starter_id):
        super().__init__(app=app)
        with new_session() as session:
            world = world_base.World.from_db(session, world_id)
        self.app.game = Game(self.app, [starter_id], world)
        self.app.game.load_a_non_i()
        self.app.run_game()


    def handle_message(self, msg: messages.Message):
        if msg.title == messages.MessageType.CLIENT_READY:
            self.app.clients[msg.author] = 1

