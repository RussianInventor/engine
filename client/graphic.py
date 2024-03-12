import os.path
import sys
import time
import pygame
from os import path

import common.world
from common.config import Config

chunk_color = {"field": (0, 200, 0),
               "mountains": path.join("img", "mountain", "Mountain.png"),
               "beach": (250, 250, 0),
               "water": (50, 50, 200),
               "desert": (200, 0, 0),
               "MEGA_MOUNTAINS": path.join("img", "mountain", "Vulcano.png")
               }


class Camera:
    _step = 10

    def __init__(self, x, y, screen_x=None, screen_y=None):
        self.vis_size_w, self.vis_size_h = pygame.display.get_window_size()
        self.scale = Config.scale
        self.x = x
        self.y = y
        self.v_x = 0
        self.v_y = 0
        self.offset_x, self.offset_y = pygame.display.get_window_size()

        self.offset_x = self.offset_x / 2 - self.vis_size_w / 2
        self.offset_y = self.offset_y / 2 - self.vis_size_h / 2

        self.screen_x = screen_x if screen_x is not None else x
        self.screen_y = screen_y if screen_y is not None else y

    def set_scale(self, delta):
        delta = round(delta, 2)
        self.scale += delta
        if self.scale > Config.max_scale:
            self.scale = Config.max_scale
        if self.scale < Config.min_scale:
            self.scale = Config.min_scale

    @property
    def shift_x(self):
        return -self.x

    @property
    def shift_y(self):
        return -self.y

    def pos_shift(self, x, y):
        x = self.offset_x + self.scaled(x - self.x)
        y = self.offset_y + self.scaled(y - self.y)
        return x, y

    @property
    def real_size(self):
        return self.unscaled(self.vis_size_w), self.unscaled(self.vis_size_h)

    def scaled(self, n):
        return self.scale * n

    def unscaled(self, m):
        return m / self.scale

    @property
    def step(self):
        return self._step / self.scale

    def down(self):
        self.v_y = -self.step

    def up(self):
        self.v_y = self.step

    def right(self):
        self.v_x = -self.step

    def left(self):
        self.v_x = self.step

    def move(self):
        self.x += self.v_x
        self.y += self.v_y


class DrawWorld:
    SOURCE = path.join("common", "source")

    def __init__(self, app):
        self.camera = None
        self.app = app
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0))

    def update(self):
        if self.camera is None:
            self.camera = Camera(x=len(self.app.game.world.chunks) / 2,
                                 y=len(self.app.game.world.chunks) / 2)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEWHEEL:
                    self.camera.set_scale(event.y * 0.1)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                        pygame.quit()
                        return
                    if event.key == pygame.K_s:
                        self.camera.down()
                    if event.key == pygame.K_w:
                        self.camera.up()
                    if event.key == pygame.K_d:
                        self.camera.right()
                    if event.key == pygame.K_a:
                        self.camera.left()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_s:
                        self.camera.v_y = 0
                    if event.key == pygame.K_w:
                        self.camera.v_y = 0
                    if event.key == pygame.K_d:
                        self.camera.v_x = 0
                    if event.key == pygame.K_a:
                        self.camera.v_x = 0
            self.screen.fill((0, 0, 0))
            self.camera.move()
            for chunk in self.visible_chunks(self.app.game.world.chunks):
                self.draw_chunk(chunk)
            pygame.draw.rect(self.screen,
                             (255, 0, 0),
                             pygame.Rect(*self.camera.pos_shift(self.camera.x, self.camera.y),
                                         self.camera.vis_size_w,
                                         self.camera.vis_size_h),
                             width=1)
            pygame.display.update()

    def visible_chunks(self, chunks):
        x = self.camera.x // Config.CHUNK_SIZE
        y = self.camera.y // Config.CHUNK_SIZE
        num_x = (self.camera.real_size[0] // Config.CHUNK_SIZE) + 1
        num_y = (self.camera.real_size[1] // Config.CHUNK_SIZE) + 1
        min_x = int(max(0, x))
        min_y = int(max(0, y))
        max_x = int(max(0, min(len(chunks[0]), x + num_x)))
        max_y = int(max(0, min(len(chunks), y + num_y)))
        for row in chunks[min_y: max_y]:
            for chunk in row[min_x: max_x]:
                yield chunk

    def draw_chunk(self, chunk: common.world.Chunk):
        if isinstance(chunk_color[chunk.biome], tuple):
            size = self.camera.scaled(Config.CHUNK_SIZE)
            x, y = self.camera.pos_shift(chunk.x * Config.CHUNK_SIZE, chunk.y * Config.CHUNK_SIZE)
            pygame.draw.rect(self.screen,
                             chunk_color[chunk.biome],
                             pygame.Rect(x, y, size + 1, size + 1),
                             width=0)
        else:
            x, y = chunk.x * Config.CHUNK_SIZE, chunk.y * Config.CHUNK_SIZE
            img = pygame.image.load(path.join(self.SOURCE, chunk_color[chunk.biome]))
            w, h = img.get_size()
            img = pygame.transform.scale(img, (self.camera.scaled(w), self.camera.scaled(h)))
            self.screen.blit(img, self.camera.pos_shift(x, y))
        self.draw_objects(chunk.objs)

    def get_img(self, obj):
        img_path = path.join(self.SOURCE, "img", obj.__class__.__name__.lower(), obj.img_name)
        return pygame.image.load(img_path)

    def draw_objects(self, objs):
        for obj in objs:
            x = obj.x
            y = obj.y
            img = self.get_img(obj)
            w, h = img.get_size()
            img = pygame.transform.scale(img, (self.camera.scaled(w), self.camera.scaled(h)))
            self.screen.blit(img, self.camera.pos_shift(x, y))
