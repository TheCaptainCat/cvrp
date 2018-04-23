from cvrp.graphics.colors import generate_new_color

from OpenGL.GL import *


class Graphics:
    def __init__(self, graph):
        self.graph = graph
        self.colors = {}
        for route in self.graph.routes:
            self.colors[route] = generate_new_color(self.colors.values(), pastel_factor=0.01)

    def draw(self):
        def draw_line(v1, v2):
            glVertex2f(v1.x, v1.y)
            glVertex2f(v2.x, v2.y)

        glPointSize(10)
        glBegin(GL_POINTS)
        for v in self.graph.vertices:
            vertex = self.graph.vertices[v]
            if vertex.id == 0:
                glColor3f(1.0, 0.0, 0.0)
            glVertex2f(vertex.x, vertex.y)
            if vertex.id == 0:
                glColor3f(1.0, 1.0, 1.0)
        glEnd()

        glPointSize(1)
        glBegin(GL_LINES)
        for route in self.graph.routes:
            glColor3fv(self.colors[route])
            vertex = route.first_vertex
            draw_line(vertex.edge_in.v1, vertex.edge_in.v2)
            edge = route.first_vertex.edge_in
            while edge.v2.id != 0:
                draw_line(edge.v1, edge.v2)
                edge = edge.v2.edge_out
            draw_line(edge.v1, edge.v2)
            glColor3f(1.0, 1.0, 1.0)
        glEnd()
