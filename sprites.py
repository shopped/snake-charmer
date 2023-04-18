import pygame
vec = pygame.math.Vector2

HEIGHT = 1080
WIDTH = 1920

signSprite = pygame.image.load("sprites/Sign.png")
goalSprite = pygame.image.load("sprites/Goal.png")
knightSprite = pygame.image.load("sprites/Knight.png")
boulderSprite = pygame.image.load("sprites/Boulder.png")
spawnerSprite = pygame.image.load("sprites/Spawner.png")
oldTreeSprite = pygame.image.load("sprites/OldTree.png")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (90, 54, 8)

class Boulder_Spawner_Sprite(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.surf = spawnerSprite
        self.rect = self.surf.get_rect(midbottom= position)
        self.child = Boulder_Sprite(position)
        self.position = position
    def update(self, ds):
        self.child.pos.x -= 16
        if self.child.pos.x < -128:
            self.child.pos = vec(self.position)
        elif self.child.pos.x < 256:
            self.child.bounce = False
        self.child.bounce = not self.child.bounce
        self.child.pos.y += 2 if self.child.bounce else -2
        self.child.rect.midbottom = self.child.pos
        ds.blit(self.child.surf, self.child.rect)


class Boulder_Sprite(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.surf = boulderSprite
        self.bounce = False
        self.rect = self.surf.get_rect(center= position)
        self.pos = vec(position)

    

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

class Knight_Sprite(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.surf = knightSprite
        self.rect = self.surf.get_rect(center= position)
        self.dead = False
        self.bounce = False
        self.pos = vec(position)
    def update(self, snakex, FLOORS):
        if self.dead:
            return
        if self.pos.y > 1300:
            self.dead = True
            return
        on_floor = pygame.sprite.spritecollide(self, FLOORS, False)
        if on_floor:
            self.bounce = not self.bounce
            self.pos.y += 1 if self.bounce else -1
        else:
            self.pos.y += 8
            self.rect.midbottom = self.pos
            return
        if snakex < self.pos.x:
            self.pos.x -= 6
        elif snakex > self.pos.x:
            self.pos.x += 6
        self.rect.midbottom = self.pos



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

class Fader(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.alpha = 255
        self.surf = pygame.Surface((WIDTH, HEIGHT))
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT/2))
        self.FADEOUT = False
        self.NEXT = False
        self.FADEIN = True
        self.WIN = False
        self.LOSE = False

    def display(self, ds):
        self.surf.set_alpha(self.alpha)
        ds.blit(self.surf, self.rect)

    def update(self):
        if self.FADEOUT:
            self.alpha += 8
            if self.alpha >= 255:
                self.FADEOUT = False
                self.NEXT = True
                self.FADEIN = True
        elif self.FADEIN:
            self.NEXT = False
            self.alpha -= 8
            if self.alpha <= 0:
                self.FADEIN = False
                self.WIN = False
                self.LOSE = False

class Time_Overlay(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.ticks = 0
        self.maxticks = None
        self.font = pygame.font.SysFont(None, 99)
        self.surf = self.font.render("00:00", True, BLACK)
        self.rect = self.surf.get_rect(center= (100, 42))
        self.best_time_surf = None
        self.best_time_rect = None

    def reset(self):
        if (self.maxticks is None) or (self.ticks < self.maxticks):
            self.maxticks = self.ticks
            seconds = int(self.ticks / 30)
            m, s = divmod(seconds, 60)
            time_string = '{:02d}:{:02d}'.format(m, s)
            self.best_time_surf = self.font.render("Best - {}".format(time_string), True, BLACK)
            self.best_time_rect = self.best_time_surf.get_rect(center= (200, 100))
        self.ticks = 0
        self.surf = self.font.render("00:00", True, BLACK)

    def display(self, ds):
        self.ticks += 1
        if (self.ticks % 30 == 0):
            seconds = int(self.ticks / 30)
            m, s = divmod(seconds, 60)
            time_string = '{:02d}:{:02d}'.format(m, s)
            self.surf = self.font.render(time_string, True, BLACK)
        ds.blit(self.surf, self.rect)
        if self.maxticks is not None:
            ds.blit(self.best_time_surf, self.best_time_rect)

class Level_Overlay(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.ticks = 0
        self.font = pygame.font.SysFont(None, 99)
        self.surf = self.font.render("Level 1", True, BLACK)
        self.rect = self.surf.get_rect(center= (350, 42))
    
    def update(self, level):
        self.surf = self.font.render("Level {}".format(level), True, BLACK)

class Volume_Overlay(pygame.sprite.Sprite):
    # Will be a volume bar, test with just a blank bar
    def __init__(self):
        super().__init__()
        self.bg = pygame.Surface((256, 64))
        self.bg.fill((0, 0, 0))
        self.rect = self.bg.get_rect(center=(1920-128-24, 42))
    
    def display(self, volume, displaysurface):
        displaysurface.blit(self.bg, self.rect)
        VOL_WIDTH = int(256 * min(1, volume / 2000000))
        self.fg = pygame.Surface((VOL_WIDTH, 64))
        if (volume < 500000):
            self.fg.fill((125, 125, 125))
        else:
            self.fg.fill((255, 255, 255))
        displaysurface.blit(self.fg, self.rect)

noteDict = {'A': 500,
'A#': 550 ,
'B':  600,
'C':  650,
'C#': 700 ,
'D':  750,
'D#': 800 ,
'E':  850,
'F':  900,
'F#': 950 ,
'G':  1000,
'G#': 1050,
}

surf = 'surf'
rect = 'rect'

class Notes_Overlay(pygame.sprite.Sprite):
    # Circle the right one in a different color
    # Also add direction keys to remind the player
    def __init__(self):
        super().__init__()
        self.entities = []
        self.notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.font = pygame.font.SysFont(None, 99)
        self.smfont = pygame.font.SysFont(None, 49)
        self.new_note_x = 550
        self.note_positions = {}

        for note in self.notes:
            new_note = self.font.render(note, True, WHITE if len(note) == 1 else BLACK)
            self.entities.append({surf: new_note, rect: new_note.get_rect(center= (self.new_note_x, 42))})
            self.note_positions[note] = self.new_note_x
            self.new_note_x += 80

        left_text = self.smfont.render("left", True, WHITE)
        self.entities.append({
            surf: left_text,
            rect: left_text.get_rect(center = (self.note_positions['C'], 88))
        })
        right_text = self.smfont.render("right", True, WHITE)
        self.entities.append({
            surf: right_text,
            rect: right_text.get_rect(center = (self.note_positions['A'], 88))
        })
        down_text = self.smfont.render("down", True, WHITE)
        self.entities.append({
            surf: down_text,
            rect: down_text.get_rect(center = (self.note_positions['E'], 88))
        })
        up_text = self.smfont.render("up", True, WHITE)
        self.entities.append({
            surf: up_text,
            rect: up_text.get_rect(center = (self.note_positions['F'], 88))
        })

        self.indicator = pygame.Surface((69, 69))
        self.indicator.fill((255, 255, 0))
    
    def display(self, note, volume, displaysurface):
        if (note != 'x') and (volume > 500000):
            displaysurface.blit(self.indicator, self.indicator.get_rect(center = (self.note_positions[note] , 42)))
        for entity in self.entities:
            displaysurface.blit(entity[surf], entity[rect])