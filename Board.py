from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty
from ResizeBehavior import *

from Square import *

from GamePiece import *
from Player import *



class Board(GridLayout):
    def __init__(self, **kwargs):
        super().__init__()
        self.grid = []


    def add_square_to_grid(self, row, square):
        #add to grid @ row and add widget to graphics
        self.grid[row].append(square)
        self.add_widget(square)


class SideBoard(Board):
    def __init__(self, **kwargs):
        super().__init__()
        #self.player = super.player
        self.cols = 4
        self.create_squares()


    def create_squares(self):
        for i in range(10):
            self.grid.append([])
            for j in range(4):
                temp = Square(i,j, "sideboard")
                self.add_square_to_grid(i,temp)

                #debug
                #temp.bind(occupied = temp.test_occupied)

class GameBoard(Board):
    def __init__(self, **kwargs):
        super().__init__()
        self.cols = 10
        self.create_squares()


    def create_squares(self):
        for i in range(10):
            self.grid.append([])
            for j in range(self.cols):
                if i in (4,5) and j in (2,3,6,7):
                    temp = Square(i,j, "water")
                else:
                    temp = Square(i,j, "land")
                self.add_square_to_grid(i,temp)

                #debug
                #temp.bind(occupied = temp.test_occupied)


    def highlight_valid_game_setup_rows(self):
        '''activates the appropriate rows for each player'''
        if self.activeplayer.color == "Red":
            toprow = 6
            bottomrow = 9
        else:
            toprow = 0
            bottomrow = 3
        for square in self.children:
            if square.row in range(toprow, bottomrow+1):
                square.valid = True
            else:
                square.valid = False
        self.enable_valid_squares()




    def highlight_valid_moves_during_game(self, piece, *args):
        if piece.max_spaces == 0:
            return

        self.find_x_moves(piece, 1)
        self.find_x_moves(piece, -1)
        self.find_y_moves(piece, 1)
        self.find_y_moves(piece, -1)
        self.enable_valid_squares()

    def clear_all_valid_markers(self):
        for square in self.children:
            if square.occupied is not None and square.valid and \
                    not self.piece_belongs_to_activeplayer(square.occupied):
                square.occupied.disabled = True
            square.disabled = True
            square.valid = False

    def enable_valid_squares(self):
        for square in self.children:
            if square.valid:
                square.disabled = False
                if square.occupied is not None:
                    square.occupied.disabled = False

            else:
                square.disabled = True

    def test_for_valid_square(self, square):
        #debug
        #if square.occupied is not None and not self.piece_belongs_to_activeplayer(square.occupied):
            #print("detected", square.occupied.id)

        if square.type == "land":
            if square.occupied is None or \
                not self.piece_belongs_to_activeplayer(square.occupied):
                return True
        return False

    def find_y_moves(self, piece, direction):
        '''direction: 1 is down, -1 is up. Goes through squares in that direction and marks the valid ones.
        Stops if it comes to an invalid square.'''
        for n in range(1, piece.max_spaces+1):
            newrow = piece.spot.row + n*direction
            if not 0 <= newrow <= 9:
                break
            else:
                possible_square = self.grid[newrow][piece.spot.col]
            if not self.test_for_valid_square(possible_square):
                   break
            else:
                possible_square.valid = True
                if possible_square.occupied is not None:
                    break


    def find_x_moves(self, piece, direction):
        '''direction: 1 is right, -1 is left. Goes through squares in that direction and marks the valid ones.
        Stops if it comes to an invalid square.'''
        for n in range(1, piece.max_spaces+1):
            newcol = piece.spot.col + n*direction
            if not 0 <= newcol <= 9:
                break
            else:
                possible_square = self.grid[piece.spot.row][newcol]
            if not self.test_for_valid_square(possible_square):
                   break
            else:
                possible_square.valid = True
                if possible_square.occupied is not None:
                    break



    def piece_belongs_to_activeplayer(self, piece):
        if piece.player_color == self.activeplayer.color:
            return True
        return False








