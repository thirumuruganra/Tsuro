from arcadegraphics import *


class Cell():
    """ Cells on the board and can provide a move_to location for the tile. """

    def __init__(self, win, game, location):
        """ The Constructor for Tile class. """

        self._win = win
        self._game = game
        self._location = location
        self._body = Square(self._win, 100, self._location)
        self._body.set_fill_color("")
        self._body.set_depth(35)
        self._body.set_border_width(0)
        self._win.add(self._body)

    def give_handler(self):
        """ Add event handler to the cell. """

        self._body.add_handler(self)

    def handle_mouse_press(self, event):
        """ Asks the Board to send a clicked Tile to Cell's self. """

        button = event.get_button()
        if button == "Left Mouse Button":
            self._game.send_tile_to_me(self)

    def create_unclickable_layer(self):
        """ Make an unclickable layer to lock this cell from doing anything. """

        layer = Square(self._win, 100, self._location)
        layer.set_fill_color("")
        layer.set_depth(5)
        layer.set_border_color("")
        self._win.add(layer)

    def get_location(self):
        """ Returns the location (a tuple) of the Cell. """

        return self._location
