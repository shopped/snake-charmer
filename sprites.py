import pygame

HEIGHT = 1080
WIDTH = 1920

signSprite = pygame.image.load("sprites/Sign.png")
goalSprite = pygame.image.load("sprites/Goal.png")

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