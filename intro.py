import pygame

class Intro:
    def __init__(self, font):
        print('INTRO!')
        self.color_bg = (16,16,16)
        self.color_text = (220,220,220)
        self.font = font
        self.timer = 60 * 5000  # in ticks
        self.finished = False
        self.text = []
        text = '''
                    S
                R
            I
        A
    T
S




CONTROLS: LEFT AND RIGHT
'''.split('\n')
        for line in text:
            self.text.append(self.font.render(line, 1, self.color_text))

    def update(self, ticks):
        self.timer -= ticks
        if self.timer < 0:
            self.text = self.font.render("created by cardboard", 1, self.color_text)
        if self.timer < -(60 * 3000):
           self.finished = True

    def run(self, display, ticks):
        self.draw(display)
        self.update(ticks)

    def draw(self, display):
        display.fill(self.color_bg)
        if type(self.text) == list:
            for i in range(len(self.text)):
                display.blit(self.text[i], (300, 100+ i * 20))
        else:
            display.blit(self.text, (310,400))
        pygame.display.update()
