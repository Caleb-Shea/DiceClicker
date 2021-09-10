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

        self.num_sides = 3 # Max number the dice can potentially roll
        self.bias = 0 # How likely a dice is to roll a higher number
        self.cur_face = 1 # The current side of the dice
        self.speed = 8 # The time it takes to complete the rolling animation
        self.roll_cooldown = 0

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

        self.add_money_this_frame = False

        self.money_made = 0

    def set_num_sides(self, amount):
        self.num_sides = amount
        return self.num_sides

    def set_image(self, num):
        self.image = self.die_sides[num]

    def roll(self):
        self.cur_face = random.randint(1, self.num_sides)

        self.set_image(self.cur_face)

        self.roll_cooldown = self.speed * FPS//2

    def update(self):
        if self.roll_cooldown > 0: # Rolling animation control
            self.roll_cooldown -= 1
            self.set_image(random.randint(1, self.num_sides))
            if self.roll_cooldown == 0:
                self.set_image(self.cur_face)
                self.add_money_this_frame = True

    def set_pos(self, pos):
        self.rect.center = pos

    def render(self):
        self.window.blit(self.image, self.rect)


class DieUpgrade():
    def __init__(self, window, die):
        self.window = window
        self.die = die

        self.font20 = pyg.font.Font(get_path(os.path.join('fonts', 'Massa.ttf')), 20)
        self.font15 = pyg.font.Font(get_path(os.path.join('fonts', 'Massa.ttf')), 15)

        self.up1_button = Button(self.window, pyg.USEREVENT + 1,
                                 self.die.rect.move(0, 120).topleft, (self.die.rect.width, 30),
                                 (170, 100, 100, 180), text='Upgrade Level')

    def render(self):
        if self.die.rect.collidepoint(pyg.mouse.get_pos()):
            self.up1_button.render()


class DieInfo():
    def __init__(self, window, die):
        self.window = window
        self.die = die

        self.font20 = pyg.font.Font(get_path(os.path.join('fonts', 'Massa.ttf')), 20)
        self.font15 = pyg.font.Font(get_path(os.path.join('fonts', 'Massa.ttf')), 15)

        self.image = pyg.Surface(die.rect.size).convert_alpha()
        self.image.fill((0, 200, 150, 180))
        self.rect = self.image.get_rect()

        self.show_stats = False

    def update(self):
        if self.show_stats:
            self.image = pyg.transform.smoothscale(self.image, (200, 150))
        else:
            self.image = pyg.transform.smoothscale(self.image, self.die.rect.size)
        self.rect = self.image.get_rect()

        self.rect.left = self.die.rect.right + 10
        self.rect.y = self.die.rect.y

        if self.rect.right > WIDTH:
            self.rect.right = self.die.rect.left - 20

    def update_image(self):
        self.image.fill((0, 200, 150, 180))

        if self.show_stats:
            self.money_made_text = self.font15.render(f'Money Made: {self.die.money_made}', True, (0, 0, 0))

            self.image.blit(self.money_made_text, (10, 10))

        else:
            black = (0, 0, 0)
            self.num_sides_text = self.font20.render(f'Max: {self.die.num_sides}', True, black)
            self.bias_text = self.font20.render(f'Level: {self.die.bias}', True, black)
            self.speed_text = self.font20.render(f'Speed: {self.die.speed}', True, black)

            self.bottom_text = self.font15.render('To see stats,', True, (0, 0, 0))
            self.bottom_text2 = self.font15.render('hold SHIFT', True, (0, 0, 0))

            self.image.blit(self.num_sides_text, (10, 10))
            self.image.blit(self.bias_text, (10, 30))
            self.image.blit(self.speed_text, (10, 50))
            self.image.blit(self.bottom_text, (10, 80))
            self.image.blit(self.bottom_text2, (10, 95))

    def render(self):
        if self.die.rect.collidepoint(pyg.mouse.get_pos()):
            self.window.blit(self.image, self.rect)

class Button():
    def __init__(self, window, e_num, pos, size, bg_col, icon=None, text=None):
        self.window = window

        self.image = pyg.Surface((size))
        self.image.fill(bg_col)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.font15 = pyg.font.Font(get_path(os.path.join('fonts', 'Massa.ttf')), 15)

        self.e_num = e_num

        self.icon = icon
        self.text = text

        if self.icon != None:
            self.icon = pyg.image.load(get_path(os.path.join('imgs', 'buttons', f'{icon}.png')))
            self.icon_rect = self.icon.get_rect()
            self.icon_rect.center = self.rect.center

            self.image.blit(self.icon, self.icon_rect)
        elif self.text != None:
            self.text = self.font15.render(self.text, True, (0, 0, 0, 200))
            self.text_rect = self.text.get_rect()
            self.text_rect.center = self.rect.center

            pos = (self.text_rect.x - self.rect.x, # Adjust for image rect offset
                   self.text_rect.y - self.rect.y)

            self.image.blit(self.text, pos)

    def render(self):
        self.window.blit(self.image, self.rect)


class GUI():
    def __init__(self, window):
        self.window = window

        self.font24 = pyg.font.Font(get_path(os.path.join('fonts', 'Massa.ttf')), 24)
        self.font32 = pyg.font.Font(get_path(os.path.join('fonts', 'Massa.ttf')), 32)
        self.font40 = pyg.font.Font(get_path(os.path.join('fonts', 'Massa.ttf')), 40)

        self.text_list = []
        self.dyn_dict = {}

        self.add_text('Current $: ', (10, 20), (0, 0, 0))


    def add_text(self, text, pos, col):
        for t in self.text_list[:]: # If text already exists at a certain place, replace it
            if t[1] == pos:
                self.text_list.remove(t)

        surf = self.font32.render(text, True, col)
        self.text_list.append([surf, pos])

    def render(self):
        for t in self.text_list:
            self.window.blit(t[0], t[1])


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

def new_dice(window, dice, dice_info, dice_up):
    if len(dice) < 60:
        die = Die(window)
        dice.append(die)
        position_all_dice(dice)

        die_info = DieInfo(window, die)
        dice_info.append(die_info)

        die_up = DieUpgrade(window, die)
        dice_up.append(die_up)

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
    gui = GUI(window)

    dice = []
    dice_info = []
    dice_up = []

    new_dice(window, dice, dice_info, dice_up)

    money = 0

    clock = pyg.time.Clock()

    while True:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                terminate()

            elif event.type == pyg.KEYDOWN:
                if event.key == pyg.K_BACKQUOTE:
                    terminate()
                elif event.key == pyg.K_SPACE: # Add new dice, max of 60
                    new_dice(window, dice, dice_info)
                elif event.key == pyg.K_LSHIFT:
                    for di in dice_info:
                        di.show_stats = True
                elif event.key == pyg.K_o:
                    # gui.add_text(f'{random.random()}test', (100, 200), (0, 0, 0))
                    money *= 2
                elif event.key == pyg.K_p:
                    for d in dice:
                        if d.num_sides < 12:
                            d.num_sides += 1

            elif event.type == pyg.KEYUP:
                if event.key == pyg.K_LSHIFT:
                    for di in dice_info:
                        di.show_stats = False

            elif event.type == pyg.MOUSEBUTTONDOWN:
                for d in dice:
                    if d.rect.collidepoint(event.pos):
                        if d.roll_cooldown == 0:
                            d.roll()

        gui.add_text(str(money), (175, 20), (200, 0, 0))

        window.fill((200, 200, 200))

        for d in dice:
            d.update()
            if d.add_money_this_frame:
                money += d.cur_face
                d.money_made += d.cur_face
                d.add_money_this_frame = False
            d.render()

        for di in dice_info:
            di.update()
            di.update_image()
            di.render()

        for du in dice_up:
            du.render()

        gui.render()

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
