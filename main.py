import pygame
from pygame.locals import *

pygame.init()

# giving time to scrolling
clock = pygame.time.Clock()
fps = 60

# setting the screen properties
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


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        # handle the animation
        self.counter += 1
        flap_cooldown = 45

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]


bird_group = pygame.sprite.Group()

flappy = Bird(100, int(height / 2))

bird_group.add(flappy)

run = True

while run:

    clock.tick(fps)
    # background
    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()

    # ground
    screen.blit(ground, (ground_scroll, 586))
    ground_scroll -= scroll_speed

    # creating infinite loop for the ground
    if abs(ground_scroll) > 35:
        ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()
