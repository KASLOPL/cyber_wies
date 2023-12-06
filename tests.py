import pygame
import math
from pygame.locals import *
from pygame import mixer
import maps

# Initialize Pygame
pygame.init()

# Inicjalizacja modułu mixer
pygame.mixer.init()
hit_sound = pygame.mixer.Sound("hit_sound.mp3")
winning_sound = pygame.mixer.Sound("winning_sound.mp3")
pygame.mixer.music.load("backgroundmusic.mp3")
pygame.mixer.music.play(-1)
shots = 0
font = pygame.font.Font(None, 36)
start_font = pygame.font.Font(None, 74)
start_button = pygame.Rect(270, 650, 250, 80)
start_text = start_font.render("", True, (255, 255, 255))
pygame.display.set_caption("MiniGolf: Journey Between Realms") # Nazwa okienka
bg = pygame.image.load("background_1.png") # Ładowanie backgroundu
player = pygame.image.load("ball.png") # Ładowanie piłeczki
hole = pygame.image.load("hole_1.png") # Ładowanie dołeczka
arrow = pygame.image.load("arrow.png") # Ładowanie strzałki
start_screen_bg = pygame.image.load("start_scren.png") # Ładowanie start screana
arrow_rect = arrow.get_rect()
display = pygame.display.set_mode((800, 800)) # Ustawienie wymiarów ekranu
lvl = 1 # Ustawienie levela na 1
blocks_1 , blocks_2, player_cords, hole_cords, where_hole = maps.map(lvl) # Pobieranie informacji o mapie
current = blocks_1 # Ustawienie aktualnie wyświetlanych bloków
player_x, player_y = player_cords # Ustawienie początkowej pozycji gracza na podstawie danych pobranych z pliku "maps"
hole_x, hole_y = hole_cords # Ustawienie pozycji dołka na podstawie danych pobranych z pliku "maps"
moving = False # Deklarowania flagi mówącej czy piłeczka się porusza
friction = 0.98 # Stała oznaczająca wartośc tarcia
world = 1 # Początkowe ustawienie wymiaru w którym znajduje się gracz
mouse_down = False # Flaga oznaczająca to czy lewy przycisk myszy jest wciśnięty
angle = 0 # Kąt pod którym ma się wyświetlać strzałka
space = False # Flaga oznaczająza czy spacja jest wciśnięta
cool_down = 0 # Wartość cool downu
power_meter_width = 14 # Szerokość paska mocy
power_meter_height = 43 # Wysokość paska mocy
power_meter_color1 = (0,0,0) # Kolor tła paska mocy
power_meter_color2 = (255, 255, 255) # Kolor paska mocy
power_bar = 0 # Poziom progresu paska mocy
power = 0 # Moc piłeczki
start_screen = True # Czy start screan jest aktywny
start_screen2 = True # Czy start screan jest aktywny 2
invisible_button_color = (0, 0, 0, 0) # Niewidzialny kolor
button_surface = pygame.Surface((start_button.width, start_button.height), pygame.SRCALPHA) # Przycisk start
button_surface.fill(invisible_button_color) # Kolorowanie przycisku
display.blit(button_surface, (start_button.x, start_button.y)) # Wyświetlanie przycisku
player_x_start = None
player_y_start = None
font = pygame.font.Font(pygame.font.get_default_font(), 36) # do renderowania tekstów w podsumowaniu
instruction = pygame.image.load("instruction.png") # instrukcja gry
end_screen = pygame.image.load("end_screen.png")
while start_screen:
    
    '''
        #? Pętla wyświetlająca start screen i odpowiadająca za przycisk start
    '''

    display.blit(start_screen_bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start_screen = False
        # przejście między startem, a 1 levelem
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if start_button.collidepoint(mouse_pos):
                transition_surface = pygame.Surface((800, 800), pygame.SRCALPHA)
                for alpha in range(0, 256, 8):
                    transition_surface.fill((0, 0, 0, alpha))
                    display.blit(transition_surface, (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(15)
                display.blit(instruction, (0, 0))
                pygame.display.flip()
                pygame.time.delay(5000)
                start_screen = False
                start_screen2 = False
                
    start_text.set_alpha(0)
    display.blit(start_text, (start_button.x + 50, start_button.y + 20))

    pygame.display.flip()
level_start_time = pygame.time.get_ticks()
elapsed_time=0
current_time=0
level_start_time = pygame.time.get_ticks()



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
        #? Zadaniem tej funkcji jest wyświetlanie wszystkich potrzebnych obiektów na ekran
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
    if power_bar>0 and mouse_down:
        pygame.draw.rect(display, power_meter_color1, (player_x+73,player_y-1, power_meter_width, power_meter_height))
        pygame.draw.rect(display, power_meter_color2, (player_x+75,player_y+41-power_bar*2, 10, power_bar*2))

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
level_start_time = pygame.time.get_ticks()
run = True
while run and not start_screen2:
    '''
        #? Główna pętla gry
        #? można ją zakończyć zmieniając zmienną run = False
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        #* Wykrywanie wciskania myszki
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_start = pygame.mouse.get_pos()
            mouse_down = True
        if event.type == pygame.MOUSEBUTTONUP and mouse_down and not moving:
            player_x_start = player_x
            player_y_start = player_y
            shots += 1
            mouse_down = False
            mouse_end = pygame.mouse.get_pos()
            dist = (int(round(get_distance(mouse_start, mouse_end), 0))/15)
            if dist > 20:
                power = 20
                mouse_down = False
            else:
                power = dist/2
            direction = get_direction(mouse_start, mouse_end)
            direction_x = direction[0]
            direction_y = direction[1]
            moving = True
            mouse_down = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_9 and not moving and lvl>1:
            lvl -= 1
            if lvl <=6:
                blocks_1 , blocks_2, player_cords, hole_cords, where_hole = maps.map(lvl)
            transition_surface = pygame.Surface((800, 800), pygame.SRCALPHA)
            for alpha in range(0, 256, 8):
                transition_surface.fill((0, 0, 0, alpha))
                display.blit(transition_surface, (0, 0))
                pygame.display.flip()
                pygame.time.delay(15)
            level_start_time = pygame.time.get_ticks()
            current = blocks_1
            player_x = player_cords[0]
            player_y = player_cords[1]
            player_x, player_y = player_cords
            hole_x, hole_y = hole_cords
            if world == 2:
                world = 1
                current = blocks_1

                bg = pygame.image.load("background_1.png")
                hole = pygame.image.load("hole_.png")
                power_meter_color1 = (0,0,0)
                power_meter_color2 = (255,255,255)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_0 and not moving:
            lvl += 1
            if lvl<=6:
                blocks_1 , blocks_2, player_cords, hole_cords, where_hole = maps.map(lvl)
            transition_surface = pygame.Surface((800, 800), pygame.SRCALPHA)
            for alpha in range(0, 256, 8):
                transition_surface.fill((0, 0, 0, alpha))
                display.blit(transition_surface, (0, 0))
                pygame.display.flip()
                pygame.time.delay(15)
            current = blocks_1
            player_x = player_cords[0]
            player_y = player_cords[1]
            player_x, player_y = player_cords
            hole_x, hole_y = hole_cords
            if world == 2:
                world = 1
                current = blocks_1
                bg = pygame.image.load("background_1.png")
                hole = pygame.image.load("hole_1.png")
                power_meter_color1 = (0,0,0)
                power_meter_color2 = (255,255,255)
        
    #* Mechaniki strzałki
    if mouse_down and not moving:
        mouse = pygame.mouse.get_pos()
        angle = math.degrees(math.atan2(mouse[1] - mouse_start[1], mouse[0] - mouse_start[0]))
        rotated_arrow = pygame.transform.rotate(arrow, -angle-45-180)
        rotated_rect = rotated_arrow.get_rect(center=(player_x+18, player_y+16))
    
    #* Poruszanie się piłeczki 
    #* oraz prosta symulacja tarcia
    if moving:
        mouse_down = False
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
            hit_sound.play()
        if player_x>603:
            direction_x*=-1
            player_x = 603
            hit_sound.play()
        if player_y<55:
            direction_y*=-1
            player_y = 55
            hit_sound.play()
        if player_y>664:
            direction_y*=-1
            player_y = 664
            hit_sound.play()
    else:
        if player_x<214:
            direction_x*=-1
            player_x = 214
            hit_sound.play()
        if player_x>603:
            direction_x*=-1
            player_x = 603
            hit_sound.play()
        if player_y<68:
            direction_y*=-1
            player_y = 68
            hit_sound.play()
        if player_y>672:
            direction_y*=-1
            player_y = 672
            hit_sound.play()

    #* Kolizje z blokami postawionymi na mapie
    if moving and is_in_block(player_x + direction_x*power, player_y):
        direction_x *=-1
        hit_sound.play()
    if moving and is_in_block(player_x, player_y + direction_y*power):
        direction_y *=-1
        hit_sound.play()
    
    #* Trafianie do dołka
    if power <15:
        if world == 1 and where_hole == "middle":
            if get_distance([hole_x+20, hole_y+20], [player_x+17, player_y+17]) < 18:
                moving = False
                lvl += 1
                pygame.mixer.music.stop()
                winning_sound.play()
                if lvl <=6:
                    blocks_1 , blocks_2, player_cords, hole_cords, where_hole = maps.map(lvl)
                current = blocks_1
                player_x = player_cords[0]
                player_y = player_cords[1]
                player_x, player_y = player_cords
                hole_x, hole_y = hole_cords
                transition_surface = pygame.Surface((800, 800), pygame.SRCALPHA)
                for alpha in range(0, 256, 8):
                    transition_surface.fill((0, 0, 0, alpha))
                    display.blit(transition_surface, (0, 0))
                    current_time = pygame.time.get_ticks() - level_start_time
                    seconds = current_time // 1000
                    minutes = seconds // 60
                    seconds %= 60
                    milliseconds = current_time % 1000
                    elapsed_time = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
                    timer_text = font.render("Czas: {}".format(elapsed_time), True, (255, 255, 255))
                    shots_text = font.render("Liczba strzałów: {}".format(shots), True, (255, 255, 255))
                    display.blit(timer_text, (10, 10))
                    display.blit(shots_text, (10, 50))
                    pygame.display.flip()
                    pygame.time.delay(15)
                elapsed_time = 0
                current_time = 0
                shots = 0
                pygame.time.delay(5000)
                pygame.mixer.music.play(-1)
                level_start_time = pygame.time.get_ticks()

        if world == 2 and where_hole == "cyber":
            if get_distance([hole_x+20, hole_y+20], [player_x+17, player_y+17]) < 18:
                moving = False
                lvl += 1
                pygame.mixer.music.stop()
                winning_sound.play()
                blocks_1 , blocks_2, player_cords, hole_cords, where_hole = maps.map(lvl)
                current = blocks_1
                player_x, player_y = player_cords
                hole_x, hole_y = hole_cords
                world = 1
                bg = pygame.image.load("background_1.png")
                hole = pygame.image.load("hole_1.png")
                transition_surface = pygame.Surface((800, 800), pygame.SRCALPHA)
                for alpha in range(0, 256, 8):
                    transition_surface.fill((0, 0, 0, alpha))
                    display.blit(transition_surface, (0, 0))
                    current_time = pygame.time.get_ticks() - level_start_time
                    seconds = current_time // 1000
                    minutes = seconds // 60
                    seconds %= 60
                    milliseconds = current_time % 1000
                    elapsed_time = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
                    timer_text = font.render("Czas: {}".format(elapsed_time), True, (255, 255, 255))
                    shots_text = font.render("Liczba strzałów: {}".format(shots), True, (255, 255, 255))
                    display.blit(timer_text, (10, 10))
                    display.blit(shots_text, (10, 50))
                    pygame.display.flip()
                    pygame.time.delay(15)
                pygame.time.delay(5000)
                pygame.mixer.music.play(-1)
                level_start_time = pygame.time.get_ticks()


                
    
    #* Przemieszczanie się między wymiarami
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not space and not moving:
        space = True
        cool_down = 100
        if world == 1:
            world = 2
            current = blocks_2
            transition_surface = pygame.Surface((800, 800), pygame.SRCALPHA)
            for alpha in range(0, 256, 8):
                    transition_surface.fill((0, 0, 0, alpha))
                    display.blit(transition_surface, (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(15)
            bg = pygame.image.load("background_2.png")
            hole = pygame.image.load("hole_2.png")
            power_meter_color1 = (255,255,255)
            power_meter_color2 = (0,0,0)
        elif world == 2:
            world = 1
            current = blocks_1
            transition_surface = pygame.Surface((800, 800), pygame.SRCALPHA)
            for alpha in range(0, 256, 8):
                transition_surface.fill((0, 0, 0, alpha))
                display.blit(transition_surface, (0, 0))
                pygame.display.flip()
                pygame.time.delay(15)
            bg = pygame.image.load("background_1.png")
            hole = pygame.image.load("hole_1.png")
            power_meter_color1 = (0,0,0)
            power_meter_color2 = (255,255,255)

        if is_in_block(player_x, player_y):
            if not is_in_block(player_x_start, player_y_start):
                player_x = player_x_start
                player_y = player_y_start
            else:
                player_x, player_y = maps.map(lvl)[2]
    
    if cool_down > 0:
        cool_down -= 1
    elif cool_down == 0:
        space = False

    if mouse_down and not moving:
        mouse_bar = pygame.mouse.get_pos()
        power_bar = (int(round(get_distance(mouse_start, mouse_bar), 0))/15)
        if power_bar >20:
            power_bar = 20

    if lvl > 6:
        run = False
    else:
        draw_objects()

display.blit(end_screen, (0, 0))
pygame.display.flip()
pygame.time.delay(30000)

pygame.quit()