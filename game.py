from arcadegraphics import StartGraphicsSystem
from classes import Game
from constants import WIN_WIDTH, WIN_HEIGHT

def main(win):
    # Entry point used by the graphics system
    Game(win)

if __name__ == "__main__":
    # Start the graphics system with the desired window size from constants
    StartGraphicsSystem(main, width=WIN_WIDTH, height=WIN_HEIGHT)