from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ObjectProperty
from kivy.animation import Animation
from math import sin, cos
from functools import partial
from ResizeBehavior import *


class GamePiece(ToggleButton):
    spot = ObjectProperty(None)

    def __init__(self, number, color, **kwargs):
        self.number = number
        self.player_color = color
        self.id = self.player_color + str(self.number)
        self.dead = False
        self.moveanim = Animation()

        #scouts can move more than 1 space, flags/bombs can't move
        if self.number == 2:
            self.max_spaces = 9
        elif self.number in (0,11):
            self.max_spaces = 0
        else:
            self.max_spaces = 1
        super(GamePiece, self).__init__()


    def get_name(self):
        return names[self.number]

    def reveal_image(self):
        self.background_normal = "images/" + self.player_color + "/normal/" + str(self.number) + ".png"
        self.background_down = "images/" + self.player_color + "/down/" + str(self.number) + ".png"
        self.background_disabled_normal = "images/" + self.player_color + "/disabled/" + str(self.number) + ".png"

        #this state will only be used for movement, so I use the bright color but disable the button
        self.background_disabled_down = "images/" + self.player_color + "/normal/" + str(self.number) + ".png"

        #turns the opacity on the number in a circle back to 1
        self.ids["layout"].opacity = 1
        self.ids["number"].opacity = 1



    def hide_image(self):
        self.background_normal = "images/" + self.player_color + "/normal/back.png"
        self.background_down = "images/" + self.player_color + "/down/back.png"
        self.background_disabled_normal = "images/" + self.player_color + "/disabled/back.png"

        #this state will only be used for movement, so I use the bright color but disable the button
        self.background_disabled_down = "images/" + self.player_color + "/normal/back.png"

        #turns the opacity on the number in a circle down to 0
        self.ids["layout"].opacity = 0
        self.ids["number"].opacity = 0

    def conflict_animation(self, instance, direction, won):
        '''first the pieces circle each other, then "joust" at each other
        direction is 1 for winner, -1 for loser'''

        #make sure they look bright, but are actually disabled
        instance.state = "down"
        instance.disabled = True

        #circle animation
        radius = 100*direction
        xcenter, ycenter = self.pos

        #current angle IN RADIANS
        #6.28319 radians in 360 degress
        #starts at 90 deg
        angle = 1.57

        #speed IN RADIANS per frame
        speed = .25

        anim = Animation(pos = (xcenter + radius, ycenter), d = .1)


        while angle < 6.28+1.57:
            newx = radius * sin(angle) + xcenter
            newy = radius * cos(angle) + ycenter

            anim += Animation(pos = (newx,newy), d = .03)
            angle += speed

        anim.bind(on_complete = partial(self.conflict_anim_p2, instance, direction, radius, xcenter, ycenter, won))
        return anim


    def conflict_anim_p2(self, instance, direction, radius, xcenter, ycenter, won, *args):
        '''has to be separate because of the image switch'''

        self.reveal_image()
        self.ids["layout"].opacity = 1

        anim = Animation(pos = (xcenter - radius , ycenter + radius/2), t = "in_out_back")
        anim += Animation(pos = (xcenter + radius , ycenter - radius/2), t = "in_out_back")


        if won:
            anim.bind(on_complete = (partial(self.winner_animation)))
        else:
            anim.bind(on_complete = (partial(self.loser_animation)))

        anim.start(instance)


    def winner_animation(self, *args):
        self.winanim = Animation(size = (self.width*1.5, self.height*1.5), pos = self.spot.pos, t = "out_bounce")
        self.winanim += Animation(size = (self.width, self.height))
        self.winanim.bind(on_complete = self.parent.eventsobject.conflictanim_on_complete)
        self.winanim.start(self)

    def loser_animation(self, *args):
        self.loseanim = Animation(size = (self.width*.75, self.height*.75))
        self.loseanim += Animation(size = (self.width, self.height), d=.1)
        self.loseanim.bind(on_complete = partial(self.parent.piece_death))
        self.loseanim.start(self)





names = {0: "Flag",
         1: "Spy",
         2: "Scout",
         3: "Miner",
         4: "Sergeant",
         5: "Lieutenant",
         6: "Captain",
         7: "Major",
         8: "Colonel",
         9: "General",
         10: "Marshal",
         11: "Bomb"}

pieceamounts = {0: 1,
           1: 1,
           2: 8,
           3: 5,
           4: 4,
           5: 4,
           6: 4,
           7: 3,
           8: 2,
           9: 1,
           10: 1,
           11: 6}

