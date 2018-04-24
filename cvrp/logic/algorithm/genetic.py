from cvrp.logic import Vertex, Graph


class Genetic:
    def __init__(self, graph, solution_cnt):
        self.graph = graph
        self.solution_cnt = solution_cnt
        self.solutions = []
        self.random_solutions()

    def random_solutions(self):
        def copy_vertices():
            vertices = {}
            for v_id in self.graph.vertices:
                vertex = self.graph.vertices[v_id]
                vertices[v_id] = Vertex(v_id, vertex.x, vertex.y, vertex.qt)
            return vertices

        while len(self.solutions) < self.solution_cnt:
            self.solutions.append(Graph(copy_vertices(), self.graph.capacity))

    def compute(self):
        pass
