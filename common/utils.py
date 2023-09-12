from . import model
from .config import Config
import random
from server.data_base import new_session


def expansion(chunks, biome, x, y, num, world):
    if num < 1:
        return
    num -= 1
    move = random.randint(-1, 1)
    new_x = x
    new_y = y
    if (x + move) != x:
        new_x = x + move
        if new_x < 0 or new_x >= world.size:
            new_x = x
    else:
        move = random.choice((-1, 1))
        new_y = y + move
        if new_y < 0 or new_y >= world.size:
            new_y = y
    filter(lambda c: c.x == new_x and c.y == new_y, chunks).__next__().biome = biome.value
    expansion(chunks, biome, new_x, new_y, num, world)


def get_biome_size(biome_type, static_biome_num):
    size = int(random.randint(*Config.biome_percents[biome_type]) / 100 * static_biome_num)
    if size < 1:
        size = 1
    return size


def procedure_generation(world: model.World):
    with new_session() as session:
        chunks = session.query(model.Chunk).filter(model.Chunk.world_id == world.id).all()
        chunks_num = len(chunks)
        water_num = int((chunks_num * (Config.world_percents["water"]) / 100))
        static_water_num = water_num
        mountains_num = int(chunks_num * (Config.world_percents["mountains"] / 100))
        static_mountains_num = mountains_num
        desert_num = int(chunks_num * (Config.world_percents["desert"] / 100))
        static_desert_num = desert_num
        while water_num > 1:
            water_size = get_biome_size("water", static_water_num)
            x = random.randint(1, world.size - 2)
            y = random.randint(1, world.size - 2)
            filter(lambda c: c.x == x and c.y == y, chunks).__next__().biome = model.Biome.WATER.value
            water_num -= water_size
            water_size -= 1
            expansion(chunks=chunks, biome=model.Biome.WATER, x=x, y=y, num=water_size, world=world)
        while desert_num > 1:
            desert_size = get_biome_size("desert", static_desert_num)
            x = random.randint(1, world.size - 2)
            y = random.randint(1, world.size - 2)
            filter(lambda c: c.x == x and c.y == y, chunks).__next__().biome = model.Biome.DESERT.value
            desert_num -= desert_size
            desert_size -= 1
            expansion(chunks=chunks, biome=model.Biome.DESERT, x=x, y=y, num=desert_size, world=world)
        while mountains_num > 1:
            mountains_size = get_biome_size("mountains", static_mountains_num)
            x = random.randint(1, world.size - 2)
            y = random.randint(1, world.size - 2)
            filter(lambda c: c.x == x and c.y == y, chunks).__next__().biome = model.Biome.MOUNTAINS.value
            mountains_num -= mountains_size
            mountains_size -= 1
            expansion(chunks=chunks, biome=model.Biome.MOUNTAINS, x=x, y=y, num=mountains_size, world=world)
        session.commit()
    with new_session() as session:
        chunks = session.query(model.Chunk).filter(model.Chunk.world_id == world.id).all()
        for chu in filter(lambda c: c.biome == model.Biome.WATER.value, chunks):
            x = chu.x
            y = chu.y
            for n_x in range(-1, 2):
                if x + n_x != world.size and x + n_x != 0:
                    for n_y in range(-1, 2):
                        if y + n_y != world.size and y + n_y != 0:
                            for chun in filter(lambda c: all((c.biome == model.Biome.FIELD.value,
                                                              c.x == n_x + x,
                                                              c.y == n_y + y)),
                                               chunks):
                                chun.biome = model.Biome.BEACH.value
        for chu in filter(lambda c: any([c.x == 0,
                                         c.x == world.size - 1,
                                         c.y == 0,
                                         c.y == world.size - 1]),
                          chunks):
            chu.biome = model.Biome.MEGA_MOUNTAINS.value
        session.commit()
