from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.label import Label
from ResizeBehavior import *
from GamePiece import *
from Square import *
from Board import *
from StrategoGame import *




class StrategoApp(App):
    def build(self):
        game = StrategoGame()
        return game



if __name__ == '__main__':
    StrategoApp().run()
