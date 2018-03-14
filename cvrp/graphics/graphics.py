from cvrp.graphics import Point, Path

from OpenGL.GL import *


class Graphics:
    def __init__(self, graph):
        self.graph = graph
        self.points = []
        self.paths = []
        colors = []
        for i in graph.vertices:
            self.points.append(Point(graph.vertices[i]))
        for route in graph.routes:
            path = Path(route, colors)
            self.paths.append(path)
            colors.append(path.color)

    def draw(self):
        glPointSize(10)
        glBegin(GL_POINTS)
        for point in self.points:
            point.draw()
        glEnd()
        glPointSize(1)
        glBegin(GL_LINES)
        for path in self.paths:
            glColor3fv(path.color)
            for line in path.lines:
                line.draw()
            glColor3f(1.0, 1.0, 1.0)
        glEnd()
