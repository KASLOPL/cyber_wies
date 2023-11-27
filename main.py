import pygame
import math
from pygame.locals import *
from pygame import mixer

#* Inicjalizacja PyGame
pygame.init()

#* Zmienne globalne
bg = pygame.image.load("background_1.png")
player = pygame.image.load("ball.png")
display = pygame.display.set_mode((800, 800))
blocks = [[pygame.image.load("block.png"), 400, 300], [pygame.image.load("block.png"), 400, 500], [pygame.image.load("block.png"), 500, 200]]
player_x = 400
player_y = 600
vel_x = 5
vel_y = 5
moving = False
friction = 0.98
map = 1

def is_in_block(x, y):
    '''
        #? Funckaj przyjmuje jako argumenty player_x oraz player_y
        #? Funkcja zwraca dystans pomiędzy tymi dwoma punktami bez zaokrąglania
    '''
    for block in blocks:
        if x < block[1] + 50 and x+ 35 > block[1] and y < block[2] + 50 and y + 35 > block[2]:
            return True

def draw_objects():
    '''
        #? Funckaj nie przyjmuje żadnych argumentów oraz nic nie zwraca
        #? Zadaniem tej funkcji jestwyświetlanie wszystkich potrzebnych obiektów na ekran
    '''
    display.blit(bg, (0, 0))
    display.blit(player, (player_x, player_y))
    for block in blocks:
        display.blit(block[0], (block[1], block[2]))

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_start = pygame.mouse.get_pos()
            mouse_down = True
        if event.type == pygame.MOUSEBUTTONUP and mouse_down and not moving:
            mouse_end = pygame.mouse.get_pos()
            dist = (int(round(get_distance(mouse_start, mouse_end), 0))/15)
            if dist > 20:
                power = 20
            else:
                power = dist
            direction = get_direction(mouse_start, mouse_end)
            direction_x = direction[0]
            direction_y = direction[1]
            moving = True
            mouse_down = False
    
    #* Poruszanie się piłeczki 
    #* oraz prosta symulacja tarcia
    if moving:
        player_x += direction_x * power
        player_y += direction_y * power
        power *= friction
        if power<0.1:
            moving = False

    #* Granice pola golfowego (średniowiecze)
    if map == 1:
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
        #todo: Tutaj będą granice pola golfowego dla mapy cyberpunkowej
        pass

    #* Kolizje z blokami postawionymi na mapie
    if moving and is_in_block(player_x + direction_x*power, player_y):
        direction_x *=-1
    if moving and is_in_block(player_x, player_y + direction_y*power):
        direction_y *=-1
        
    draw_objects()

pygame.quit()