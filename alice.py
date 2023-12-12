import pygame
import math
import time
size = 750
pygame.init()
screen = pygame.display.set_mode((size, size))


def y(x):
    try:
        ans = math.tan(x*2) * max(x, size)
        return -ans
    except ZeroDivisionError:
        return 0


for i in range(int(-size/2), int(size/2)):
    pygame.draw.line(surface=screen, color=(255, 255, 255), start_pos=(i-1+size/2, y(i-1)+size/2), end_pos=(i+size/2, y(i)+size/2))
    pygame.display.update()
    time.sleep(0.001)
while True:
    pass
