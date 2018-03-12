import math


class Vertex:
    def __init__(self, v_id, x, y, qt):
        self.id = v_id
        self.x = x
        self.y = y
        self.qt = qt

    def __repr__(self):
        return f'Vertex {self.id} [{self.x},{self.y}] -> {self.qt}'

    def distance_to(self, vertex):
        return math.sqrt((abs(self.x - vertex.x) ** 2) + (abs(self.y - vertex.y) ** 2))
