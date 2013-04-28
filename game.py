import sys
import timeit
import pygame
import random

class Game:
    def __init__(self, display, font):
        self.color_bg = (16, 16, 16)
        self.display = display
        self.player = Player(display)
        self.stairs = Stairs(display)
        self.timer = timeit.default_timer()
        self.timer_interval = 0.75
        self.start_time = timeit.default_timer()
        self.game_time = self.start_time + 14
    def run(self, display, keys, ticks):
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
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
        if timeit.default_timer() > (self.timer + self.timer_interval):
            self.stairs.generateStep(self.player.left.y, self.player.right.y)
            self.timer = timeit.default_timer()
        for step in self.stairs.steps:
            step.update(self.display, self.player.left, self.player.right)
        # check if player hits a step or falls off staircase
        if timeit.default_timer() > self.game_time:
            self.player.checkFeet(self.stairs)
        self.player.right.move()
        self.player.left.move()
        self.draw(display)
    def draw(self, display):
        display.fill(self.color_bg)
        #self.stairs.steps.draw(display)
        for step in self.stairs.steps:
            step.draw(self.display)
        self.player.left.draw(display)
        self.player.right.draw(display)
        try:
            pygame.draw.rect(self.display, (0,255,128), self.player.debugrect)
        except:
            pass
        pygame.display.update()

class Player:
    def __init__(self, display):
        self.display = display
        self.left = Foot(display, 250) #! ADJUST
        self.right = Foot(display, 500) #! ADJUST
        self.debugrect = pygame.Rect(0,0,0,0)
    def checkFeet(self, stairs):
        for step in stairs.steps:
            if self.left.rect.colliderect(step.rect) or self.right.rect.colliderect(step.rect):
                if self.left.y == self.left.starting_y and self.right.y == self.right.starting_y:
                    self.debugrect = self.left.rect.clip(step.rect)

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

class Stairs:
    def __init__(self, display):
        self.display = display
        self.steps = pygame.sprite.Group()
        self.lastx = display.get_width()/2
        self.gap = 0#50
    def generateStep(self, left_y, right_y):
        print('NEW STEP')
        # RANDOM X COORD THAT IS CLOSE TO LAST X COORD
        newx = random.randint(self.lastx-self.gap, self.lastx+self.gap)
        self.steps.add(Step(newx))
        self.lastx = newx

class Step(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = -25
        self.width = 100
        self.height = 25
        self.yspeed = 0
        self.xspeed = 0
        self.image = pygame.Surface( (self.width, self.height) )
        self.image.fill( (220, 220, 220) )
        self.rect = self.image.get_rect()
    def draw(self, display):
        pygame.draw.rect(display, (220, 220, 220), self.rect)
    def update(self, display, left, right):
        self.x += self.xspeed
        self.y += self.yspeed
        self.rect.top = self.y
        self.rect.left = self.x
        # UPDATE DEPENDING ON LEFT AND RIGHT FEET
        if left.moving == True:
            coeff = 1
        elif right.moving == True:
            coeff = -1
        else:
            coeff = 0
        self.xspeed = abs(self.y) / 100
        self.xspeed = coeff * self.clamp(self.xspeed, 0.5, 10)
        self.yspeed = abs(self.y**2) / 50000
        self.yspeed = self.clamp(self.yspeed, 0.3, 10)
        # SCALE DEPENDING ON Y POSITION
        self.rect = pygame.Rect(self.x, self.y, self.width*self.yspeed, self.height* self.clamp(self.y/500, 0.1, 3) ) #self.rect.inflate(self.yspeed, self.yspeed/3)
        self.rect.move_ip(-self.yspeed*50, 0)
        # DELETE IF OFF SCREEN
        if self.y > display.get_height():
            self.kill()
            print("STEP KILLED")
    def clamp(self, val, low, high):
        if val < low:
            return low
        elif val > high:
            return high
        else:
            return val
