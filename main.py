import pygame as pyg
import random
import math
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

FPS = 30


class Die(pyg.sprite.Sprite):
    def __init__(self, window):
        super().__init__()
        self.window = window

        self.image = pyg.image.load(get_path(os.path.join('imgs', 'die_faces', '1.png')))

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2, HEIGHT//2)

        self.num_sides = 12 # Number of sides the dice can potentially roll
        self.bias = 0 # How likely a dice is to roll a higher number
        self.speed = 1 # The time it takes to complete the rolling animation
        self.side = 1 # The current side of the dice

        self.die_sides = {1: pyg.image.load(get_path(os.path.join('imgs', 'die_faces', '1.png'))),
                           2: pyg.image.load(get_path(os.path.join('imgs', 'die_faces', '2.png'))),
                           3: pyg.image.load(get_path(os.path.join('imgs', 'die_faces', '3.png'))),
                           4: pyg.image.load(get_path(os.path.join('imgs', 'die_faces', '4.png'))),
                           5: pyg.image.load(get_path(os.path.join('imgs', 'die_faces', '5.png'))),
                           6: pyg.image.load(get_path(os.path.join('imgs', 'die_faces', '6.png'))),
                           7: pyg.image.load(get_path(os.path.join('imgs', 'die_faces', '7.png'))),
                           8: pyg.image.load(get_path(os.path.join('imgs', 'die_faces', '8.png'))),
                           9: pyg.image.load(get_path(os.path.join('imgs', 'die_faces', '9.png'))),
                           10: pyg.image.load(get_path(os.path.join('imgs', 'die_faces', '10.png'))),
                           11: pyg.image.load(get_path(os.path.join('imgs', 'die_faces', '11.png'))),
                           12: pyg.image.load(get_path(os.path.join('imgs', 'die_faces', '12.png')))}


    def set_num_sides(self, amount):
        self.num_sides = amount
        return self.num_sides

    def set_image(self, num):
        self.image = self.die_sides[num]

    def roll(self):
        self.side = random.randint(1, self.num_sides)

        self.set_image(self.side)

    def set_pos(self, pos):
        self.rect.center = pos

    def render(self):
        self.window.blit(self.image, self.rect)


def terminate():
    pyg.quit()
    raise SystemExit()

def get_path(path):
    """Returns the full file path of a file."""
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dirname, path)

def play_sound(sound):
    se_channel = pyg.mixer.find_channel()
    se_channel.play(sound)

def position_all_dice(dice):
    num_die = len(dice)
    num_rows = math.ceil(num_die / 10)

    for i in range(num_rows): # Split dice into groups of 10 so each row can be centered independently
        try:
            row = dice[10*i:10*i+10]
        except:
            row = dice[10*i:]

        for j, die in enumerate(row):
            # Center each row around the WIDTH//2 with a set interval between each row
            die.rect.centery = HEIGHT//2 + 120*i - 60*num_rows + 60
            # Then center each die within each row
            die.rect.centerx = WIDTH//len(row) * (j + .5)

def main():
    dice = []
    die1 = Die(window)
    dice.append(die1)

    clock = pyg.time.Clock()

    while True:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                terminate()

            elif event.type == pyg.KEYDOWN:
                if event.key == pyg.K_BACKQUOTE:
                    terminate()
                elif event.key == pyg.K_SPACE: # New dice, max of 60
                    if len(dice) < 60:
                        die = Die(window)
                        dice.append(die)

                        position_all_dice(dice)

            elif event.type == pyg.MOUSEBUTTONDOWN:
                for d in dice:
                    if d.rect.collidepoint(event.pos):
                        d.roll()

        window.fill((200, 200, 200))

        for d in dice:
            d.render()

        pyg.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    pyg.mixer.pre_init(44100, -16, 2, 512)
    pyg.mixer.init()
    pyg.init()
    pyg.display.set_caption("Dice Clicker")
    window = pyg.display.set_mode(flags=pyg.HWSURFACE | pyg.FULLSCREEN | pyg.DOUBLEBUF)
    WIDTH, HEIGHT = pyg.display.get_window_size()

    main()
