import pygame
import sys
import random
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2

HEIGHT = 1080
WIDTH = 1920
FPS = 30

FramesPecSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Charmer")
restingSprite = pygame.image.load("sprites/RestingSnek2.png")
movingSprite = pygame.image.load("sprites/MovingSnek.png")
movingSprite2 =pygame.image.load("sprites/MovingSnek2.png")
restingSprite2 = pygame.image.load("sprites/RestingSnek.png")
signSprite = pygame.image.load("sprites/Sign.png")
goalSprite = pygame.image.load("sprites/Goal.png")

restingSpriteF = pygame.transform.flip(restingSprite, True, False)
movingSpriteF = pygame.transform.flip(movingSprite, True, False)
movingSprite2F = pygame.transform.flip(movingSprite2, True, False)
restingSprite2F = pygame.transform.flip(restingSprite2, True, False)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = restingSprite
        self.rect = self.surf.get_rect(center= (10,420))

        self.pos = vec((180,1070))
        self.vel = vec(0,0)
        self.flipped = False
        self.moveToggle = False

    def animateMove(self):
        if self.moveToggle:
            self.surf = movingSpriteF if self.flipped else movingSprite
            self.moveToggle = False
        else:
            self.surf = movingSprite2F if self.flipped else movingSprite2
            self.moveToggle = True

    def move(self):
        on_floor = pygame.sprite.spritecollide(PLAYER, FLOORS, False)
        on_tree = pygame.sprite.spritecollide(PLAYER, TREES, False)
        on_sign = pygame.sprite.spritecollide(PLAYER, signs, False)
        pressed_keys = pygame.key.get_pressed() # for testing only
        if pressed_keys[K_LEFT] and on_floor:
            if on_floor:
                self.vel = (-8,0)
                self.animateMove()
                self.flipped = True
        elif pressed_keys[K_RIGHT] and on_floor:
                self.vel = (8,0)
                self.animateMove()
                self.flipped = False
        elif pressed_keys[K_UP] and (on_tree or on_floor):
                self.vel = (0,-8)
                self.surf = restingSpriteF if self.flipped else restingSprite
                self.flipped = not self.flipped
        elif pressed_keys[K_DOWN] and on_tree:
            if on_tree:
                self.vel = (0,8)
                self.surf = restingSpriteF if self.flipped else restingSprite
                self.flipped = not self.flipped
        else:
            self.vel = (0,0)
            self.moveToggle = False
            if random.randint(0, 100) == 0:
                self.surf = restingSprite2F if self.flipped else restingSprite2
            else:
                self.surf = restingSpriteF if self.flipped else restingSprite

        if not on_floor and not on_tree:
            self.vel = (0, 8)

        if on_sign:
            SIGN_OVERLAY.change_text(on_sign[0].text)
            SIGN_OVERLAY.visible = True
        else:
            SIGN_OVERLAY.visible = False
           
        self.pos += self.vel
        self.rect.midbottom = self.pos

BLACK = (0, 0, 0)
BROWN = (90, 54, 8)

class Sign_Sprite(pygame.sprite.Sprite):
    def __init__(self, text, position):
        super().__init__()
        self.surf = signSprite
        self.text = text
        self.rect = self.surf.get_rect(center= position)

class Goal_Sprite(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.surf = goalSprite
        self.rect = self.surf.get_rect(center= position)


class Sign_Overlay(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont(None, 99)
        self.visible = True
        self.entities = []
        self.change_text("Hello World!")
    
    def change_text(self, display_text):
        self.entities = []
        bg = pygame.Surface((WIDTH/2, HEIGHT/2))
        bg.fill(BROWN)
        bg_rect = bg.get_rect(center = (WIDTH/2, HEIGHT / 2))
        self.entities.append({"surf": bg, "rect": bg_rect})
        text_array = display_text.split(' ')
        current_line = ""
        text_x = WIDTH/4 + 42
        text_y = HEIGHT/4 + 42
        for word in text_array:
            if len(current_line) > 0:
                current_line = current_line + " " + word
            else:
                current_line = word
            if len(current_line) >= 15:
                text_line = self.font.render(current_line, True, BLACK)
                text_pos = (text_x, text_y)
                self.entities.append({"surf": text_line, "rect": text_pos})
                text_y += 84
                current_line = ""
        if len(current_line) > 0:
            text_line = self.font.render(current_line, True, BLACK)
            self.entities.append({"surf": text_line, "rect": (text_x, text_y)})
            current_line = ""

class Floor(pygame.sprite.Sprite):
    def __init__(self, size, pos):
        super().__init__()
        self.surf = pygame.Surface(size)
        self.surf.fill((150, 75, 0))
        self.rect = self.surf.get_rect(center=pos)



class Tree(pygame.sprite.Sprite):
    def __init__(self, size, pos):
        super().__init__()
        self.surf = pygame.Surface(size)
        self.surf.fill((150, 75, 0))
        self.rect = self.surf.get_rect(center=pos)

PLAYER = Player()
SIGN_OVERLAY = Sign_Overlay()

sign_texts = {
    0: 'You can play an A note to move left. Try playing a C note to move right.',
    1: 'Welcome to snake charmer! Play a C note into your microphone to proceed forward',
    2: 'Snakes cannot see well, so you need to be touching a sign to read it',
    3: 'Did you know you can play an A note to move left?',
    4: 'Play E/F notes to climb up and down a tree',
    5: 'Good job! Keep going!',
    6: 'Your job as a python is to search for the holy grail. Try to get all 4 as fast as possible!',
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

all_sprites = pygame.sprite.Group()
all_sprites.add(FLOORS)
all_sprites.add(TREES)
all_sprites.add(signs)
all_sprites.add(PLAYER)
all_sprites.add(GOAL)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    displaysurface.fill((100,100,200))

    PLAYER.move()
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)

    if SIGN_OVERLAY.visible:
        for entity in SIGN_OVERLAY.entities:
            displaysurface.blit(entity["surf"], entity["rect"])

    pygame.display.update()
    FramesPecSec.tick(FPS)