import pygame
from sprites import *

HEIGHT = 1080
WIDTH = 1920

sign_texts = {
    0: 'CAUTION! BOULDERS!',
    1: 'CAUTION! BOULDERS!',
    2: 'This is a sign you are very high!',
    3: 'CAUTION! BOULDERS!',
    4: 'DISREGARD CAUTION! NO MORE BOULDERS!'
}
sign0 = Sign_Sprite(sign_texts[0], (200,1010))
sign1 = Sign_Sprite(sign_texts[1], (800,1010))
sign2 = Sign_Sprite(sign_texts[2], (800,100))
sign3 = Sign_Sprite(sign_texts[3], (1400,1010))
sign4 = Sign_Sprite(sign_texts[4], (1700,1010))
signs = [sign0, sign1, sign2, sign3, sign4]

floor1 = Floor((WIDTH/2+100, 32), (WIDTH/4+50, HEIGHT - 42))
floor2 = Floor((WIDTH/3+300, 32), (WIDTH/8*5+164, HEIGHT - 42 - 256 - 5))
floor3 = Floor((WIDTH/2, 32), (WIDTH-100, HEIGHT - 42))
FLOORS = [floor1, floor2, floor3]

tree1 = Tree((32, 369), (WIDTH/8*4, HEIGHT-256/2-32-32-32))
tree2 = Tree((32, 369), (WIDTH/8*6, HEIGHT-256/2-32-32-32))
TREES = [tree1, tree2]

GOAL = Goal_Sprite((1800,1010))

def create_sprite_group(PLAYER):
    level_one_sprites = pygame.sprite.Group()
    level_one_sprites.add(FLOORS)
    level_one_sprites.add(TREES)
    level_one_sprites.add(signs)
    level_one_sprites.add(PLAYER)
    level_one_sprites.add(GOAL)
    return level_one_sprites