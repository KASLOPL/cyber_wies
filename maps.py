import pygame
def map(lvl):
    if lvl == 1:
        return  [[pygame.image.load("block_1.png"), 400, 300], [pygame.image.load("block_1.png"), 400, 500], [pygame.image.load("block_1.png"), 500, 200], [pygame.image.load("block_1.png"), 220, 100]],\
                [[pygame.image.load("block_2.png"), 450, 200], [pygame.image.load("block_2.png"), 214, 500], [pygame.image.load("block_2.png"), 588, 550], [pygame.image.load("block_2.png"), 214, 300]],\
                [400,600],\
                [400, 100],\
                "middle"
    if lvl == 2:
        pass