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

    @property
    def distance(self):
        return sum(route.distance for route in self.routes)

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

    def swap_vertices(self, v1, v2):
        v1.swap_with(v2)
        self.vertices[v1.id] = v1
        self.vertices[v2.id] = v2

    def random_swap(self):
        tmp_list = list(self.vertices.values())
        v1 = self.vertices[random.randint(1, len(tmp_list) - 1)]
        v2 = self.vertices[random.randint(1, len(tmp_list) - 1)]
        self.swap_vertices(v1, v2)
