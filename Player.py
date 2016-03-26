from GamePiece import *
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty

class Player(Widget):
    pieces_left_to_be_placed = NumericProperty(40)

    def __init__(self, color):
        self.color = color
        self.pieces = []


        for piecenumber in pieceamounts:
            for i in range(pieceamounts[piecenumber]):
                temp = GamePiece(piecenumber, self.color)
                self.pieces.append(temp)
                if self.color == "Red":
                    temp.reveal_image()
                else:
                    temp.hide_image()


    def activate_player_pieces(self):
        for piece in self.pieces:
            if not piece.dead:
                piece.disabled = False
                piece.state = "normal"

    def disable_player_pieces(self):
        for piece in self.pieces:
            piece.disabled = True

