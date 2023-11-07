import pygame
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
    size = 100

    def __init__(self, x, y, screen_x=None, screen_y=None):
        self.scale = Config.scale
        self.x = x
        self.y = y
        self.size = self.scaled(self.size)

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

    def scaled(self, n):
        return self.scale * n

    @property
    def step(self):
        return self._step/self.scale

    def down(self):
        self.y -= self.step

    def up(self):
        self.y += self.step

    def right(self):
        self.x -= self.step

    def left(self):
        self.x += self.step


class DrawWorld:
    def __init__(self, app):
        self.camera = None
        self.app = app
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0))

    def update(self):
        self.camera = Camera(x=len(self.app.game.world.chunks)/2,
                             y=len(self.app.game.world.chunks)/2)
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

            self.draw_chunks(self.app.game.world.chunks)
            pygame.display.update()

    def draw_chunks(self, chunks):
        size = self.camera.scaled(Config.CHUNK_SIZE)
        for row in chunks:
            for chu in row:
                x, y = self.camera.pos_shift(chu.x, chu.y)
                pygame.draw.rect(self.screen,
                                 chunk_color[chu.biome],
                                 pygame.Rect(x*size, y*size, size+1, size+1),
                                 width=0)
