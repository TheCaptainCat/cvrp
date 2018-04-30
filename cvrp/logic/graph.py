import random


class Graph:
    def __init__(self, vertices, capacity):
        self.vertices = vertices
        self.home = vertices[0]
        del self.vertices[0]
        self.vertices_cnt = len(vertices)
        self.capacity = capacity
        self.routes = []
        self.algorithm = None

    def route_length(self, route_id):
        route = self.routes[route_id]
        if len(route) == 0:
            return 0
        vertex = route[0]
        length = self.home.distance_to(self.vertices[route[0]])
        for i in range(1, len(route)):
            length += self.vertices[vertex].distance_to(self.vertices[route[i]])
            vertex = route[i]
        length += self.home.distance_to(self.vertices[route[len(route) - 1]])
        return length

    def route_quantity(self, route_id):
        return sum(self.vertices[vertex].qt for vertex in self.routes[route_id])

    @property
    def distance(self):
        return sum(self.route_length(i) for i in range(0, len(self.routes)))

    @property
    def is_full(self):
        for i in range(0, len(self.routes)):
            if self.route_quantity(i) > self.capacity:
                return True
        return False

    def find_vertex_coordinates(self, v_id):
        for route_id in range(0, len(self.routes)):
            for v_index in range(0, len(self.routes[route_id])):
                if self.vertices[self.routes[route_id][v_index]].id == v_id:
                    return route_id, v_index
        return None

    @classmethod
    def random_routes(cls, vertices, capacity):
        routes = []
        vertices_set = set()
        for v in vertices.values():
            if v.id != 0:
                vertices_set.add(v)
        route = []
        cnt = 0
        while len(vertices_set) > 0:
            r_vertex = random.choice(list(vertices_set))
            if cnt + r_vertex.qt > capacity:
                routes.append(route)
                cnt = 0
                route = []
            vertices_set.remove(r_vertex)
            route.append(r_vertex.id)
            cnt += r_vertex.qt
        routes.append(route)
        for route in routes:
            random.shuffle(route)
        return routes

    def set_random_routes(self):
        self.routes = Graph.random_routes(self.vertices, self.capacity)

    def pick_random_vertices(self):
        v1 = self.vertices[random.randint(1, self.vertices_cnt)]
        v2 = self.vertices[random.randint(1, self.vertices_cnt)]
        return v1, v2

    def pick_random_routes(self):
        r1 = self.routes[random.randint(0, len(self.routes) - 1)]
        r2 = self.routes[random.randint(0, len(self.routes) - 1)]
        return r1, r2

    def swap_vertices(self, v1, v2):
        v1_route_id, v1_index = self.find_vertex_coordinates(v1.id)
        v2_route_id, v2_index = self.find_vertex_coordinates(v2.id)
        self.routes[v1_route_id][v1_index] = v2.id
        self.routes[v2_route_id][v2_index] = v1.id

    def remove_vertex(self, v_id):
        route_id, _ = self.find_vertex_coordinates(v_id)
        self.routes[route_id].remove(v_id)

    def insert_vertex(self, route_id, vertex, index):
        self.routes[route_id].insert(index, vertex)

    def insert_route_fragment(self, route_id, fragment, index):
        for i in range(0, len(fragment)):
            self.remove_vertex(fragment[i])
            self.insert_vertex(route_id, fragment[i], index + i)

    def move_vertex(self, v1, origin_route, dest_route, index):
        self.routes[dest_route].insert(index, v1.id)
        self.routes[origin_route].remove(v1.id)

    def remove_empty_routes(self):
        routes_to_rm = []
        for route in self.routes:
            if len(route) == 0:
                routes_to_rm.append(route)
        for route in routes_to_rm:
            self.routes.remove(route)

    def compute_algorithm(self):
        if self.algorithm is not None:
            self.algorithm.compute()
            self.remove_empty_routes()
