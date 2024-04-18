from manim import *
from math import *

import numpy as np

def point(angle):
    xx = 2 * sin(angle)
    yy = 2 * cos(angle)
    return (xx, yy)

class SimplePendulum(Scene):
    def construct(self):
        delta_t = 0.02
        y = np.array([0.0,1.0])
        a = 0.0
        time  = np.arange(0,0.2,delta_t)

        for t in time:
            a += 0.1
            pos_xy = point(a)

            dot = Dot(point=np.array([-pos_xy[0],-pos_xy[1],0.0]),radius=0.2,color=BLUE)
            line = Line([0,0,0],[-pos_xy[0],-pos_xy[1],0],color=BLUE)

            self.add(line)
            self.add(dot)
            self.wait(0.1)
            self.remove(line)
            self.remove(dot)