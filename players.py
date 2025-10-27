from arcadegraphics import *


class Player():
    """ Player class that controls the movement of markers on the board. """

    def __init__(self, win, number, game):
        """ The Constructor for Player class. """

        self._win = win
        self._game = game
        self._current_loc = ()
        self._location_history = []
        self._still_playing = True

        self._player_id = str(number + 1)

        # Prepare the possible starting locations for each players:
        initial_side_1 = (
            133, 166, 233, 266, 333, 366, 433, 466, 533, 566, 633, 666)
        initial_side_2 = initial_side_1[::-1]
        self._initial_loc = []
        for x1 in initial_side_1:
            self._initial_loc.append((x1, 100))
        for y1 in initial_side_1:
            self._initial_loc.append((700, y1))
        for x2 in initial_side_2:
            self._initial_loc.append((x2, 700))
        for y2 in initial_side_2:
            self._initial_loc.append((100, y2))

        # Create the graphic part of the markers:
        # All player pieces use the requested theme color
        marker_color = '#9bc3ab'
        panel_color = '#efe2c2'  # parchment panels

        self._marker = Circle(self._win, 12, (133, 100))
        self._marker.set_fill_color(marker_color)
        self._marker.set_depth(6 + 2 * number)
        self._text = Text(self._win, self._player_id, 12, (133, 100))
        self._text.set_depth(5 + 2 * number)
        self._piece = [self._marker, self._text]
        for element in self._piece:
            self._win.add(element)

        # Create clickable button to set piece
        self._box = Rectangle(self._win, 650, 50, (400, 750))
        self._box.set_fill_color(panel_color)
        self._box.set_border_color('#5a4a3b')
        self._box.set_depth(8 + 2 * number)
        prompt = "Player " + self._player_id + \
            ", LEFT CLICK HERE to move your piece clockwise, " + \
            "RIGHT CLICK HERE to set your piece down."
        self._msg = Text(self._win, prompt, 9, (400, 750))
        self._msg.set_depth(7 + 2 * number)
        self._click_box = [self._box, self._msg]
        for element in self._click_box:
            self._win.add(element)
        for element in self._click_box:
            element.add_handler(self)

        self._click_counter = 0

        # Create in game instrucation window
        self._in_game_win = Rectangle(self._win, 555, 250, (1100, -400))
        self._in_game_win.set_fill_color(panel_color)
        self._in_game_win.set_border_color('#5a4a3b')
        self._in_game_win.set_depth(40)
        in_game_txt1 = "Player " + self._player_id + \
            ", please pick a tile to place on the board."
        self._in_game_msg1 = Text(self._win, in_game_txt1, 12, (1100, -330))
        self._in_game_msg1.set_depth(39)
        in_game_txt2 = "LEFT CLICK a tile then LEFT CLICK a location on the" + \
            " board to place it there."
        self._in_game_msg2 = Text(self._win, in_game_txt2, 10, (1100, -466))
        self._in_game_msg2.set_depth(39)
        in_game_txt3 = "RIGHT CLICK the tile to rotate."
        self._in_game_msg3 = Text(self._win, in_game_txt3, 10, (1100, -500))
        self._in_game_msg3.set_depth(39)

        self._in_game_prompt = [self._in_game_win, self._in_game_msg1, \
            self._in_game_msg2, self._in_game_msg3]

        for element in self._in_game_prompt:
            self._win.add(element)

    def display_in_game_prompt(self):
        """ Display the in-game prompt window by moving it onto the screen. """

        location = [(1100, 410), (1100, 315), (1100, 476), (1100, 510)]

        for position in range(4):
            self._in_game_prompt[position].move_to(location[position])

    def hide_in_game_prompt(self):
        """ Hide the in-game prompt window after a player has placed a tile. """

        for element in self._in_game_prompt:
            element.move_to((-400, -400))

    def handle_mouse_press(self, event):
        """ Left click to move the corresponding marker to one next location,
            and right click to set the piece and remove the click box. """

        button = event.get_button()
        if button == "Left Mouse Button":
            # If the move is legal, hide the warning and move the piece
            self._game.hide_warning_overlap()
            if self._click_counter == 47:
                self._click_counter = 0
                for element in self._piece:
                    element.move_to(self._initial_loc[self._click_counter])
            else:
                self._click_counter += 1
                for element in self._piece:
                    element.move_to(self._initial_loc[self._click_counter])

        if button == "Right Mouse Button":
            # If the move is ok, place the marker and move on to the next player
            if self._game.no_overlap(self._initial_loc[self._click_counter]):
                self.update_location(self._initial_loc[self._click_counter])
                for element in self._click_box:
                    element.move_to((-1000, -1000))
                self._game.hide_hand(self._player_id)

                # If this is the last player to finish set up, then run game
                if self._game.last_on_the_list(self._player_id):
                    self._game.remove_initial_view()
                    self._game.run()
            else:
                self._game.show_warning_overlap()

    def update_location(self, coord):
        """ Update the current location, and also adding it to history. """

        self._current_loc = coord
        self._location_history.append(coord)

    def return_current_loc(self):
        """ Return the current location. """

        return self._current_loc

    def hist(self):
        """ Return the marker movement history. """

        return self._location_history

    def move_player(self, location):
        """ Move the player marker to given location. """

        for element in self._piece:
            element.move_to(location)

    def eliminated(self):
        """ This player is eliminated, update status, remove marker. """

        self.move_player((-100, -100))
        self._still_playing = False

    def return_border(self):
        """ Return the coordinate for the borders. """

        return self._initial_loc

    def return_id(self):
        """ Return player id string. """

        return self._player_id

    def still_in(self):
        """ Returns a boolean to show if player is still in the game. """

        return self._still_playing
