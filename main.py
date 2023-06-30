import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

width = 864
height = 736

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')

# game variables
ground_scroll = 0
scroll_speed = 3

# load img
bg = pygame.image.load('img/bg.png')
ground = pygame.image.load('img/ground.png')

run = True

while run:

    clock.tick(fps)
    screen.blit(bg, (0, 0))

    screen.blit(ground, (ground_scroll, 586))
    ground_scroll -= scroll_speed

    if abs(ground_scroll) > 35:
        ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()
