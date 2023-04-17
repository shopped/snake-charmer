import pygame
import sys
import random
from pygame.locals import *
from sprites import *
from Realtime_PyAudio_FFT.stream_analyzer import Stream_Analyzer
import level1, level2, level3, level4

pygame.init()
vec = pygame.math.Vector2

HEIGHT = 1080
WIDTH = 1920
FPS = 30

FramesPecSec = pygame.time.Clock()
ear = Stream_Analyzer(rate   = None, # Audio samplerate, None uses the default source settings
                    FFT_window_size_ms  = 60,    # Window size used for the FFT transform
                    updates_per_second  = 1000,  # How often to read the audio stream for new data
                    smoothing_length_ms = 50)

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Charmer")
restingSprite = pygame.image.load("sprites/RestingSnek2.png")
movingSprite = pygame.image.load("sprites/MovingSnek.png")
movingSprite2 =pygame.image.load("sprites/MovingSnek2.png")
restingSprite2 = pygame.image.load("sprites/RestingSnek.png")

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

    def move(self, note, volume):
        on_floor = pygame.sprite.spritecollide(PLAYER, FLOORS, False)
        on_tree = pygame.sprite.spritecollide(PLAYER, TREES, False)
        on_sign = pygame.sprite.spritecollide(PLAYER, signs, False)
        on_goal = pygame.sprite.spritecollide(PLAYER, [GOAL], False)
        pressed_keys = pygame.key.get_pressed() # for testing only
        # DIR = 'None'
        # if (volume > 500000):
            # if (note == 'C' or note == 'B'):
                # DIR = 'LEFT'
            # elif (note == 'A' or note == 'A#' or note == 'G#'):
                # DIR = 'RIGHT'
            # elif (note == 'F' or note == 'F#'):
                # DIR = 'UP'
            # elif (note == 'E' or note == 'C#'):
                # DIR = 'DOWN'
        if pressed_keys[K_LEFT] and on_floor:
        # if DIR == 'LEFT' and on_floor:
            if on_floor:
                self.vel = (-8,0)
                self.animateMove()
                self.flipped = True
        if pressed_keys[K_RIGHT] and on_floor:
        # elif DIR == 'RIGHT' and on_floor:
                self.vel = (8,0)
                self.animateMove()
                self.flipped = False
        if pressed_keys[K_UP] and on_floor:
        # elif DIR == 'UP' and (on_tree or on_floor):
                self.vel = (0,-8)
                self.surf = restingSpriteF if self.flipped else restingSprite
                self.flipped = not self.flipped
        if pressed_keys[K_DOWN] and on_floor:
        # elif DIR == 'DOWN' and on_tree:
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

        if (self.pos.y > 1200):
            FADER.FADEOUT = True
            FADER.LOSE = True
        elif (on_goal):
            if (not FADER.FADEOUT and not FADER.FADEIN):
                FADER.FADEOUT = True
                FADER.WIN = True

PLAYER = Player()
SIGN_OVERLAY = Sign_Overlay()
TIME_OVERLAY = Time_Overlay()
LEVEL_OVERLAY = Level_Overlay()
VOLUME_OVERLAY = Volume_Overlay()
NOTES_OVERLAY = Notes_Overlay()

FADER = Fader()

all_sprites = level1.create_sprite_group(PLAYER)
FLOORS = level1.FLOORS
TREES = level1.TREES
signs = level1.signs
GOAL = level1.GOAL

all_sprites.add(LEVEL_OVERLAY)

level = 1
def start_next_level():
    global level
    level += 1
    current_level = level1
    if level == 2:
        current_level = level2
    elif level == 3:
        current_level = level3
    elif level == 4:
        current_level = level4
    else:
        level = 1
        TIME_OVERLAY.reset()
        print("Reminder to display the best time")
    LEVEL_OVERLAY.update(level)
    
    global all_sprites
    global FLOORS
    global TREES
    global signs
    global GOAL
    all_sprites = current_level.create_sprite_group(PLAYER)
    all_sprites.add(LEVEL_OVERLAY)
    
    FLOORS = current_level.FLOORS
    TREES = current_level.TREES
    signs = current_level.signs
    GOAL = current_level.GOAL

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    displaysurface.fill((100,100,200))
    audio_data = ear.get_audio_features()

    PLAYER.move(audio_data['note'], audio_data['vol'])
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)

    if SIGN_OVERLAY.visible:
        for entity in SIGN_OVERLAY.entities:
            displaysurface.blit(entity["surf"], entity["rect"])

    TIME_OVERLAY.display(displaysurface)
    NOTES_OVERLAY.display(audio_data['note'], audio_data['vol'], displaysurface)
    VOLUME_OVERLAY.display(audio_data['vol'], displaysurface)

    if FADER.FADEOUT or FADER.FADEIN:
        FADER.display(displaysurface)
        FADER.update()
        if (FADER.NEXT and FADER.LOSE):
            PLAYER.pos = vec((180,1070))
        if (FADER.NEXT and FADER.WIN):
            PLAYER.pos = vec((180,1070))
            start_next_level()

    pygame.display.update()
    FramesPecSec.tick(FPS)