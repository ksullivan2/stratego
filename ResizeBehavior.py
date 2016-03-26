#each object that uses this method must have a numeric property called ratio
from kivy.properties import NumericProperty


class ResizeBehavior():
    ratio = NumericProperty()

    def do_layout(self, *args):
        for child in self.children:
            self.apply_ratio(child)
        super(ResizeBehavior, self).do_layout()

    def apply_ratio(self, child):
        # ensure the child don't have specification we don't want
        child.size_hint = None, None
        child.pos_hint = {"center_x": .5, "center_y": .5}

        # calculate the new size, ensure one axis doesn't go out of the bounds
        w, h = self.size
        h2 = w * self.ratio
        if h2 > self.height:
            w = h / self.ratio
        else:
            h = h2
        child.size = w, h