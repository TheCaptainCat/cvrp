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

    def random_routes(self):
        total = 0
        vertices = set()
        for v in self.vertices.values():
            if v.id != 0:
                vertices.add(v)
                total += v.qt
        route = Route(self.vertices[0])
        route.vertices.append(self.vertices[0])
        cnt = 0
        while len(vertices) > 0:
            r_vertex = random.choice(list(vertices))
            if cnt + r_vertex.qt > self.capacity:
                self.routes.append(route)
                cnt = 0
                route = Route(self.vertices[0])
                route.vertices.append(self.vertices[0])
            vertices.remove(r_vertex)
            route.add_vertex(r_vertex)
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

    def delete_route(self, route):
        self.routes.remove(route)

    def unlink_route_fragment(self, fragment_head, length=1):
        route = self.find_route_by_vertex(fragment_head)

        def unlink_vertex(vertex):
            route.remove_vertex(vertex)
            del self.vertices[vertex.id]

        unlink_vertex(fragment_head)
        previous_edge = fragment_head.edge_in

        last_vertex = fragment_head
        next_vertex = fragment_head.edge_out.v2
        i = 1
        while i < length:
            unlink_vertex(next_vertex)
            last_vertex = next_vertex
            next_vertex = next_vertex.edge_out.v2
            i += 1

        previous_edge.v2 = next_vertex
        if next_vertex.id != 0:
            next_vertex.edge_in = previous_edge
        # fragment_head.edge_in = None
        # last_vertex.edge_out.v2 = None

    def link_route_fragment(self, new_head, fragment_head, length=1):
        route = self.find_route_by_vertex(new_head)
        first_edge = new_head.edge_out
        if new_head.edge_in.v1.id == 0:
            route.first_vertex = fragment_head
        last_vertex = first_edge.v2
        first_edge.v2 = fragment_head

        def link_vertex(vertex):
            self.unlink_route_fragment(self.vertices[vertex.id])
            self.vertices[vertex.id] = vertex
            route.add_vertex(vertex)

        link_vertex(fragment_head)
        fragment_head.edge_in = first_edge
        cur_vertex = fragment_head
        i = 1
        while i < length:
            cur_vertex = cur_vertex.edge_out.v2
            link_vertex(cur_vertex)
            i += 1
        cur_vertex.edge_out.v2 = last_vertex
        if last_vertex.id != 0:
            last_vertex.edge_in = cur_vertex.edge_out
        if last_vertex.id == 0:
            route.last_vertex = cur_vertex
        pass

    def find_route_by_vertex(self, vertex):
        for route in self.routes:
            for v in route.vertices:
                if v is vertex:
                    return route
        return None
