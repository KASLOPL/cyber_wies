import pygame
import math
from pygame.locals import *
from pygame import mixer
import maps

#* Inicjalizacja PyGame
pygame.init()

#* Zmienne globalne
bg = pygame.image.load("background_1.png")
player = pygame.image.load("ball.png")
hole = pygame.image.load("hole.png")
arrow = pygame.image.load("arrow.png")
arrow_rect = arrow.get_rect()
display = pygame.display.set_mode((800, 800))
lvl = 1
blocks_1 , blocks_2, player_cords, hole_cords, where_hole = maps.map(lvl)
current = blocks_1
player_x, player_y = player_cords
hole_x, hole_y = hole_cords
vel_x = 5
vel_y = 5
moving = False
friction = 0.98
world = 1
mouse_down = False
angle = 0
space = False
cool_down = 0

def is_in_block(x, y):
    '''
        #? Funckaj przyjmuje jako argumenty player_x oraz player_y
        #? Funkcja zwraca dystans pomiędzy tymi dwoma punktami bez zaokrąglania
    '''
    for block in current:
        if x < block[1] + 50 and x+ 35 > block[1] and y < block[2] + 50 and y + 35 > block[2]:
            return True

def draw_objects():
    '''
        #? Funckaj nie przyjmuje żadnych argumentów oraz nic nie zwraca
        #? Zadaniem tej funkcji jestwyświetlanie wszystkich potrzebnych obiektów na ekran
    '''
    display.blit(bg, (0, 0))
    if world == 1 and where_hole == "middle":
        display.blit(hole, (hole_x, hole_y))
    if world == 2 and where_hole == "cyber":
        display.blit(hole, (hole_x, hole_y))
    display.blit(player, (player_x, player_y))
    for block in current:
        display.blit(block[0], (block[1], block[2]))
    if mouse_down and not moving:
        display.blit(rotated_arrow, rotated_rect.topleft)
    
    pygame.display.update()

def get_distance(mouse_start, mouse_end):
    '''
        #? Funckaj przyjmuje jako argumenty dwa tuple 
        #! mouse_start -> koordynaty myszki w momencie kliknięcia myszki
        #! mouse_end -> koordynaty myszki w momęcie puszczenia myszki
        #? Funkcja zwraca dystans pomiędzy tymi dwoma punktami bez zaokrąglania
    '''
    return math.sqrt((mouse_end[0] - mouse_start[0]) ** 2 + (mouse_end[1] - mouse_start[1]) ** 2)

def get_angle(mouse_start, mouse_end):
    '''
        #? Funckaj przyjmuje jako argumenty dwa tuple 
        #! mouse_start -> koordynaty myszki w momencie kliknięcia myszki
        #! mouse_end -> koordynaty myszki w momęcie puszczenia myszki
        #? Funkcja zwraca tupla zawierającego kąt w radnianach oraz sekcje w której znajduje się myszka
        #? sekcje oznaczone są literami:
        #! "L" i "R" oznaczające left i right
        #! "U" i "D" oznaczające up i down
    '''

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
    '''
        #? Funckaj przyjmuje jako argumenty dwa tuple 
        #! mouse_start -> koordynaty myszki w momencie kliknięcia myszki
        #! mouse_end -> koordynaty myszki w momęcie puszczenia myszki
        #? Funkcja zwraca tupla zawierającego ilość pikseli do pokonania w osi x oraz osi y dla obliczonego kąta
    '''

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
    '''
        #? Główna pętla gry
        #? można ją zakończyć zmieniając zmienną run = False
    '''
    #* Wykrywanie wciskania myszki
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_start = pygame.mouse.get_pos()
            mouse_down = True
        if event.type == pygame.MOUSEBUTTONUP and mouse_down and not moving:
            mouse_down = False
            mouse_end = pygame.mouse.get_pos()
            dist = (int(round(get_distance(mouse_start, mouse_end), 0))/15)
            if dist > 20:
                power = 20
                mouse_down = False
            else:
                power = dist
            direction = get_direction(mouse_start, mouse_end)
            direction_x = direction[0]
            direction_y = direction[1]
            moving = True
            mouse_down = False
    
    #* Mechaniki strzałki
    if mouse_down and not moving:
        mouse = pygame.mouse.get_pos()
        angle = math.degrees(math.atan2(mouse[1] - mouse_start[1], mouse[0] - mouse_start[0]))
        rotated_arrow = pygame.transform.rotate(arrow, -angle-45-180)
        rotated_rect = rotated_arrow.get_rect(center=(player_x+18, player_y+16))
    
    #* Poruszanie się piłeczki 
    #* oraz prosta symulacja tarcia
    if moving:
        player_x += direction_x * power
        player_y += direction_y * power
        power *= friction
        if power<0.1:
            moving = False

    #* Granice pola golfowego
    if world == 1:
        if player_x<220:
            direction_x*=-1
            player_x = 220
        if player_x>603:
            direction_x*=-1
            player_x = 603
        if player_y<55:
            direction_y*=-1
            player_y = 55
        if player_y>664:
            direction_y*=-1
            player_y = 664
    else:
        if player_x<214:
            direction_x*=-1
            player_x = 214
        if player_x>603:
            direction_x*=-1
            player_x = 603
        if player_y<68:
            direction_y*=-1
            player_y = 68
        if player_y>672:
            direction_y*=-1
            player_y = 672

    #* Kolizje z blokami postawionymi na mapie
    if moving and is_in_block(player_x + direction_x*power, player_y):
        direction_x *=-1
    if moving and is_in_block(player_x, player_y + direction_y*power):
        direction_y *=-1
    
    #* Trafianie do dołka
    if world == 1 and where_hole == "middle":
        if get_distance([hole_x+20, hole_y+20], [player_x+17, player_y+17]) < 18:
            moving = False
            lvl += 1
            blocks_1 , blocks_2, player_cords, hole_cords = maps.map(lvl)
            player_x = 400
            player_y = 600
    if world == 2 and where_hole == "cyber":
        if get_distance([hole_x+20, hole_y+20], [player_x+17, player_y+17]) < 18:
            moving = False
            lvl += 1
            blocks_1 , blocks_2, player_cords, hole_cords = maps.map(lvl)
            player_x = 400
            player_y = 600
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not space and not moving:
        space = True
        cool_down = 100
        if world == 1:
            world = 2
            current = blocks_2
            bg = pygame.image.load("background_2.png")
            hole = pygame.image.load("hole_2.png")
        elif world == 2:
            world = 1
            current = blocks_1
            bg = pygame.image.load("background_1.png")
            hole = pygame.image.load("hole.png")
    
    if cool_down > 0:
        cool_down -= 1
    elif cool_down == 0:
        space = False

    draw_objects()

pygame.quit()