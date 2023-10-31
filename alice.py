import pygame
import random

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

ball = pygame.image.load('ball.png')
paddle_l = pygame.image.load('paddle_l.png')
paddle_r = paddle_l

def draw_window():
    screen.blit(paddle_l, (0, 0))
    screen.blit(paddle_r, (639, 0))

    pygame.draw.rect(screen, (255, 255, 255), (5, 5, 150, 10))
    pygame.draw.rect(screen, (255, 0, 255), (629, 5, 150, 10))

run = True


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_l.get_rect().x > 5:
            paddle_l.set_rect(pygame.Rect(paddle_l.get_rect().left - 5,
                                          paddle_l.get_rect().top,
                                          paddle_l.get_rect().width,
                                          paddle_l.get_rect().height))
        elif keys[pygame.K_RIGHT] and paddle_r.get_rect().x < 634:
            paddle_r.set_rect(pygame.Rect(paddle_r.get_rect().right - 5,
                                          paddle_r.get_rect().top,
                                          paddle_r.get_rect().width,
                                          paddle_r.get_rect().height))
pos = ball.get_rect(center=(320, 240))
vel = vec(3, 3)

hits = 0
while hits < 20:
    pos.move_ip(vel)
    dx, dy = pos.get_size() / 2
    if 0 < dx <= 310 and dx >= -310:
        if (dx < 0 and pos.top > paddle_r.get_rect().bottom) or \
           (dx > 0 and pos.bottom < paddle_r.get_rect().top):
            vel.x *= -1
        if pos.collidelight(paddle_r):
            hits += 1
    else:
        vel.x *= 0.9

    if 0 < dy <= 160 and dy >= -160:
        if (dy < 0 and pos.right > paddle_l.get_rect().left) or \
        (dy > 0 and pos.left < paddle_l.get_rect().right):
            vel.y *= -1

        if pos.collidelight(paddle_l):
            hits += 1
    else:
        vel.y *= 0.9
    draw_window()
    clock.tick(60)
pygame.quit()