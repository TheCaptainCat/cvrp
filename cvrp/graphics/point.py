from OpenGL.GL import *


class Point:
    def __init__(self, vertex):
        self.vertex = vertex

    def draw(self):
        if self.vertex.id == 0:
            glColor3f(1.0, 0.0, 0.0)
        glVertex2f(self.vertex.x, self.vertex.y)
        if self.vertex.id == 0:
            glColor3f(1.0, 1.0, 1.0)

    def __repr__(self):
        return f'Point [{self.vertex.x},{self.vertex.y}]'
