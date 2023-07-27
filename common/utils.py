import model
from config import Config
import random
from data_base import new_session


def expansion(chunks, biome, x, y, num):
    if num < 1:
        return
    num -= 1
    move = random.randint(-1, 1)
    new_x = x
    new_y = y
    if (x + move) != x:
        new_x = x + move
    else:
        move = random.choice((-1, 1))
        new_y = y + move
    filter(lambda c: c.x == new_x and c.y == new_y, chunks).__next__().biome = biome.value
    expansion(chunks, biome, new_x, new_y, num)


def procedure_generation(world:model.World):
    with new_session() as session:
        chunks = session.query(model.Chunk).filter(model.Chunk.world_id == world.id).all()
        chunks_num = len(chunks) * len(chunks)
        water_num = int(chunks_num * (Config.world_percents["water"]/100))
        mountains_num = int(chunks_num * (Config.world_percents["mountains"]/100))
        desert_num = int(chunks_num * (Config.world_percents["desert"]/100))
        while water_num > 1:
            water_size = int(random.randint(*Config.biome_percents["water"])/100 * water_num)
            x = random.randint(1, world.size-2)
            y = random.randint(1, world.size-2)
            filter(lambda c: c.x == x and c.y == y, chunks).__next__().biome = model.Biome.WATER.value
            water_size -= 1
            water_num -= 1
            expansion(chunks=chunks, biome=model.Biome.WATER, x=x, y=y, num=water_size)

        for chu in filter(lambda c: any([c.x == 0,
                                         c.x == world.size-1,
                                         c.y == 0,
                                         c.y == world.size - 1]),
                           chunks):
            chu.biome = model.Biome.MEGA_MOUNTAINS.value
