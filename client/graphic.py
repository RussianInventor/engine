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
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.scale = Config.scale

    def pos_shift(self, x, y):
        x = (x - self.x) * self.scale
        y = (y - self.y) * self.scale
        return x, y


class DrawWorld:
    def __init__(self, app):
        self.camera = Camera(x=len(app.game.world.chunks[0]), y=len(app.game.world.chunks))
        self.app = app
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0))

    def update(self):
        while True:
            self.screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEWHEEL:
                    Config.set_scale(event.y*0.1)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()
            self.draw_chunks(self.app.game.world.chunks)
            pygame.display.update()

    def draw_chunks(self, chunks):
        size = (Config.CHUNK_SIZE * self.camera.scale) + 1
        for row in chunks:
            for chu in row:
                pygame.draw.rect(self.screen,
                                 chunk_color[chu.biome],
                                 pygame.Rect(*self.camera.pos_shift(chu.x, chu.y), size, size),
                                 width=0)
