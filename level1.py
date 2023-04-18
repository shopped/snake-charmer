import pygame
from sprites import *

HEIGHT = 1080
WIDTH = 1920

position = (180,1050)

sign_texts = {
    0: 'You can play an C note to move left. Try playing a A note to move right.',
    1: 'Welcome to snake charmer! Play the A note into your microphone to proceed forward',
    2: 'Snakes cannot see well, so you need to be touching a sign to read it',
    3: 'Did you know you can play a C note to move left?',
    4: 'Play E/F notes to climb up and down a tree',
    5: 'Good job! Keep going!',
    6: 'Your job as a python is to search for the holy grail. Try to get all 3 as fast as possible!',
    'x': 'Easter egg. Good job.'
}
sign0 = Sign_Sprite(sign_texts[0], (20,1010))
sign1 = Sign_Sprite(sign_texts[1], (200,1010))
sign2 = Sign_Sprite(sign_texts[2], (420,1010))
sign3 = Sign_Sprite(sign_texts[3], (700,1010))
sign4 = Sign_Sprite(sign_texts[4], (900,1010))
sign5 = Sign_Sprite(sign_texts[5], (WIDTH/8*5, HEIGHT - 42 - 256 - 24))
sign6 = Sign_Sprite(sign_texts[6], (1600,1010))
signx = Sign_Sprite(sign_texts['x'], (2000,1010))
signs = [sign0, sign1, sign2, sign3, sign4, sign5, sign6, signx]

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