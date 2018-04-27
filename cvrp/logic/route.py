import random

from cvrp.logic import Edge


class Route:
    def __init__(self, home):
        self.vertices = []
        self.home_vertex = home
        self.first_vertex = None
        self.last_vertex = None

    def random_path(self):
        vertex = self.home_vertex
        vertices = set()
        for v in self.vertices:
            if v.id != 0:
                vertices.add(v)
        while len(vertices) > 0:
            r_vertex = random.choice(list(vertices))
            r_vertex.route = self
            if vertex.id == 0:
                self.first_vertex = r_vertex
            vertices.remove(r_vertex)
            e = Edge(vertex, r_vertex)
            if vertex.id != 0:
                vertex.edge_out = e
            r_vertex.edge_in = e
            vertex = r_vertex
        vertex.edge_out = Edge(vertex, self.home_vertex)
        self.last_vertex = vertex

    @property
    def quantity(self):
        s = 0
        v = self.first_vertex
        while v.id != 0:
            s += v.qt
            v = v.edge_out.v2
        return s

    @property
    def distance(self):
        s = 0
        v = self.first_vertex
        s += self.first_vertex.edge_in.distance
        while v.id != 0:
            s += v.edge_out.distance
            v = v.edge_out.v2
        return s

    @property
    def first_edge(self):
        return self.first_vertex.edge_in

    def __repr__(self):
        return f'Route ({len(self.vertices)} vertices) (distance: {self.distance}) (quantity: {self.quantity})'

    def remove_vertex(self, vertex):
        self.vertices.remove(vertex)

    def add_vertex(self, vertex):
        self.vertices.append(vertex)
