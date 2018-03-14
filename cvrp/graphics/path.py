from cvrp.graphics import Line
from cvrp.graphics.colors import generate_new_color


class Path:
    def __init__(self, route, existing_colors):
        self.color = generate_new_color(existing_colors, pastel_factor=0.01)
        self.route = route
        self.lines = []
        for edge in route.edges:
            self.lines.append(Line(edge))
