from arcadegraphics import *


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


class Popupclicks():
    """ Clickable Objects on the popups. """

    def __init__(self, win, popup, center, color, no):
        """ The Constructor for Popup class. """

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
