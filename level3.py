import pygame
from sprites import *

HEIGHT = 1080
WIDTH = 1920

position = (300,1050)

sign_texts = {
    0: 'CAUTION! BOULDERS!',
    1: 'CAUTION! BOULDERS!',
    2: 'This is a sign you are very high!',
    3: 'DISREGARD CAUTION! NO MORE BOULDERS!'
}
sign0 = Sign_Sprite(sign_texts[0], (500,1010))
sign1 = Sign_Sprite(sign_texts[1], (800,HEIGHT/4*3 - 42 - 28))
sign2 = Sign_Sprite(sign_texts[2], (1400,HEIGHT/4 - 42 - 28))
sign3 = Sign_Sprite(sign_texts[3], (1400,1010))
signs = [sign0, sign1, sign2, sign3]

floor1 = Floor((WIDTH/6, 32), (WIDTH/6 + 100, HEIGHT - 42))
floor2 = Floor((WIDTH/6, 32), (WIDTH - WIDTH/6 - 100, HEIGHT - 42))
floor3 = Floor((WIDTH - 400, 32), (WIDTH/2, HEIGHT/4*3 - 42))
floor4 = Floor((WIDTH - 400, 32), (WIDTH/2, HEIGHT/4*2 - 42))
floor5 = Floor((WIDTH/6, 32), (WIDTH/3, HEIGHT/4 - 42))
floor6 = Floor((WIDTH/6, 32), (WIDTH/3*2, HEIGHT/4 - 42))
FLOORS = [floor1, floor2, floor3, floor4, floor5, floor6]

tree1 = Tree((32, 369), (WIDTH/8*2, HEIGHT-256/2-32-32-32))
tree2 = Tree((32, 369), (WIDTH/8*6, HEIGHT-256/2-32-32-32))
tree3 = Tree((32, 369), (WIDTH/8*3, HEIGHT/2+100))
tree4 = Tree((32, 369), (WIDTH/8*5, HEIGHT/2+100))
tree5 = Tree((32, 369), (WIDTH/8*3-100, 356))
tree6 = Tree((32, 369), (WIDTH/8*5+100, 356))
tree7 = Tree((32, 369), (WIDTH/2, 356))
TREES = [tree1, tree2, tree3, tree4, tree5, tree6, tree7]

spawner1 = Boulder_Spawner_Sprite((1600, HEIGHT/4*3 - 42))
spawner2 = Boulder_Spawner_Sprite((1500, HEIGHT/4*2 - 42))
SPAWNERS = [spawner1, spawner2]

GOAL = Goal_Sprite((WIDTH-300,1010))

def create_sprite_group(PLAYER):
    level_one_sprites = pygame.sprite.Group()
    level_one_sprites.add(FLOORS)
    level_one_sprites.add(TREES)
    level_one_sprites.add(signs)
    level_one_sprites.add(PLAYER)
    level_one_sprites.add(GOAL)
    level_one_sprites.add(SPAWNERS)
    return level_one_sprites