from random import choice
from arcadegraphics import *
from constants import WIN_WIDTH, WIN_HEIGHT, BOARD_LEN, IMG_DIR
from helpers import load_matches
class Game:
    """ The Game class that controls all the other classes. """

    def __init__(self, win):
        """ The Constructor for the Board. """

        self._win = win
        # Initiate overall player list and active player list (for game cycls):
        self._players_list = []
        self._active_players = []

        # Theme colors (ancient scroll)
        self._parchment = '#efe2c2'   # panel background
        self._parchment_btn = '#e8dec5'  # buttons
        self._ink = '#2f2a1e'         # text/border ink
        self._accent_blue = '#6B8BA4' # subtle selection accent

        # Dicationaries that controls markers' movement
        # Need 2 dict - each spot on the board corresponds to two other spots
        self._loc_dict1 = {}
        self._loc_dict2 = {}

        # Location logic keys for each tile
        # 8 spots that make 4 connection pairs per rotation, 4 rotation per tile
        self._coord_list = load_matches()

        # Adding background image
        self._bkg = Image(
            self._win, IMG_DIR + '/bkg2.png', WIN_WIDTH, WIN_HEIGHT, (750, 400))
        self._bkg.set_depth(50)
        self._win.add(self._bkg)

        # Adding board image
        self._board_ctr = (400, 400)
        self._board = Image(
            self._win, IMG_DIR + '/board.jpg', BOARD_LEN, BOARD_LEN, self._board_ctr)
        self._board.set_depth(40)
        self._win.add(self._board)

        # Make all the tiles ready to use

        self._tiles = [
            Tile(self._win, self, n, self._coord_list[n]) for n in range(35)]

        # Make dragon tile, and add it to the overall list
        self._dragon = Dragon(self._win, self)
        self._all_tiles = self._tiles + [self._dragon]

        # Making a popup window to get the amount of players
        Popup(self._win, self)

        # Prepare (but do not yet show) the initial prompt window; it will be
        # displayed after players choose the player count.
        self._initial_msg = self.initial_view()

        # Make the cells on the board
        side_coord = [150, 250, 350, 450, 550, 650]
        cell_coord = [(x, y) for x in side_coord for y in side_coord]
        self._cells = [Cell(self._win, self, coord) for coord in cell_coord]

        # Make warnings for illegal placement of pieces and tiles

        w_overlap_box = Rectangle(self._win, 600, 50, (-1100, -600))
        w_overlap_box.set_fill_color(self._parchment)
        w_overlap_box.set_border_color(self._ink)
        w_overlap_box.set_depth(2)
        w_overlap_text = Text(self._win, \
            "WARNING: You cannot place your piece here, this spot is taken!", \
            15, (-1100, -600))
        #w_overlap_text.set_color("red")
        w_overlap_text.set_depth(1)
        self._warn_overlap = [w_overlap_box, w_overlap_text]
        for element in self._warn_overlap:
            self._win.add(element)

        w_placement_box = Rectangle(self._win, 600, 50, (-1100, -600))
        w_placement_box.set_fill_color(self._parchment)
        w_placement_box.set_border_color(self._ink)
        w_placement_box.set_depth(2)
        w_placement_text = Text(self._win, \
            "WARNING: You can only place a tile next to your piece!", \
            15, (-1100, -600))
        #w_placement_text.set_color("red")
        w_placement_text.set_depth(1)
        self._warn_placement = [w_placement_box, w_placement_text]
        for element in self._warn_placement:
            self._win.add(element)

    def run(self):
        """ The main game squence, after all the inital prep is done. """

        # Add handlers for all cells and tiles to make them clickable:
        for cell in self._cells:
            cell.give_handler()
        for tile in self._tiles:
            tile.give_handler()

        # Start the game with player1
        self.game_cycle("1")

    def game_cycle(self, player_id):
        """ The main cycle of games, gives each active player turns to go. """

        for player in self._players_list:
            if player.return_id() == player_id:
                current_player = player

        # Display in game prompt for each individual player
        self.show_in_game(current_player)

    def replenish_hand(self, player):
        """ If the current player has a dragon tile and the pile is not empty,
            initiate a refill process for everyone. """

        # Counting how many tiles are in the pile
        pile = 0
        for tile in self._tiles:
            if tile.return_status() == "pile":
                pile += 1

        # If tiles are avaliable when a player has the dragon tile,
        # Return the dragon tile and draw a tile
        if self._dragon.return_status() == player.return_id() and pile > 0:
            self._dragon.change_status("pile")
            self.deal_card(player.return_id())
            pile -= 1

        # If there's are avalible tiles in pile and player's hand has less than
        # 3 tiles, draw a tile
        if self._dragon.return_status() == "pile" and pile > 0:
            tile_counter = 0
            for tile in self._tiles:
                if tile.return_status() == player.return_id():
                    tile_counter += 1

            if tile_counter < 3:
                self.deal_card(player.return_id())

    def show_in_game(self, player):
        """ Show in-game prompt and player's tiles. """

        # Display in-game prompt (playerID's turn and how to place a tile)
        player.display_in_game_prompt()

        # Check conditions to see if there's avalible tiles for player
        self.replenish_hand(player)

        # Display player's tiles
        self.display_hand(player.return_id(), 10)

    def hide_in_game(self, player_id):
        """ Hide in-game prompt and player's tiles. Trigger movement. """

        # Find the current player
        for player in self._players_list:
            if player.return_id() == player_id:
                current_player = player

        # Hide the prompt and hand for this player
        current_player.hide_in_game_prompt()
        self.hide_hand(player_id)

        # Deal additional card:
        self.deal_card(player_id)

        # Move player markers and update the list for players still in the game
        self.move_markers()
        self.update_active_player_list()

        # Check number of active players left, and decide win/tie/continue
        players_count = len(self._active_players)
        if  players_count == 0:
            tie(self._win)
        elif players_count == 1:
            winner(self._win, self._active_players[0].return_id())
        else:

            # Find who should be the next to go after the current player
            index_counter = self._players_list.index(current_player)
            index_counter += 1
            temp_list = []
            while index_counter < len(self._players_list):
                if self._players_list[index_counter].still_in():
                    temp_list.append(self._players_list[index_counter])
                    index_counter += 1

            temp_len = len(temp_list)
            if temp_len == 0:
                self.game_cycle(self._active_players[0].return_id())
            else:
                self.game_cycle(temp_list[0].return_id())

    def move_markers(self):
        """ Check to see if players marker can move and if this move will
            eliminate these players. """

        for player in self._active_players:

            # Check both dicationary to see if player can move
            while self.moveable1(player) or self.moveable2(player):

                # If a moveable, mathing coordinate is found in dicationary1
                if self.moveable1(player) and not self.moveable2(player):
                    new_loc = self._loc_dict1[player.return_current_loc()]
                    player.move_player(new_loc)
                    player.update_location(new_loc)

                # If a moveable, mathing coordinate is found in dicationary1
                if self.moveable2(player) and not self.moveable1(player):
                    new_loc = self._loc_dict2[player.return_current_loc()]
                    player.move_player(new_loc)
                    player.update_location(new_loc)

            # Check if any player is eliminated
            self.check_elimination(player)

    def check_elimination(self, player):
        """ Check if a player is eliminated, put back all the unused tiles. """

        # Make sure we are not eliminating players before their first turn
        if player.return_current_loc() in player.return_border() and \
            len(player.hist()) != 1:
            player.eliminated()

            # "Put back" all the tiles of this player to the pile
            for tile in self._all_tiles:
                if tile.return_status() == player.return_id():
                    tile.change_status("pile")

    def moveable1(self, player):
        """ Return a boolean for if loc_dict1 has key matching the location. """

        if self._loc_dict1.get(player.return_current_loc(), 'no') != 'no' and \
            self._loc_dict1[player.return_current_loc()] not in player.hist():
            return True

        return False

    def moveable2(self, player):
        """ Return a boolean for if loc_dict2 has key matching the location. """

        if self._loc_dict2.get(player.return_current_loc(), 'no') != 'no' and \
            self._loc_dict2[player.return_current_loc()] not in player.hist():
            return True

        return False

    def make_players(self, num):
        """ Make players based on popup (1-8), though we can't play with 1. """

        for counts in range(num):
            self._players_list.append(Player(self._win, counts, self))
        self.update_active_player_list()

        # Deal 3 tiles to each player
        for _ in range(3):
            for player in self._active_players:
                self.deal_card(player.return_id())

        # Show player's hand so they can better decide where to start
        for player in self._active_players:
            self.display_hand(player.return_id(), 15 + int(player.return_id()))

    def update_active_player_list(self):
        """ Update the list to all players still in the game. """

        self._active_players = []
        for player in self._players_list:
            if player.still_in():
                self._active_players.append(player)

    def deal_card(self, player_id):
        """ Deal card to players. """

        # Make a list for tiles that can be drawn from the pile
        avaliable_tiles = [
            tile for tile in self._tiles if tile.return_status() == "pile"]

        if avaliable_tiles:
            chosen_t = choice(avaliable_tiles)
            chosen_t.change_status(player_id)
        else:
            if self._dragon.return_status() == "pile":
                self._dragon.change_status(player_id)

    def display_hand(self, player_id, depth):
        """ Display the player's hand. """

        # Locations to show the tiles depends on how many the players has
        tile_3_loc = [(950, 400), (1100, 400), (1250, 400)]
        tile_2_loc = [(1000, 400), (1200, 400)]
        tile_1_loc = (1100, 400)

        tiles = [t for t in self._all_tiles if t.return_status() == player_id]
        for tile in tiles:
            tile.change_depth(depth)

        if len(tiles) == 3:
            for n_var in range(3):
                tiles[n_var].move_location(tile_3_loc[n_var])

        if len(tiles) == 2:
            for n_var in range(2):
                tiles[n_var].move_location(tile_2_loc[n_var])

        if len(tiles) == 1:
            tiles[0].move_location(tile_1_loc)

    def hide_hand(self, player_id):
        """ Hide given player's hand of tiles. """

        hidden_loc = (-400, -400)

        for tile in self._all_tiles:
            if tile.return_status() == player_id:
                tile.change_depth(30)
                tile.move_location(hidden_loc)

    def display_initial_view(self):
        """ Display the prompt window for intial marker selection. """

        self._initial_msg[0].move_to((1100, 380))
        self._initial_msg[1].move_to((1100, 330))

    def remove_initial_view(self):
        """ Remove the inital prompt window. """

        for element in self._initial_msg:
            self._win.remove(element)

    def initial_view(self):
        """ Make a window to prompt players to look at their tiles. """

        ract = Rectangle(self._win, 500, 200, (-1100, 380))
        ract.set_fill_color(self._parchment)
        ract.set_border_color(self._ink)
        ract.set_depth(46)
        txt = "Please view your starting tiles and choose a starting location! "
        msg = Text(self._win, txt, 12, (-1100, 330))
        msg.set_depth(45)
        box = [ract, msg]
        for element in box:
            self._win.add(element)

        return box

    def last_on_the_list(self, player_id):
        """ Return true if this player is the last player on the list. """

        return self._active_players[-1].return_id() == player_id

    def send_tile_to_me(self, cell):
        """ Sends a clicked Tile (if there is one) to this Cell object. """

        tile = self.get_clicked_tile()
        if tile is not None:
            if self.legal_placement(cell, tile):
                current_player_id = tile.return_status()

                # This is a extra line just to keep warning signs off the screen
                self.hide_warning_tile_placement()
                self.move_tile_to_cell(tile, cell)

                # Create a layer so this particular cell becomes unclickable
                cell.create_unclickable_layer()

                # Hide prompts, the called method start turn for the next player
                self.hide_in_game(current_player_id)
            else:
                self.show_warning_tile_placement()

    def get_clicked_tile(self):
        """ Return a Tile object, if one is clicked. """

        for tile in self._tiles:
            if tile.is_clicked():
                return tile
        return None

    def legal_placement(self, cell, tile):
        """ Check if the target location is next to this player's marker. """

        # Get this player's piece/marker location
        player_id = tile.return_status()
        for player in self._players_list:
            if player_id == player.return_id():
                marker_location = player.return_current_loc()

        # Get this cell's location
        target_loc = cell.get_location()
        possible_loc = []
        for shift in [(-17, -50), (16, -50), (-50, -17), (50, -17), (-50, 16), \
            (50, 16), (-17, 50), (16, 50)]:
            possible_loc.append(tuple(map(sum, zip(target_loc, shift))))

        # Check to see if marker's location is on any side of the cell
        if marker_location in possible_loc:
            return True

        return False

    def unclick_all_other(self, tile_id):
        """ When one tile is clicked, unclick all other tiles in the list. """

        for tile in self._tiles:
            if tile.return_image_id() != tile_id:
                tile.change_clicked()

    def move_tile_to_cell(self, tile, cell):
        """ Move the given tile object to the location of the cell object, and
            trigger all subsequent events. This is 'one move' of a player. """

        location = cell.get_location()
        tile.move_location(location)
        tile.set_still()

        # Call on method to trigger passing of location logic from tile to game
        self.update_loc_dict(tile.return_coord(), location)

    def update_loc_dict(self, coord, center):
        """ Use coordinate from the tile, update location dicationary. """

        logic_list = [(-17, -50), (16, -50), (-50, -17), (50, -17)] +\
            [(-50, 16), (50, 16), (-17, 50), (16, 50)]
        for pairs in coord:
            location_a = tuple(map(sum, zip(center, logic_list[pairs[0] - 1])))
            location_b = tuple(map(sum, zip(center, logic_list[pairs[1] - 1])))

            # 2 dicationaries-every spot on the graph can leads to 2 other spots
            if self._loc_dict1.get(location_a, "no_value") != "no_value":
                self._loc_dict2[location_a] = location_b
            else:
                self._loc_dict1[location_a] = location_b

            if self._loc_dict1.get(location_b, "no_value") != "no_value":
                self._loc_dict2[location_b] = location_a
            else:
                self._loc_dict1[location_b] = location_a

    def no_overlap(self, location):
        """ In game setup check if this location is overlapping with others. """

        for player in self._players_list:
            if player.return_current_loc() == location:
                return False

        return True

    def show_warning_overlap(self):
        """ Show warning that prevent players to overlap their markers. """

        for element in self._warn_overlap:
            element.move_to((1100, 600))

    def hide_warning_overlap(self):
        """ Hide the overlaps warning. """

        for element in self._warn_overlap:
            element.move_to((-1100, -600))

    def show_warning_tile_placement(self):
        """ Show warning that prevent players to overlap their markers. """

        for element in self._warn_placement:
            element.move_to((1100, 600))

    def hide_warning_tile_placement(self):
        """ Hide the overlaps warning. """

        for element in self._warn_placement:
            element.move_to((-1100, -600))


class Cell(EventHandler):
    """ Cells on the board and can provide a move_to location for the tile. """

    def __init__(self, win, game, location):
        """ The Constructor for Tile class. """

        EventHandler.__init__(self)

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


class Tile(EventHandler):
    """ Tile class that interactive and carries the location logic. """

    def __init__(self, win, game, number, coord):
        """ The Constructor for Tile class. """

        EventHandler.__init__(self)

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


class Popup:
    """ Popup to ask the amount of players. """

    def __init__(self, win, game):
        """ The Constructor for Popup class. """

        self._game = game
        self._win = win
        self._center = (1150, 400)

        self._popup = []
        self._popup_window = Rectangle(self._win, 550, 400, self._center)
        self._popup_window.set_fill_color('#efe2c2')  # parchment panel
        self._popup_window.set_border_color('#5a4a3b')  # ink border
        self._popup_window.set_depth(10)
        self._popup.append(self._popup_window)
        self._message1 = "Please choose the number of players (2-8): "
        self._text1 = Text(self._win, self._message1, 17, (1150, 312.5))
        self._text1.set_depth(9)
        self._popup.append(self._text1)
        self._message2 = "Welcome to Tsuro!"
        self._text2 = Text(self._win, self._message2, 20, (1150, 250))
        self._text2.set_depth(9)
        self._popup.append(self._text2)

        for entry in self._popup:
            self._win.add(entry)

        self._clickables = []
        ctr_list = [(962, 400), (1087, 400), (1212, 400), (1337, 400)] + \
            [(962, 500), (1087, 500), (1212, 500), (1337, 500)]
        # Neutral parchment buttons for all counts (remove bright colors)
        col_list = ['#e8dec5'] * 8

        # Only allow 2-8 players (remove 1-player option)
        for num in range(7):  # indices 0..6
            n = num + 2       # labels 2..8
            self._clickables.append(
                Popupclicks(self._win, self, ctr_list[num], col_list[num], n))

    def report_number(self, number):
        """ Give the Game class a feedback on player counts. """

        # Calls the game to make players
        self._game.make_players(number)

        # Now that the popup will be removed, display the initial prompt
        # for viewing starting tiles and choosing starting locations.
        self._game.display_initial_view()

        # Remove everything in this popup
        for element in self._clickables:
            element.remove_it()
        for element in self._popup:
            self._win.remove(element)


class Popupclicks(EventHandler):
    """ Clickable Objects on the popups. """

    def __init__(self, win, popup, center, color, no):
        """ The Constructor for Popup class. """

        EventHandler.__init__(self)

        self._win = win
        self._popup = popup
        self._id = no

        self._box = Square(self._win, 60, center)
        self._box.set_fill_color(color)
        self._box.set_border_color('#5a4a3b')
        self._box.set_border_width(2)
        self._box.set_depth(8)
        self._text = Text(self._win, str(self._id), 15, center)
        self._text.set_depth(7)
        self._objects = [self._box, self._text]

        for element in self._objects:
            self._win.add(element)

        for element in self._objects:
            element.add_handler(self)

    def handle_mouse_press(self, event):
        """ When clicking, give the Popup class a feedback on player counts. """

        self._popup.report_number(self._id)

    def remove_it(self):
        """ Remove the clickable box and text. """

        for entry in self._objects:
            self._win.remove(entry)


class Player(EventHandler):
    """ Player class that controls the movement of markers on the board. """

    def __init__(self, win, number, game):
        """ The Constructor for Player class. """

        EventHandler.__init__(self)

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


def winner(win, player_id):
    """ Announce the winner. """

    # Winner message "window"
    box_winner = Rectangle(win, 400, 40, (1100, 400))
    box_winner.set_fill_color('#efe2c2')
    box_winner.set_border_color('#5a4a3b')
    box_winner.set_depth(2)
    # box_winner.set_fill_color("black")
    win.add(box_winner)

    # Winner message text that matches that player's color
    color_list = ['#3b3b3b','#5c5346','#2f5d43','#2d4f6c',
        '#7a3f2c','#8a6b2f','#4a5568','#5e3a4a']
    txt = "Player " + player_id + " is the winner! Congratulations!"
    msg_winner = Text(win, txt, 14, (1100, 400))
    # msg_winner.set_color(color_list[int(player_id) - 1])
    msg_winner.set_depth(1)
    win.add(msg_winner)


def tie(win):
    """ Message for a tied game. """

    box_tie = Rectangle(win, 300, 40, (1100, 400))
    box_tie.set_fill_color('#efe2c2')
    box_tie.set_border_color('#5a4a3b')
    box_tie.set_depth(2)
    win.add(box_tie)
    msg_tie = Text(win, "It's a tie! No winner...", 20, (1100, 400))
    msg_tie.set_depth(1)
    win.add(msg_tie)