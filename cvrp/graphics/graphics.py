from cvrp.graphics.colors import generate_new_color

from OpenGL.GL import *


class Graphics:
    def __init__(self, graph):
        self.graph = graph
        self.colors = {}
        for i in range(0, len(self.graph.routes) + 1):
            self.colors[i] = generate_new_color(self.colors.values(), pastel_factor=0.01)

    def draw(self):
        def draw_line(v1, v2):
            glVertex2f(v1.x, v1.y)
            glVertex2f(v2.x, v2.y)

        glPointSize(10)
        glBegin(GL_POINTS)

        glColor3f(1.0, 0.0, 0.0)
        glVertex2f(self.graph.home.x, self.graph.home.y)
        glColor3f(1.0, 1.0, 1.0)
        for v in self.graph.vertices:
            vertex = self.graph.vertices[v]
            glVertex2f(vertex.x, vertex.y)
        glEnd()

        glPointSize(1)
        glBegin(GL_LINES)
        for i in range(0, len(self.graph.routes)):
            route = self.graph.routes[i]
            if len(route) == 0:
                continue
            glColor3fv(self.colors[i])
            draw_line(self.graph.home, self.graph.vertices[route[0]])
            for j in range(1, len(route)):
                draw_line(self.graph.vertices[route[j - 1]], self.graph.vertices[route[j]])
            draw_line(self.graph.vertices[route[len(route) - 1]], self.graph.home)
            glColor3f(1.0, 1.0, 1.0)
        glEnd()
