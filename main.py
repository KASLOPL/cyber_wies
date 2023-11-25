import pygame
from pygame.locals import *
from pygame import mixer

#inicjalizacja pygame
pygame.init()

bg = pygame.image.load("background.png")
player = pygame.image.load("ball.png")
display = pygame.display.set_mode((800, 800))
player_x = 400
player_y = 600
vel_x = 5

def draw_objects():
    display.blit(bg, (0, 0))
    display.blit(player, (player_x, player_y))

    pygame.display.update()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_x > 0:
        player_x -= vel_x
    if keys[pygame.K_d] and player_x < 765:
        player_x += vel_x

    draw_objects()