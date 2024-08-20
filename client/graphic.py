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
               "desert": path.join("img", "desert", "desert1.png"),
               "MEGA_MOUNTAINS": path.join("img", "mountain", "Vulcano.png")
               }


class Sprites:
    def __init__(self):
        self.images = {}

    def add_img(self, img, key, scale):
        if self.images.get(scale) is None:
            self.images[scale] = {}
        self.images[scale][key] = img

    def exists(self, scale, key=None):
        if self.images.get(scale) is None:
            return False
        if key is None:
            return len(self.images.get(scale)) > 0
        return self.images.get(scale).get(key) is not None

    def get(self, scale, key):
        try:
            return self.images[scale][key]
        except KeyError:
            return None


class Camera:
    camera_vis = False
    _step = 10

    def __init__(self, x, y, screen_x=None, screen_y=None):
        self.vis_size_w, self.vis_size_h = pygame.display.get_window_size()
        self.scale = Config.scale
        self.x = x
        self.y = y
        self.v_x = 0
        self.v_y = 0
        self.fps = None
        self.offset_x, self.offset_y = pygame.display.get_window_size()

        self.offset_x = self.offset_x / 2 - self.vis_size_w / 2
        self.offset_y = self.offset_y / 2 - self.vis_size_h / 2

        self.screen_x = screen_x if screen_x is not None else x
        self.screen_y = screen_y if screen_y is not None else y

    def show_camera(self, screen):
        pygame.draw.rect(screen,
                         (255, 0, 0),
                         pygame.Rect(*self.pos_shift(self.x, self.y),
                                     self.vis_size_w,
                                     self.vis_size_h),
                         width=1)

    def set_scale(self, scale):
        self.scale = scale

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
        self.v_y = self.step

    def up(self):
        self.v_y = -self.step

    def right(self):
        self.v_x = self.step

    def left(self):
        self.v_x = -self.step

    def move(self):
        self.x += self.v_x
        self.y += self.v_y


class DrawWorld:
    SOURCE = Config.SOURCE

    def __init__(self, app):
        self.camera = None
        self.sprites = None
        self.app = app
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("Consoles", 50)
        self.screen = pygame.display.set_mode((0, 0))

    def show_debug(self, screen):
        txt = self.font.render(f" fps: {self.camera.fps}", 0, [255, 255, 255])
        screen.blit(txt, (5, 5))

    def update(self):
        if self.camera is None:
            self.camera = Camera(x=len(self.app.game.world.chunks) / 2,
                                 y=len(self.app.game.world.chunks) / 2)
            self.sprites = Sprites()
        for scale in Config.scales:
            self.camera.scale = scale
            self.load_img_objects(self.app.game.world._objects.values())
            for row in self.app.game.world.chunks:
                for chunk in row:
                    self.load_img_chunk(chunk)

        while True:
            frame_start = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        Config.scale_index += 1
                        Config.scale_index = min(Config.scale_index, len(Config.scales) - 1)
                    if event.y < 0:
                        Config.scale_index -= 1
                        Config.scale_index = max(Config.scale_index, 0)
                    self.camera.set_scale(Config.scale)
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
            if not self.sprites.exists(scale=self.camera.scale):
                self.load_img_objects(self.app.game.world._objects.values())
                for row in self.app.game.world.chunks:
                    for chunk in row:
                        self.load_img_chunk(chunk)
            self.screen.fill((0, 0, 0))
            self.camera.move()
            for chunk in self.visible_chunks(self.app.game.world.chunks):
                self.draw_chunk(chunk)
            if self.camera.camera_vis:
                self.camera.show_camera(self.screen)
            for chunk in self.visible_chunks(self.app.game.world.chunks):
                for obj in sorted(list(chunk.objects(self.app.game.world)),
                                  key=lambda ob: ob.y):
                    img = self.sprites.get(scale=self.camera.scale,
                                           key=obj.img_key)
                    pos = self.camera.pos_shift(obj.x, obj.y)
                    self.screen.blit(img,
                                     (pos[0] - obj.shift_img_x * img.get_size()[0],
                                      pos[1] - obj.shift_img_y * img.get_size()[1]))
            self.show_debug(self.screen)
            pygame.display.update()
            frame_end = time.time()
            self.camera.fps = int(1 / (frame_end - frame_start))

    def visible_chunks(self, chunks):
        x = self.camera.x // Config.CHUNK_SIZE
        y = self.camera.y // Config.CHUNK_SIZE
        num_x = (self.camera.real_size[0] // Config.CHUNK_SIZE) + 2
        num_y = (self.camera.real_size[1] // Config.CHUNK_SIZE) + 2
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
            img = self.sprites.get(scale=self.camera.scale, key=chunk.img_key)
            self.screen.blit(img, self.camera.pos_shift(x, y))

    def get_img_path(self, obj):
        return path.join(self.SOURCE, "img", obj.__class__.__name__.lower(), obj.img_name)

    def load_img_objects(self, objs):
        for obj in objs:
            img_path = self.get_img_path(obj)
            obj.add_img_key(img_path)
            if self.sprites.exists(key=img_path, scale=self.camera.scale):
                continue
            img = pygame.image.load(img_path)
            w, h = obj.w, obj.h
            img = pygame.transform.scale(img, (self.camera.scaled(w), self.camera.scaled(h)))
            self.sprites.add_img(img=img, scale=self.camera.scale, key=img_path)

    def load_img_chunk(self, chunk):
        if isinstance(chunk_color[chunk.biome], tuple):
            return
        img_path = path.join(self.SOURCE, chunk_color[chunk.biome])
        img = pygame.image.load(img_path)
        w, h = Config.CHUNK_SIZE, Config.CHUNK_SIZE
        img = pygame.transform.scale(img, (self.camera.scaled(w)+1, self.camera.scaled(h)+1))
        self.sprites.add_img(img=img, scale=self.camera.scale, key=img_path)
        chunk.add_img_key(img_path)
