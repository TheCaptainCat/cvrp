import random

from cvrp.logic import Edge


class Route:
    def __init__(self):
        self.vertices = []
        self.edges = []

    def random_path(self):
        vertex = self.vertices[0]
        vertices = set()
        for v in self.vertices.values():
            if v.id != 0:
                vertices.add(v)
        while len(vertices) > 0:
            r_vertex = random.choice(list(vertices))
            vertices.remove(r_vertex)
            self.edges.append(Edge(vertex, r_vertex))
            vertex = r_vertex
        self.edges.append(Edge(self.vertices[0], vertex))
