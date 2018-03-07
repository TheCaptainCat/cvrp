from cvrp import Vertex


class Builder:
    def __init__(self, path):
        self.path = path

    def build(self):
        vertices = {}
        with open(self.path) as f:
            for line in f:
                params = line.split('\n')[0].split(";")
                vertices[int(params[0])] = Vertex(int(params[0]), int(params[1]), int(params[2]), int(params[3]))
        return vertices
