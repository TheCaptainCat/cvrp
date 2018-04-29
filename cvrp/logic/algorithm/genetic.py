import copy
import random

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
            self.solutions[len(self.solutions) - 1].random_routes()

    def reproduction(self):
        total_distance = sum(graph.distance for graph in self.solutions)
        ranks = [graph for graph in self.solutions]
        roulette = {}
        for graph in self.solutions:
            roulette[graph] = graph.distance / total_distance
        ranks = sorted(ranks, key=lambda g: roulette[g])
        new_solutions = []
        while len(new_solutions) < self.solution_cnt:
            r = random.random()
            w = 1
            rank = 0
            while 1 - w < r:
                rank += 1
                w /= 1.5
            new_solutions.append(copy.deepcopy(ranks[min(rank - 1, len(ranks) - 1)]))
        self.solutions = new_solutions

    def crossover(self):
        for i in range(0, self.solution_cnt):
            print(i)
            giver = self.solutions[i]
            receiver = giver
            while receiver is giver:
                receiver = self.solutions[random.randint(0, len(self.solutions) - 1)]
            v_id = random.randint(1, len(giver.vertices) - 1)
            r_length = random.randint(1, 5)
            length = 1
            vertex = giver.vertices[v_id]
            vertex2 = vertex
            while vertex2.edge_out.v2.id != 0 and length < r_length:
                vertex2 = vertex2.edge_out.v2
                length += 1
            new_head = receiver.vertices[random.randint(1, len(receiver.vertices) - 1)]
            receiver.link_route_fragment(new_head, vertex, length)

    def mutation(self):
        pass

    def compute(self):
        self.reproduction()
        self.crossover()
        self.mutation()
