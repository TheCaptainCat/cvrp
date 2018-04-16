import random

from cvrp.logic import Edge


class Route:
    def __init__(self):
        self.vertices = []
        self.edges = []

    def random_path(self):
        if len(self.vertices) == 0:
            return
        vertex = self.vertices[0]
        vertices = set()
        for v in self.vertices:
            if v.id != 0:
                vertices.add(v)
        while len(vertices) > 0:
            r_vertex = random.choice(list(vertices))
            vertices.remove(r_vertex)
            self.edges.append(Edge(vertex, r_vertex))
            vertex = r_vertex
        self.edges.append(Edge(vertex, self.vertices[0]))

    @property
    def quantity(self):
        return sum(v.qt for v in self.vertices)

    @property
    def distance(self):
        return sum(e.distance for e in self.edges)

    def find_edges_by_vertex(self, vertex):
        e1 = [e for e in self.edges if e.v2 == vertex]
        e2 = [e for e in self.edges if e.v1 == vertex]
        return e1[0], e2[0]

    def __repr__(self):
        return f'Route ({len(self.vertices)} vertices) (distance: {self.distance}) (quantity: {self.quantity})'

    def remove_vertex(self, vertex):
        self.vertices.remove(vertex)

    def remove_edge(self, edge):
        self.edges.remove(edge)

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def add_edge(self, edge):
        self.edges.append(edge)
