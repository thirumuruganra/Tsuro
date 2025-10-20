from game_core import main

from arcadegraphics import StartGraphicsSystem
from constants import WIN_WIDTH, WIN_HEIGHT

if __name__ == "__main__":
    # Start the graphics system with the desired window size from constants
    StartGraphicsSystem(main, width=WIN_WIDTH, height=WIN_HEIGHT)