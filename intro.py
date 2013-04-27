import pygame

class Intro:
    def __init__(self, font):
        self.color_bg = (16,16,16)
        self.color_text = (220,220,220)
        self.font = font
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
        self.text = []
        for line in text:
            self.text.append(font.render(line, 1, self.color_text))
        print("INTRO")

    def run(self, display, events, keys, ticks, font):
        self.draw(display, font)
        #self.update(ticks)

    def draw(self, display, font):
        display.fill(self.color_bg)
        for i in range(len(self.text)):
            display.blit(self.text[i], (150, i * 38))
        pygame.display.update()




