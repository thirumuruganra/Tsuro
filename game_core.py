from arcadegraphics import *
from classes import Game
from constants import WIN_WIDTH, WIN_HEIGHT

def main(win):
    win._width = WIN_WIDTH
    win._height = WIN_HEIGHT

    Game(win)

if __name__ == "__main__":
    StartGraphicsSystem(main)