import random

from cvrp.logic import Route


class Graph:
    def __init__(self, vertices, capacity):
        self.vertices = vertices
        self.capacity = capacity
        self.routes = []

    def random_routes(self):
        cnt = 0
        vertices = set()
        for v in self.vertices.values():
            if v.id != 0:
                vertices.add(v)
        while len(vertices) > 0:
            route = Route()
            while cnt < self.capacity:
                r_vertex = random.choice(list(vertices))
                vertices.remove(r_vertex)
                route.vertices.append(r_vertex)
