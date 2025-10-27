from arcadegraphics import *
from constants import IMG_DIR


class Tile():
    """ Tile class that interactive and carries the location logic. """

    def __init__(self, win, game, number, coord):
        """ The Constructor for Tile class. """

        self._win = win
        self._game = game
        self._id_n = number
        self._rotations = 0
        self._coord = coord
        self._status = "pile"
        self._clicked = False

        self._image_loc = IMG_DIR + '/' + str(self._id_n) + ".jpg"
        self._image = Image(self._win, self._image_loc, 100, 100, (-350, -350))
        self._image.set_depth(30)
        self._frame = Square(self._win, 100, (-350, -350))
        self._frame.set_fill_color("")
        self._frame.set_depth(31)
        self._frame.set_border_width(0)
        self._tile = [self._image, self._frame]
        for element in self._tile:
            self._win.add(element)

    def return_status(self):
        """ Return the status of the tile (pile/(player#)/board). """

        return self._status

    def change_status(self, command_str):
        """ Updatae the status of the tile. """

        self._status = command_str

    def move_location(self, coord):
        """ Move the tile image to location. """

        for element in self._tile:
            element.move_to(coord)

    def change_depth(self, depth):
        """ Change the depth of the tile image. """

        for element in self._tile:
            element.set_depth(depth)

    def return_coord(self):
        """ Determines the orientation of the tile, then return the location
            logic for the game. """

        return self._coord[self._rotations % 4]

    def give_handler(self):
        """ Add event handler to the tile. """
        self._image.add_handler(self)
        # Also attach to the frame so clicks on the blue border are registered
        self._frame.add_handler(self)

    def handle_mouse_press(self, event):
        """ Asks the Board to send a clicked Tile to Cell's self. """

        button = event.get_button()
        if button == "Left Mouse Button":
            if not self._clicked:

                # then highlight the Tile's border:
                self._clicked = True
                self._frame.set_border_width(5)
                # Selection color updated to muted ink-blue accent for scroll theme
                self._frame.set_border_color('#9bc3ab')
                self._game.unclick_all_other(self._id_n)
            else:

                # then un-highlight the Tile's border:
                self._clicked = False
                self._frame.set_border_width(0)
                self._frame.set_border_color("black")
        if button == "Right Mouse Button":
            self._image.rotate(90)
            self._rotations += 1

    def is_clicked(self):
        """ Returns the Tile's _clicked status. """

        return self._clicked

    def set_still(self):
        """ Make the tile unclickable and update tile status to 'board'. """

        for element in self._tile:
            element.set_depth(36)
        self._clicked = False
        self._frame.set_border_width(0)
        self._frame.set_border_color("black")
        self.change_status("board")

    def change_clicked(self):
        """ Change the status for this tile to unclicked. """

        self._clicked = False
        self._frame.set_border_width(0)
        self._frame.set_border_color("black")

    def return_image_id(self):
        """ Returns image id number. """

        return self._id_n


class Dragon:
    """ Dragon tile that the first player receive when the pile is empty. """

    def __init__(self, win, game):
        """ The Constructor for Dragon class. """

        self._win = win
        self._game = game
        self._status = "pile"
        self._tile = Image(self._win, IMG_DIR + "/dragon.jpg", 100, 100, (-250, -250))
        self._tile.set_depth(30)
        self._win.add(self._tile)

    def return_status(self):
        """ Return the status of the tile (pile or player#). """

        return self._status

    def change_status(self, command_str):
        """ Updatae the status of the tile. """

        self._status = command_str

    def move_location(self, coord):
        """ Move the tile image to location. """

        self._tile.move_to(coord)

    def change_depth(self, depth):
        """ Change the depth of the tile image. """

        self._tile.set_depth(depth)
