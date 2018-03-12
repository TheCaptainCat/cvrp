import random

from cvrp.logic import Route


class Graph:
    def __init__(self, vertices, capacity):
        self.vertices = vertices
        self.capacity = capacity
        self.routes = []

    @property
    def edges(self):
        return [edge for route in self.routes for edge in route.edges]

    def random_routes(self):
        cnt = 0
        vertices = set()
        for v in self.vertices.values():
            if v.id != 0:
                vertices.add(v)
        route = Route()
        route.vertices.append(self.vertices[0])
        while len(vertices) > 0:
            r_vertex = random.choice(list(vertices))
            if cnt + r_vertex.qt > self.capacity:
                self.routes.append(route)
                cnt = 0
                route = Route()
                route.vertices.append(self.vertices[0])
            vertices.remove(r_vertex)
            route.vertices.append(r_vertex)
            cnt += r_vertex.qt
        self.routes.append(route)
        for route in self.routes:
            route.random_path()
