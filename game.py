import pygame
import random

class Game:
    def __init__(self, display, font):
        self.color_bg = (16, 16, 16)
        self.display = display
        self.player = Player(display)
        self.stairs = Stairs(display)
        self.timer = 0
    def run(self, display, events, keys, ticks):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if self.player.right.y == self.player.right.starting_y and self.player.left.y == self.player.left.starting_y:
                        self.player.right.moving = True
                        print('STEPPING RIGHT...')
                if event.key == pygame.K_LEFT:
                    if self.player.left.y == self.player.left.starting_y and self.player.right.y == self.player.right.starting_y: #self.player.right.moving == False:
                        self.player.left.moving = True
                        print('STEPPING LEFT...')
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.right.moving = False
                    print('STOPPED STEPPING RIGHT...')
                if event.key == pygame.K_LEFT:
                    self.player.left.moving = False
                    print('STOPPED STEPPING LEFT...')
        self.player.right.move()
        self.player.left.move()
        self.draw(display)
    def update(self, ticks):
        self.timer += ticks
        if self.timer > 1000: #! ADJUST IF NECESSARY
            stairs.generateStep(self.player.left.y, self.player.right.y)
            self.timer = 0
    def draw(self, display):
        display.fill(self.color_bg)
        self.player.left.draw(display)
        self.player.right.draw(display)
        pygame.display.update()

class Player:
    def __init__(self, display):
        self.left = Foot(display, 250) #! ADJUST
        self.right = Foot(display, 500) #! ADJUST

class Foot:
    def __init__(self, display, x):
        self.display = display
        self.x = x
        self.width = 50 #! ADJUST
        self.height = 75 #! ADJUST
        self.starting_y = self.display.get_height() - self.height
        self.y = self.starting_y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = 10 #! ADJUST
        self.speed_reverse = 5 #! ADJUST
        self.min_y = 300 #! ADJUST
        self.moving = False
    def draw(self, display):
        pygame.draw.rect(display, (234, 41, 214), self.rect)
    def move(self):
        if self.moving == True:
            print(self.rect.y)
            self.y -= self.speed
            self.y = self.clamp(self.y, self.min_y, self.starting_y)
            self.rect.top = self.y
            if self.y <= self.min_y:
                self.moving = False
        elif self.moving == False:
            self.y += self.speed_reverse
            self.y = self.clamp(self.y, self.min_y, self.starting_y)
            self.rect.top = self.y
    def clamp(self, val, low, high):
        if val < low:
            return low
        elif val > high:
            return high
        else:
            return val
    def onStep(self, stairs):
        for step in stairs:
            pass
            #CHECK IF FOOT ON STEP

class Stairs:
    def __init__(self, display):
        self.display = display
        self.steps = pygame.sprite.Group()
    def generateStep(self, left_y, right_y):
        #FIGURE OUT WHERE TO PLACE EACH FOOT
        #BASED ON FEET Y POSITIONS
        #EACH STEP IS A SPRITE
        newStep = Step()
        self.steps.add(newStep)

class Step(pygame.sprite.Sprite):
    def __init__(self):
        self.width = 100
        self.height = 50
