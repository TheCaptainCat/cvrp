from cvrp.graphics import Line
from cvrp.graphics.colors import generate_new_color


class Path:
    def __init__(self, route, existing_colors):
        self.color = generate_new_color(existing_colors, pastel_factor=0.01)
        self.route = route
        self.lines = []
        self.create_lines()

    def create_lines(self):
        self.lines = []
        vertex = self.route.first_vertex
        self.lines.append(Line(vertex.edge_in))
        while vertex.id != 0:
            self.lines.append(Line(vertex.edge_out))
            vertex = vertex.edge_out.v2
