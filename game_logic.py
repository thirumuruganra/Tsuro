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

        # Import dependencies for other classes
        from tiles import Tile, Dragon
        from cells import Cell
        from ui_components import Popup

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

        # Import winner/tie functions
        from ui_components import winner, tie

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

        from players import Player

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
