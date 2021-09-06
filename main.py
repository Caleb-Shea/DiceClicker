import pygame as pyg
import random
import math
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

FPS = 30

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

def main():

    clock = pyg.time.Clock()

    while True:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                terminate()
            elif event.type == pyg.KEYDOWN:
                if event.key == pyg.K_BACKQUOTE:
                    terminate()
            elif event.type == pyg.MOUSEBUTTONDOWN:
                ...

        window.fill((200, 200, 200))

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
