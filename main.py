import pygame
from pygame.locals import *
from pygame import mixer

#inicjalizacja pygame
pygame.init()

bg = pygame.image.load("background.png")
display = pygame.display.set_mode((800, 800))

def draw_objects():
    display.blit(bg, (0, 0))

    pygame.display.update()

while True:

    draw_objects()