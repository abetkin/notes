

from .points import make_points

class Iterator:

    def __init__(self, text):
        self.text = text
        self.points = make_points(text)

    def on_regular(self, point):
        1
    
    def on_x_z(self, point):
        # return new point
        # F depends on diagonal length
        1
    
    def process(self):
        for point in self.points:
            if point['type'] == 1:
                self.on_regular(point)
                continue
            assert point['type'] == 2
            p = self.on_x_z(point)
            self.render_point(p)

    def render_point(self, p):
        line = f"X{self.X} Z{self.Z} R{self.R} F{self.F}"
        self.text[self.start:self.end] = line