import pygame
from sprites import *

HEIGHT = 1080
WIDTH = 1920

position = (400,HEIGHT/3*2 - 42)

sign_texts = {
    0: 'Beware the Knight of Night!',
    1: 'Why dont you C what happens *hint* *hint*',
    2: 'Beware th-',
}
sign0 = Sign_Sprite(sign_texts[0], (500,HEIGHT/3*2 - 62))
sign1 = Sign_Sprite(sign_texts[1], (1600,HEIGHT/3 - 62))
sign2 = Sign_Sprite(sign_texts[2], (400,HEIGHT - 62))
signs = [sign0, sign1, sign2]

floor1 = Floor((WIDTH - 400, 32), (WIDTH/2+150, HEIGHT - 42))
floor2 = Floor((WIDTH - 550, 32), (WIDTH/2+100, HEIGHT/3*2 - 42))
floor3 = Floor((WIDTH - 200, 32), (WIDTH/2, HEIGHT/3 - 42))
FLOORS = [floor1, floor2, floor3]

tree1 = Tree((32, 369), (WIDTH/8*4, HEIGHT-256/2-32-32-38))
tree2 = Tree((32, 369), (WIDTH/8*6, HEIGHT-256/2-32-32-38))
tree3 = Tree((32, 369), (WIDTH/8*2, HEIGHT-256/2-32-32-38))
tree4 = Tree((32, 369), (WIDTH/8*6-150, HEIGHT-369/2-HEIGHT/3-48))
TREES = [tree1, tree2, tree3, tree4]

KNIGHT = Knight_Sprite((1000,1040))
GOAL = Goal_Sprite((1800,1010))

def reset_knight():
    KNIGHT.pos = vec(1000,1010)
    KNIGHT.dead = False

def create_sprite_group(PLAYER):
    reset_knight()
    level_sprites = pygame.sprite.Group()
    level_sprites.add(FLOORS)
    level_sprites.add(TREES)
    level_sprites.add(signs)
    level_sprites.add(PLAYER)
    level_sprites.add(GOAL)
    level_sprites.add(KNIGHT)
    return level_sprites