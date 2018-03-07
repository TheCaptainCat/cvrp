from cvrp.graphics import Point, Line

from OpenGL.GL import *


class Graphics:
    def __init__(self, route):
        self.route = route
        self.points = []
        self.lines = []
        for i in route.vertices:
            self.points.append(Point(route.vertices[i]))
        for edge in route.edges:
            self.lines.append(Line(edge))

    def draw(self):
        glPointSize(10)
        glBegin(GL_POINTS)
        for point in self.points:
            point.draw()
        glEnd()
        glPointSize(1)
        glBegin(GL_LINES)
        for line in self.lines:
            line.draw()
        glEnd()
