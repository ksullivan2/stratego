from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ObjectProperty, OptionProperty
from kivy.graphics.instructions import *
from Popups import *
from kivy.clock import Clock


from random import randint


from ResizeBehavior import *
from functools import partial
from Square import *
from GamePiece import *
from Board import *
from Player import *
from EventHandler import *
from GameState import *


class StrategoGame(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__()

        #create aliases for children widgets
        self.board = self.ids["board"]
        self.sidebar = self.ids["sidebar"]

        #gamestatus
        self.activeplayer = None
        self.pieceinhand = None
        self.gamestate = GameState.start_popup
        self.winner = None

        #set up event handlers for all relevant widgets
        self.eventsobject = Controller(self)
        self.board.eventsobject = self.eventsobject
        self.sidebar.eventsobject = self.eventsobject

       #players are now created after initialization to ease up the memory load

        self.create_start_game_popup()

#gamestate actions

    def change_gamestate(self, newstate):

        #debug
        #print("swap", self.gamestate, "to", newstate)

        self.gamestate = newstate

        if self.gamestate == GameState.player_setup:
            #create new players has been moved to here to ease up memory load
            if self.activeplayer is None:
                self.create_new_players()

            self.player_start()

            if self.activeplayer.color == "Red":
                self.board.highlight_valid_game_setup_rows()
                self.create_place_pieces_popup()
                self.change_gamestate(GameState.setup_no_piece)
            else:
                self.quick_place_pieces()
                self.swap_active_player()
                self.change_gamestate(GameState.gameplay_no_piece)

        elif self.gamestate == GameState.setup_no_piece:
            self.activeplayer.activate_player_pieces()

        elif self.gamestate == GameState.pieces_placed:
            for slot in self.sidebar.children:
                slot.disabled = True
            self.change_gamestate(GameState.gameplay_no_piece)
            self.swap_active_player()


        elif self.gamestate == GameState.gameplay_no_piece:
            self.board.clear_all_valid_markers()


        elif self.gamestate == GameState.game_selected_piece:
            self.board.highlight_valid_moves_during_game(self.pieceinhand)

        elif self.gamestate == GameState.conflict:
            self.board.clear_all_valid_markers()

        elif self.gamestate == GameState.win:
            self.win_popup(self.winner)

            #remove player widgets and unoccupy squares
            for piece in self.player1.pieces:
                self.remove_widget(piece)
            for piece in self.player2.pieces:
                self.remove_widget(piece)
            for square in self.board.children:
                square.occupied = None
            for square in self.sidebar.children:
                square.occupied = None

            #clear winner property and sets activeplayer to none so player setup will create new ones
            self.winner = None
            self.activeplayer = None


    def swap_active_player(self):
        self.activeplayer.disable_player_pieces()
        if self.activeplayer == self.player1:
            self.activeplayer = self.player2
        else:
            self.activeplayer = self.player1
        #make sure the board knows the new player too...
        self.board.activeplayer = self.activeplayer

        self.activeplayer.activate_player_pieces()

        #debug
        #print("swap activeplayer to " + self.activeplayer.color)




#interacting with the "hand"
    def place_in_hand(self, piece):
        self.pieceinhand = piece

    def clear_hand(self):
        self.pieceinhand = None


#moving pieces around the board

    def update_pieces_left_to_be_placed(self, square):
        if square.type == "sideboard":
            self.activeplayer.pieces_left_to_be_placed += 1
        else:
            self.activeplayer.pieces_left_to_be_placed -=1

    def move_to_square(self, square, on_complete=None):
        piece = self.pieceinhand

        #disable inactive pieces so the user can't create unwanted input
        for item in self.activeplayer.pieces:
            item.disabled = True
            #don't dim if we're in game setup cause it's annoying
            if self.gamestate == GameState.setup_selected_piece:
                item.state = "down"
            #sets the image to the bright one while still disabling the piece
            elif item == self.pieceinhand:
                item.state = "down"

        #the most recently added piece is highest on Z axis
        #it's really annoying there's no other way to do this
        self.remove_widget(piece)
        self.add_widget(piece)

        #remove it from the previous spot and put it on new one
        piece.spot.occupied = None

        #piece's animation
        piece.moveanim = Animation(pos = square.pos, t = "out_expo", d=.5)
        if on_complete:
            piece.moveanim.bind(on_complete = partial(on_complete, self, square))

        piece.moveanim.start(piece)

        #this is necessary since this method is also used before player conflict
        if square.occupied is None:
            self.officially_place_on_square(square, piece)

    def officially_place_on_square(self, square, piece):
        piece.spot = square
        square.occupied = piece
        piece.state = "normal"

        #debug
        #print(piece.id, square.occupied.id)


    def quick_place_pieces(self, *args):
        if self.activeplayer.color =="Red":
            x = 6
        else:
            x = 0
        y = 0
        templist = []
        for piece in self.activeplayer.pieces:
            if piece.spot.type == "sideboard":
                templist.append(piece)
        while len(templist) > 0:
            if self.board.grid[x][y].occupied is None:
                piece = templist[randint(0,len(templist)-1)]
                self.pieceinhand = piece
                self.move_to_square(self.board.grid[x][y])
                self.officially_place_on_square(self.board.grid[x][y], piece)
                templist.remove(piece)
                self.activeplayer.pieces_left_to_be_placed -= 1
            if y == 9:
                y = 0
                x += 1
            else:
                y += 1


#creating players & pieces
    def create_new_players(self):
        self.player1 = Player("Red")
        self.player2 = Player("Blue")
        self.activeplayer = self.player1
        self.board.activeplayer = self.player1


    def player_start(self):
        '''creates the gamepieces for each player'''

        #initializes the count of how many pieces are left to be placed
        #which will count down to 0
        self.activeplayer.bind(pieces_left_to_be_placed = self.eventsobject.piece_placed)

        for piece, square in zip(self.activeplayer.pieces, self.sidebar.children):
            self.add_widget(piece)
            piece.spot = square
            piece.pos = piece.spot.pos
            piece.size = square.size
            piece.eventsobject = self.eventsobject
            square.occupied = piece



#boolean helper functions
    def pieces_are_all_placed(self, *args):
        if self.activeplayer.pieces_left_to_be_placed > 0:
            return False
        #debug
        # print("pieces placed")

        return True

    def piece_belongs_to_activeplayer(self, piece):
        if piece.player_color == self.activeplayer.color:
            return True
        return False


#conflict

    def player_conflict(self, square):
        '''does the conflict animation, moves winner to square and "kills" loser'''
        attacker = self.pieceinhand
        defender = square.occupied

        winner = None
        loser = None

        #special cases first
        if defender.number == 0:
            self.winner = attacker

        if (attacker.number == 1 and defender.number == 10) or \
                (attacker.number == 3 and defender.number == 11) or \
                (attacker.number >= defender.number):
            winner = attacker
            loser = defender
        else:
            winner = defender
            loser = attacker

        self.officially_place_on_square(square, winner)

        #makes sure that the pieces are at the top of the Z axis
        self.remove_widget(loser)
        self.remove_widget(winner)
        self.add_widget(loser)
        self.add_widget(winner)

        #attacker goes in positive direction, defender in -1
        #then pass in boolean for if they won
        attacker.conflictanim = attacker.conflict_animation(attacker, 1, winner==attacker)
        defender.conflictanim = defender.conflict_animation(defender, -1, winner==defender)
        winner.conflictanim.start(winner)
        loser.conflictanim.start(loser)


    def piece_death(self, instance, piece, *args):
        #debug
        # print(piece.number, "dead")

        #kill the beast! (umm... piece...)
        piece.dead = True

        #find an empty slot on the sidebar.
        #there are not enough slots.... fix this later
        deadslot = None
        for slot in self.sidebar.children:
            if slot.occupied is None:
                deadslot = slot
                break

        piece.disabled = True
        piece.state = "normal"

        #piece's animation
        piece.moveanim = Animation(pos = deadslot.pos, t = "out_expo")
        piece.moveanim.start(piece)

        self.officially_place_on_square(deadslot, piece)


#creating popups
    def create_start_game_popup(self):
        self.startpopup = Popup()
        self.startpopup.center = 600,700
        #apparently the widgets aren't sized yet when this is run, need to fix
        #self.center = (self.center_x, self.center_y + self.board.height/2)
        self.startpopup.instructions = "Test your mettle in a game of strategy and cunning!"
        self.startpopup.startbuttontext = "Start a new game!"
        self.startpopup.buttonpress = self.eventsobject.start_game_button_press
        self.add_widget(self.startpopup)


    def create_place_pieces_popup(self):
        self.pp_popup = Popup(title = "Instructions", size = (1000,800))
        self.pp_popup.center = (self.board.center_x, self.board.center_y)
        self.pp_popup.instructions = "The purpose of the game is to capture your opponent's flag.\n" \
                                    "Place your pieces on the highlighted squares in a strategic formation.\n\n" \
                                    "RULES:\nHigher numbered pieces capture lower pieces.\nAttacker wins in a tie.\n" \
                                    "3s can defuse bombs.\n2s can move unlimited spaces.\n" \
                                    "1s are Spies and can capture 10s only if the Spy attacks."

        self.pp_popup.startbuttontext = "Got it!"
        self.pp_popup.buttonpress = partial(self.remove_widget, self.pp_popup)

        self.qpp_button = Button(text= "Impatient? Click to randomly place the rest of your pieces.",
                               on_press = self.quick_place_pieces_callback, pos = (self.board.center_x -
                                self.pp_popup.width/2, self.board.center_y),
                                 size_hint = (None, None), size = (self.pp_popup.width, 100))

        self.add_widget(self.qpp_button)
        self.add_widget(self.pp_popup)

    def quick_place_pieces_callback(self, *args):
        self.quick_place_pieces()
        self.remove_widget(self.qpp_button)


    def create_ready_popup(self):
        self.readypopup = Popup(title = "Ready to Play?")
        self.readypopup.center = (self.board.center_x, self.board.center_y + self.board.height/4)
        self.readypopup.instructions = "If you're happy with your formation, click Play."
        self.readypopup.startbuttontext = "PLAY STRATEGO!"
        self.readypopup.buttonpress = self.ready_callback
        self.readypopup.ids["layout"].add_widget(Button(text = "Not yet", on_press = self.not_yet_callback,
                                                 size_hint_y = 1/3))
        self.add_widget(self.readypopup)

    def not_yet_callback(self, *args):
        self.remove_widget(self.readypopup)
        self.change_gamestate(GameState.setup_no_piece)

    def ready_callback(self, *args):
        self.remove_widget(self.readypopup)
        self.swap_active_player()
        self.change_gamestate(GameState.player_setup)

    def win_popup(self, winner):
        self.winpopup = Popup()
        self.winpopup.center = 600,700
        #apparently the widgets aren't size yet when this is run, need to fix
        #self.center = (self.center_x, self.center_y + self.board.height/2)
        self.winpopup.instructions = self.winner.player_color + " won the game!"
        self.winpopup.startbuttontext = "Start a new game!"
        self.winpopup.buttonpress = self.eventsobject.start_game_button_press
        self.add_widget(self.winpopup)