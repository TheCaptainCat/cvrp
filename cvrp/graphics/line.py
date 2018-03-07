from OpenGL.GL import *


class Line:
    def __init__(self, edge):
        self.edge = edge

    def draw(self):
        glVertex2f(self.edge.v1.x, self.edge.v1.y)
        glVertex2f(self.edge.v2.x, self.edge.v2.y)
