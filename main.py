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
flying = False
game_over = False

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

    # draw the ground
    screen.blit(ground, (ground_scroll, 586))

    # check if bird hit the ground
    if flappy.rect.bottom > 586:
        game_over = True
        flying = False

    # ground
    if game_over == False:
        ground_scroll -= scroll_speed
        # creating infinite loop for the ground
        if abs(ground_scroll) > 35:
            ground_scroll = 0

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()
pygame.quit()
