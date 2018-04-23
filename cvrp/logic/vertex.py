import math


class Vertex:
    def __init__(self, v_id, x, y, qt):
        self.id = v_id
        self.x = x
        self.y = y
        self.qt = qt
        self.edge_in = None
        self.edge_out = None

    def __repr__(self):
        return f'Vertex {self.id} [{self.x},{self.y}] -> {self.qt}'

    def distance_to(self, vertex):
        return math.sqrt(((self.x - vertex.x) ** 2) + ((self.y - vertex.y) ** 2))

    def swap_with(self, vertex):
        def swap(a, b):
            return b, a
        self.id, vertex.id = swap(self.id, vertex.id)
        self.x, vertex.x = swap(self.x, vertex.x)
        self.y, vertex.y = swap(self.y, vertex.y)
        self.qt, vertex.qt = swap(self.qt, vertex.qt)
