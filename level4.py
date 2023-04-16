import pygame
from sprites import *

HEIGHT = 1080
WIDTH = 1920

sign_texts = {
    0: 'Some trees here are tricky and wont let you climb',
    1: '*hint* 1248->1248->1248->1248->1248', #0001->1000->0101->1010->0111
    2: 'The secret code is binary',
    3: 'Did you know, there are over 32,000 combinations for this level?',
    5: 'Also I randomly generate it, so you cannot cheat',
    6: 'You can always look at the source code if you are stuck, but at this point you probably do not need it',
    7: 'I hope you wrote down the hint at this point! Or you remember what it was',
    8: 'Great job! See if you can beat your best time. Completing this final level will reset you back to the beginning',
    9: 'Thank you for playing, I hope you enjoyed the game!'
}
sign0 = Sign_Sprite(sign_texts[0], (200,1010))
signs = [sign0]

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