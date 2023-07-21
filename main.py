import pygame
from pygame.locals import *
import random

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
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency

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
        self.vel = 0
        self.clicked = False

    def update(self):

        # gravity
        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
                print(self.vel)
            if self.rect.bottom < 586:
                self.rect.y += int(self.vel)

        if game_over == False:
            # jumping
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # handle the animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        # position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
flappy = Bird(100, int(height / 2))

bird_group.add(flappy)

run = True

while run:

    clock.tick(fps)
    # background
    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()

    pipe_group.draw(screen)


    # draw the ground
    screen.blit(ground, (ground_scroll, 586))

    # check for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    # check if bird hit the ground
    if flappy.rect.bottom >= 586:
        game_over = True
        flying = False

    if game_over == False and flying == True:
        # generating new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            bottom_pipe = Pipe(width, int(height / 2) + pipe_height, -1)
            top_pipe = Pipe(width, int(height / 2) + pipe_height, 1)
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
        # ground
        ground_scroll -= scroll_speed
        # creating infinite loop for the ground
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()
pygame.quit()
