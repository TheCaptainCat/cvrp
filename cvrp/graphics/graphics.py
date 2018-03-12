from cvrp.graphics import Point, Line
from cvrp.graphics.colors import generate_new_color

from OpenGL.GL import *


class Graphics:
    def __init__(self, graph):
        self.graph = graph
        self.points = []
        self.lines = []
        self.colors = {}
        for i in graph.vertices:
            self.points.append(Point(graph.vertices[i]))
        for route in graph.routes:
            edges = []
            for edge in route.edges:
                edges.append(Line(edge))
            self.lines.append(edges)
            self.colors[self.lines.index(edges)] = generate_new_color(self.colors.values(), pastel_factor=0.01)

    def draw(self):
        glPointSize(10)
        glBegin(GL_POINTS)
        for point in self.points:
            point.draw()
        glEnd()
        glPointSize(1)
        glBegin(GL_LINES)
        for lines in self.lines:
            glColor3fv(self.colors[self.lines.index(lines)])
            for line in lines:
                line.draw()
            glColor3f(1.0, 1.0, 1.0)
        glEnd()
