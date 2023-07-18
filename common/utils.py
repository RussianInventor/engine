import model
from data_base import new_session

def procedure_generation(world:model.World):
    with new_session() as session:
        chunks = session.query(model.Chunk).filter(model.Chunk.world_id == world.id).all()
        for chu in filter(lambda c: any([c.x == 0,
                                         c.x == world.size-1,
                                         c.y == 0,
                                         c.y == world.size - 1]),
                           chunks):
            chu.biome = model.Biome.MEGA_MOUNTAINS.value
