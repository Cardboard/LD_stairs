import pygame

class Intro:
    def __init__(self, font):
        print('INTRO!')
        self.color_bg = (16,16,16)
        self.color_text = (220,220,220)
        self.font = font
        self.timer = 60 * 100  # in ticks
        self.finished = False
        self.text = []
        text = '''
                                                STAIRS

                                        climb the
                                    stairs by
                                stepping
                            with one
                        foot, then
                    the other,
                then the
            first foot
        then the
    second,
ad infinitum
'''.split('\n')
        for line in text:
            self.text.append(self.font.render(line, 1, self.color_text))

    def update(self, ticks):
        self.timer -= ticks
        print(self.timer)
        if self.timer < 0:
            self.text = self.font.render("created by cardboard", 1, self.color_text)
        if self.timer < -(60 * 100):
           self.finished = True

    def run(self, display, events, keys, ticks):
        self.draw(display)
        self.update(ticks)

    def draw(self, display):
        display.fill(self.color_bg)
        if type(self.text) == list:
            for i in range(len(self.text)):
                display.blit(self.text[i], (150, i * 38))
        else:
            display.blit(self.text, (225,250))
        pygame.display.update()
