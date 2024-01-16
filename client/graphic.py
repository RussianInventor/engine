import pygame
from os import path
from common.config import Config

chunk_color = {"field": (0, 200, 0),
               "mountains": (50, 0, 0),
               "beach": (250, 250, 0),
               "water": (50, 50, 200),
               "desert": (200, 0, 0),
               "MEGA_MOUNTAINS": (0, 0, 0)
               }


class Camera:
    _step = 10
    vis_size = 500

    def __init__(self, x, y, screen_x=None, screen_y=None):
        self.scale = Config.scale
        self.x = x
        self.y = y
        self.offset_x, self.offset_y = pygame.display.get_window_size()
        self.offset_x = self.offset_x / 2 - self.vis_size / 2
        self.offset_y = self.offset_y / 2 - self.vis_size / 2
        self.vis_size = self.scaled(self.vis_size)

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
        x = x + self.shift_x
        y = y + self.shift_y
        return x, y

    @property
    def real_size(self):
        return self.unscaled(self.vis_size)

    def scaled(self, n):
        return self.scale * n

    def unscaled(self, m):
        return m / self.scale

    @property
    def step(self):
        return self._step / self.scale

    def down(self):
        self.y -= self.step

    def up(self):
        self.y += self.step

    def right(self):
        self.x -= self.step

    def left(self):
        self.x += self.step


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
            self.screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEWHEEL:
                    self.camera.set_scale(event.y * 0.1)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                    if event.key == pygame.K_DOWN:
                        self.camera.down()
                    if event.key == pygame.K_UP:
                        self.camera.up()
                    if event.key == pygame.K_RIGHT:
                        self.camera.right()
                    if event.key == pygame.K_LEFT:
                        self.camera.left()

            #for row in self.app.game.world.chunks:
                #for chunk in row:
            for chunk in self.visible_chunks(self.app.game.world.chunks):
                self.draw_chunk(chunk)
            # self.draw_objects(self.app.game.world.objects)
            pygame.draw.rect(self.screen,
                             (255, 0, 0),
                             pygame.Rect(*self.camera.pos_shift(self.camera.x, self.camera.y),
                                         self.camera.vis_size,
                                         self.camera.vis_size),
                             width=1)
            pygame.display.update()

    def visible_chunks(self, chunks):
        x = self.camera.x // Config.CHUNK_SIZE
        y = self.camera.y // Config.CHUNK_SIZE
        num = (self.camera.real_size // Config.CHUNK_SIZE) + 1
        min_x = int(max(0, x))
        min_y = int(max(0, y))
        max_x = int(min(len(chunks[0]), x + num))
        max_y = int(min(len(chunks), y + num))
        for row in chunks[min_y: max_y]:
            for chunk in row[min_x: max_x]:
                yield chunk

    def draw_chunk(self, chunk):
        size = self.camera.scaled(Config.CHUNK_SIZE)
        x, y = self.camera.pos_shift(chunk.x, chunk.y)
        pygame.draw.rect(self.screen,
                         chunk_color[chunk.biome],
                         pygame.Rect(x * size, y * size, size + 1, size + 1),
                         width=0)

    def get_img(self, obj):
        img_path = path.join(self.SOURCE, "img", obj.__class__.__name__.lower(), obj.img_name)
        return pygame.image.load(img_path)

    def draw_objects(self, objs):
        for obj in objs:
            x = obj.x
            y = obj.y
            img = self.get_img(obj)
            self.screen.blit(img, self.camera.pos_shift(x, y))
