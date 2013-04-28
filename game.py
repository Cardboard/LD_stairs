import sys
import timeit
import pygame
import random

class Game:
    def __init__(self, display, font, serious=False):
        print("GAME!")
        self.color_bg = (16, 16, 16)
        self.display = display
        self.font = font
        self.player = Player(display)
        self.stairs = Stairs(display)
        if serious == True:
            filename = 'serious.png'
        else:
            filename = 'potato.png'
        self.potato = Potato(display,filename)
        self.state = 'game'
        self.timer = timeit.default_timer()
        self.timer_interval = 0.75
        self.start_time = timeit.default_timer()
        self.game_time = self.start_time + 14
        self.endgame_time = self.start_time + 60
        text = "DON'T TRIP. DON'T FALL OFF."
        self.message = [self.font.render(text, 1, (220,220,220)), self.font.size(text)[0], self.start_time + 6]
    def reset(self):
        self.state = 'game'
        self.player = Player(self.display)
        text = "DON'T TRIP. DON'T FALL OFF."
        self.start_time = timeit.default_timer()
        self.message = [self.font.render(text, 1, (220,220,220)), self.font.size(text)[0], self.start_time + 6]
        self.game_time = self.start_time + 14
        self.endgame_time = self.start_time + 60
        self.stairs.reset()
    def gameOver(self):
        if self.player.dead == True:
            print("GAMEOVER")
            return True
    def run(self, display, ticks):
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if self.player.right.y == self.player.right.starting_y and self.player.left.y == self.player.left.starting_y:
                        self.player.right.moving = True
                if event.key == pygame.K_LEFT:
                    if self.player.left.y == self.player.left.starting_y and self.player.right.y == self.player.right.starting_y: #self.player.right.moving == False:
                        self.player.left.moving = True
                if event.key == pygame.K_DOWN:
                    self.endgame_time = timeit.default_timer() + 10
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.right.moving = False
                if event.key == pygame.K_LEFT:
                    self.player.left.moving = False
        if timeit.default_timer() > self.endgame_time:
            self.state = 'endgame'
            self.stairs.gap = 0
            self.stairs.lastx = self.display.get_width()/2
        if timeit.default_timer() > (self.game_time + 30):
            self.stairs.gap = 100
        if self.state == 'game' and timeit.default_timer() > (self.timer + self.timer_interval):
                self.stairs.generateStep(self.player.left.y, self.player.right.y)
                self.timer = timeit.default_timer()
        if self.state == 'endgame' and timeit.default_timer() < (self.endgame_time + 5):
            if timeit.default_timer() > (self.timer + self.timer_interval):
                self.stairs.generateStep(self.player.left.y, self.player.right.y)
                self.timer = timeit.default_timer()
        self.stairs.killSteps()
        for step in self.stairs.steps:
            if timeit.default_timer() > self.endgame_time + 12:
                step.update(self.display, self.player.left, self.player.right, True)
            else:
                step.update(self.display, self.player.left, self.player.right, False)

        # check if player hits a step or falls off staircase
        if timeit.default_timer() > self.game_time:
            self.player.checkFeet(self.stairs)
        # play player death animation if player is dead
        self.player.die()
        self.player.right.move()
        self.player.left.move()
        self.draw(display)
        if self.state == 'endgame':
            self.potato.move()
    def draw(self, display):
        display.fill(self.color_bg)
        pygame.draw.rect(self.display, (0,0,255), self.player.safezone)
        for step in self.stairs.steps:
            step.draw(self.display)
        self.player.left.draw(display)
        self.player.right.draw(display)
        try:
            pygame.draw.rect(self.display, (0,255,128), self.player.debugrect)
        except:
            pass
        self.draw_message()
        if self.state == 'endgame':
            self.potato.draw(self.display)
        pygame.display.update()
    def draw_message(self):
        if timeit.default_timer() < self.message[2]:
            self.display.blit(self.message[0],(self.display.get_width()/2-self.message[1]/2, 100))

class Player:
    def __init__(self, display):
        self.display = display
        self.display_height = self.display.get_height()
        self.left = Foot(display, 250) #! ADJUST
        self.right = Foot(display, 500) #! ADJUST
        self.safezone = pygame.Rect(0,0,0,0)
        self.debugrect = pygame.Rect(0,0,0,0)
        self.dead = False
        self.death = 0 # 1 = left foot falls, 2 = right foot falls, 3 = hit step
    def checkFeet(self, stairs):
        for step in stairs.steps:
            # either foot collides with a step
            if self.left.rect.colliderect(step.rect) or self.right.rect.colliderect(step.rect):
                # both feet are on the ground
                if self.left.y == self.left.starting_y and self.right.y == self.right.starting_y:
                    self.death = 3
                    self.debugrect = self.left.rect.clip(step.rect) #! REMOVE
        # set safezone (rect where foot doesn't fall off of staircase)
        self.safezone = pygame.Rect(stairs.killed_step.x+50, self.display_height-200, stairs.killed_step.width-50, 200)
        if self.left.rect.colliderect(self.safezone):
            pass # foot is in safezone
        # foot isn't on a step. fall off staircase if foot isn't in the air
        else:
            if self.left.y == self.left.starting_y:
                print("LEFT FOOT FELL OFF STAIRCASE!")
                self.death = 1
        if self.right.rect.colliderect(self.safezone):
            pass # foot is in safezone
        # foot isn't on a step. fall off staircase if foot isn't in the air
        else:
            if self.right.y == self.right.starting_y:
                print("RIGHT FOOT FELL OFF STAIRCASE!")
                self.death = 2

    # feet fall off bottom of stage
    def die(self):
        if self.death == 3:
            self.left.die()
            self.right.die()
        if self.death == 2:
            self.right.die()
        if self.death == 1:
            self.left.die()
        else:
            pass
        if self.left.rect.y > self.display_height+50 or self.right.rect.y > self.display_height+50:
            self.dead = True

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
        self.speed_reverse = 10 #! ADJUST
        self.min_y = 300 #! ADJUST
        self.moving = False
        self.dead = False
    def die(self):
        if self.dead == False:
            print("FOOT KILLED")
            self.starting_y = self.display.get_height() + 100
            self.moving = False
            self.speed = 0
            self.speed_reverse = 3
            self.dead = True
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
        self.gap = 50
        self.killed_step = pygame.Rect(0,0,0,0)
    def generateStep(self, left_y, right_y):
        # RANDOM X COORD THAT IS CLOSE TO LAST X COORD
        newx = random.randint(self.lastx-self.gap, self.lastx+self.gap)
        self.steps.add(Step(newx))
        self.lastx = newx
    def killSteps(self):
        for step in self.steps:
            if step.y > self.display.get_height():
                self.killed_step = step.rect
                step.kill()
    def reset(self):
        self.lastx = self.display.get_width()/2
        self.gap = 50
        for step in self.steps:
            step.kill()


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
    def update(self, display, left, right, potato):
        self.x += self.xspeed
        self.y += self.yspeed
        self.rect.top = self.y
        self.rect.left = self.x
        # UPDATE DEPENDING ON LEFT AND RIGHT FEET
        if left.moving == True and potato == False:
            coeff = 1
        elif right.moving == True and potato == False:
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
    def clamp(self, val, low, high):
        if val < low:
            return low
        elif val > high:
            return high
        else:
            return val

class Potato(pygame.sprite.Sprite):
    def __init__(self, display, filename):
        self.display = display
        self.display_width = self.display.get_width()
        self.filename = filename
        self.image = pygame.image.load(self.filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.y = -200
        self.rect.y = self.y
        self.rect.x = display.get_width()/2 - self.rect.width/2
        self.max_y = 150
        self.speed = 0.3
    def move(self):
        if self.rect.y <= self.max_y:
            if self.y < 125:
                self.speed = 0.3
            else:
                self.speed = self.clamp((self.y-125)**2/1000, 0.3, 1)
            self.y += self.speed
            if self.y > 50:
                width = int(self.y)
                height = int(self.y)
            else:
                width = 50
                height = 50
            self.rect = pygame.Rect((self.display_width/2-width/2), self.y, width, height)
            self.image = pygame.transform.scale(pygame.image.load(self.filename).convert_alpha(), (width, height))
    def draw(self, display):
        pygame.draw.rect(display, (255,0,255), self.rect)
        display.blit(self.image, self.rect)
    def ready(self):
        if self.rect.y == self.max_y:
            return True
    def clamp(self, val, low, high):
        if val < low:
            return low
        elif val > high:
            return high
        else:
            return val
