import pygame
def map(lvl):
    if lvl == 1:
        return  [[pygame.image.load("block_1.png"), 220, 300], [pygame.image.load("block_1.png"), 270, 300], [pygame.image.load("block_1.png"), 320, 300], [pygame.image.load("block_1.png"), 370, 300], [pygame.image.load("block_1.png"), 420, 300], [pygame.image.load("block_1.png"), 470, 300], [pygame.image.load("block_1.png"), 520, 300], [pygame.image.load("block_1.png"), 570, 300], [pygame.image.load("block_1.png"), 590, 300]],\
                [],\
                [400,600],\
                [400, 100],\
                "middle"
    if lvl == 2:
        return  [[pygame.image.load("block_1.png"), 219, 566], [pygame.image.load("block_1.png"), 269, 566], [pygame.image.load("block_1.png"), 319, 566], [pygame.image.load("block_1.png"), 369, 566], [pygame.image.load("block_1.png"), 419, 566], [pygame.image.load("block_1.png"), 469, 566], [pygame.image.load("block_1.png"), 519, 566], [pygame.image.load("block_1.png"), 569, 566], [pygame.image.load("block_1.png"), 590, 566],  [pygame.image.load("block_1.png"), 368, 516], [pygame.image.load("block_1.png"), 368, 466], [pygame.image.load("block_1.png"), 368, 416], [pygame.image.load("block_1.png"), 468, 416], [pygame.image.load("block_1.png"), 468, 466], [pygame.image.load("block_1.png"), 468, 516]],\
                [[pygame.image.load("block_2.png"), 219, 566], [pygame.image.load("block_2.png"), 269, 566], [pygame.image.load("block_2.png"), 319, 566], [pygame.image.load("block_2.png"), 369, 566], [pygame.image.load("block_2.png"), 419, 416], [pygame.image.load("block_2.png"), 469, 566], [pygame.image.load("block_2.png"), 519, 566], [pygame.image.load("block_2.png"), 569, 566], [pygame.image.load("block_2.png"), 590, 566],  [pygame.image.load("block_2.png"), 368, 516], [pygame.image.load("block_2.png"), 368, 466], [pygame.image.load("block_2.png"), 368, 416], [pygame.image.load("block_2.png"), 468, 416], [pygame.image.load("block_2.png"), 468, 466], [pygame.image.load("block_2.png"), 468, 516]],\
                [400,650],\
                [400, 100],\
                "middle"