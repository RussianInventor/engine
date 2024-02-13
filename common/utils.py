import pygame.display

from . import model
from .config import Config
import random
from server.data_base import new_session
import math
from .world import World
from . import game_objects
import json


def is_inside(x, y, points):
    x1 = x
    x2 = x + 1000000
    y1 = y
    y2 = y
    inter = 0
    for i in range(len(points)):
        x3 = points[i][0]
        x4 = points[i - 1][0]
        y3 = points[i][1]
        y4 = points[i - 1][1]
        u_down = ((y4 - y3) * (x2 - x1)) - ((x4 - x3) * (y2 - y1))
        if u_down == 0:
            continue
        u_up_a = ((x4 - x3) * (y1 - y3) - ((y4 - y3) * (x1 - x3)))
        u_up_b = ((x2 - x1) * (y1 - y3) - ((y2 - y1) * (x1 - x3)))
        ua = u_up_a / u_down
        ub = u_up_b / u_down
        if 0 <= ua <= 1 and 0 <= ub <= 1:
            inter += 1
    if inter % 2 == 0:
        return False
    return True


def stain_points(radius, x, y):
    points = []
    new_ang = 0
    angle = 360
    while angle > 0:
        d = random.randint(1, min(60, angle))
        angle -= d
        new_ang += d
        rad = random.randint(int(radius / 2), int(radius * 1.5))
        new_x = math.cos(math.radians(new_ang)) * rad
        new_y = math.sin(math.radians(new_ang)) * rad
        points.append((new_x + x, new_y + y))
    return points


def stain(chunks, biome, x, y, radius):
    ar = 0
    points = stain_points(radius * Config.CHUNK_SIZE, x, y)
    min_x = min(points, key=lambda i: i[0])[0] // Config.CHUNK_SIZE
    max_x = max(points, key=lambda i: i[0])[0] // Config.CHUNK_SIZE
    min_y = min(points, key=lambda i: i[1])[1] // Config.CHUNK_SIZE
    max_y = max(points, key=lambda i: i[1])[1] // Config.CHUNK_SIZE
    max_x = int(min(max_x, len(chunks[0])))
    min_y = int(max(min_y, 0))
    min_x = int(max(min_x, 0))
    max_y = int(min(max_y, len(chunks)))
    # debug_screen = pygame.display.set_mode((len(chunks) * Config.CHUNK_SIZE, len(chunks) * Config.CHUNK_SIZE))
    for c_y in range(min_y, max_y):
        for c_x in range(min_x, max_x):
            if is_inside(chunks[c_y][c_x].x * Config.CHUNK_SIZE, chunks[c_y][c_x].y * Config.CHUNK_SIZE, points):
                chunks[c_y][c_x].biome = biome
                ar += 1
    #             pygame.draw.rect(debug_screen,
    #                              (255, 0, 0),
    #                              pygame.Rect((c_x * Config.CHUNK_SIZE,
    #                                           c_y * Config.CHUNK_SIZE),
    #                                          (Config.CHUNK_SIZE,
    #                                           Config.CHUNK_SIZE)))
    # pygame.draw.polygon(debug_screen, (255, 255, 255), points, 1)
    # pygame.display.update()
    # input()
    return ar


def expansion(chunks, biome, x, y, num):
    if num < 1:
        return
    num -= 1
    move = random.randint(-1, 1)
    new_x = x
    new_y = y
    if (x + move) != x:
        new_x = x + move
        if new_x < 0 or new_x >= len(chunks):
            new_x = x
    else:
        move = random.choice((-1, 1))
        new_y = y + move
        if new_y < 0 or new_y >= len(chunks):
            new_y = y
    chunks[new_y][new_x].biome = biome.value
    expansion(chunks, biome, new_x, new_y, num)


def get_biome_size(biome_type, static_biome_num):
    size = int(random.randint(*Config.biome_percents[biome_type]) / 100 * static_biome_num)
    if size < 1:
        size = 1
    return size


def obj_gen(session):
    return session.query(model.ObjectGen).all()


def procedure_generation(world: model.World):
    with new_session() as session:
        chunks = session.query(model.Chunk).filter(model.Chunk.world_id == world.id).order_by(model.Chunk.y,
                                                                                              model.Chunk.x).all()
        game_world = World.load(world, chunks, [])
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
            expansion(chunks=game_world.chunks, biome=model.Biome.WATER, x=x, y=y, num=water_size)
            game_world.save(session)
        while desert_num > 1:
            desert_num -= stain(chunks=game_world.chunks, biome="desert",
                                x=random.randint(0, world.size * Config.CHUNK_SIZE),
                                y=random.randint(0, world.size * Config.CHUNK_SIZE),
                                radius=math.sqrt(get_biome_size("desert", static_desert_num) / math.pi))
            game_world.save(session)
        while mountains_num > 1:
            mountains_num -= stain(chunks=game_world.chunks, biome="mountains",
                                   x=random.randint(0, world.size * Config.CHUNK_SIZE),
                                   y=random.randint(0, world.size * Config.CHUNK_SIZE),
                                   radius=math.sqrt(get_biome_size("mountains", static_mountains_num) / math.pi))
            game_world.save(session)
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
                                                              c.biome == model.Biome.DESERT.value,
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
    with new_session() as session:
        for gen in obj_gen(session):
            for row in game_world.chunks:
                for chunk in filter(lambda c: c.biome == gen.biome, row):
                    if random.randint(0, 100) <= gen.percent_chunks:
                        for i in range(random.randint(gen.min_num_in_chunk, gen.max_num_in_chunk)):
                            kwargs = json.loads(gen.init_data)
                            obj = vars(game_objects)[gen.cls].generation(chunk, kwargs)
                            chunk.add_obj(obj)
        game_world.save(session)
        session.commit()
