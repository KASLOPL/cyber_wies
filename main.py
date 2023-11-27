import pygame
import math
from pygame.locals import *
from pygame import mixer

#inicjalizacja pygame
pygame.init()

bg = pygame.image.load("background_1.png")
player = pygame.image.load("ball.png")
display = pygame.display.set_mode((800, 800))
player_x = 400
player_y = 600
vel_x = 5
vel_y = 5
moving = False
friction = 0.98

def draw_objects():
    display.blit(bg, (0, 0))
    display.blit(player, (player_x, player_y))

    pygame.display.update()

def get_distance(mouse_start, mouse_end):
    return math.sqrt((mouse_end[0] - mouse_start[0]) ** 2 + (mouse_end[1] - mouse_start[1]) ** 2)

def get_angle(mouse_start, mouse_end):
    side_a = int(math.fabs(mouse_end[0] - mouse_start[0]))
    side_b = int(math.fabs(mouse_end[1] - mouse_start[1]))
    if mouse_end[0]<mouse_start[0]:
        section = "L"
    else:
        section = "R"
    if mouse_end[1]<mouse_start[1]:
        section += "U"
    else:
        section += "D"
    return math.atan2(side_b, side_a), section

def get_direction(mouse_start, mouse_end):
    angle = get_angle(mouse_start, mouse_end)
    if angle[1] == "LU":
        return math.cos(angle[0]), math.sin(angle[0])
    if angle[1] == "LD":
        return math.cos(angle[0]),-1* math.sin(angle[0])
    if angle[1] == "RU":
        return -1* math.cos(angle[0]), math.sin(angle[0])
    if angle[1] == "RD":
        return -1* math.cos(angle[0]), -1* math.sin(angle[0])

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_start = pygame.mouse.get_pos()
            print(mouse_start)
            mouse_down = True
        if event.type == pygame.MOUSEBUTTONUP and mouse_down and not moving:
            mouse_end = pygame.mouse.get_pos()
            dist = (int(round(get_distance(mouse_start, mouse_end), 0))/15)
            power = dist
            direction = get_direction(mouse_start, mouse_end)
            direction_x = direction[0]
            direction_y = direction[1]
            moving = True
            mouse_down = False
    
    if moving:
        player_x += direction_x * power
        player_y += direction_y * power
        power *= friction
        if power<0.1:
            moving = False
    
    if player_x<220:
        direction_x*=-1
    if player_x>595:
        direction_x*=-1
    if player_y<63:
        direction_y*=-1
    if player_y>652:
        direction_y*=-1


    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        direction = 0,0
    draw_objects()

pygame.quit()