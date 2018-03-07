from cvrp.graphics import Point

from OpenGL.GL import *


class Graph:
    def __init__(self, vertices):
        self.points = []
        for i in vertices:
            self.points.append(Point(vertices[i]))

    def draw(self):
        glPointSize(10)
        glBegin(GL_POINTS)
        for point in self.points:
            point.draw()
        glEnd()
