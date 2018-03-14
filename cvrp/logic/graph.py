import random

from cvrp.logic import Route


class Graph:
    def __init__(self, vertices, capacity):
        self.vertices = vertices
        self.vertex_count = len(list(self.vertices.values()))
        self.capacity = capacity
        self.routes = []
        self.algorithm = None

    @property
    def edges(self):
        return [edge for route in self.routes for edge in route.edges]

    @property
    def distance(self):
        return sum(route.distance for route in self.routes)

    @property
    def is_full(self):
        for route in self.routes:
            if route.quantity > self.capacity:
                return True
        return False

    def compute_algorithm(self):
        if self.algorithm is not None:
            self.algorithm.compute()
            # self.delete_routes()

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

    def pick_random_vertices(self):
        v1 = self.vertices[random.randint(1, self.vertex_count - 1)]
        v2 = self.vertices[random.randint(1, self.vertex_count - 1)]
        return v1, v2

    def swap_vertices(self, v1, v2):
        v1.swap_with(v2)
        self.vertices[v1.id] = v1
        self.vertices[v2.id] = v2

    def random_swap(self):
        v1, v2 = self.pick_random_vertices()
        self.swap_vertices(v1, v2)

    def find_route_by_vertex(self, vertex):
        for route in self.routes:
            for v in route.vertices:
                if v is vertex:
                    return route
        return None

    def transfer_vertex(self, vertex, origin_route, dest_route):
        origin_route.remove_vertex(vertex)
        dest_route.add_vertex(vertex)

    def delete_routes(self):
        min_route = min(self.routes, key=lambda r: len(r.vertices))
        if len(min_route.vertices) <= 1:
            return
        loop = True
        while loop:
            vertex = min(min_route.vertices, key=lambda v: v.qt if v.id != 0 else float('infinity'))
            change = False
            for route in self.routes:
                if route is not min_route:
                    if route.quantity + vertex.qt <= self.capacity:
                        self.transfer_vertex(vertex, min_route, route)
                        change = True
                        break
            if not change:
                loop = False

