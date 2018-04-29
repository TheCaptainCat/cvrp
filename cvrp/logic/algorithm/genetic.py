import copy
import random

from cvrp.logic import Graph


class Genetic:
    def __init__(self, graph, solution_cnt):
        self.graph = graph
        self.solution_cnt = solution_cnt
        self.solutions = []
        self.random_solutions()

    def random_solutions(self):
        while len(self.solutions) < self.solution_cnt:
            solution = Graph.random_routes(self.graph.vertices, self.graph.capacity)
            self.graph.routes = solution
            self.solutions.append({'routes': solution, 'distance': self.graph.distance})

    def reproduction(self):
        total_distance = sum(solution['distance'] for solution in self.solutions)
        roulette = {}
        for i in range(0, len(self.solutions)):
            roulette[i] = self.solutions[i]['distance'] / total_distance
        ranks = list(range(0, len(self.solutions)))
        ranks = sorted(ranks, key=lambda j: roulette[j])
        new_solutions = []
        while len(new_solutions) < self.solution_cnt:
            r = random.random()
            w = 1
            rank = 0
            while 1 - w < r:
                rank += 1
                w /= 1.5
            new_solutions.append(self.solutions[ranks[min(rank - 1, len(ranks) - 1)]])
        self.solutions = new_solutions

    def crossover(self):
        for i in range(0, self.solution_cnt):
            giver = self.solutions[i]['routes']
            r_i = random.randint(0, len(self.solutions) - 1)
            receiver = copy.deepcopy(self.solutions[r_i]['routes'])
            save = copy.deepcopy(self.solutions[r_i]['routes'])

            self.graph.routes = giver
            r_vertex = self.graph.vertices[random.randint(1, len(self.graph.vertices))]
            route_id, v_index = self.graph.find_vertex_coordinates(r_vertex.id)
            route_length = len(self.graph.routes[route_id])
            r_length = min(route_length - v_index, random.randint(1, 5))
            route_fragment = self.graph.routes[route_id][v_index:v_index + r_length]

            self.graph.routes = receiver
            r_vertex = self.graph.vertices[random.randint(1, len(self.graph.vertices))]
            route_id, v_index = self.graph.find_vertex_coordinates(r_vertex.id)
            self.graph.insert_route_fragment(route_id, route_fragment, v_index)
            if self.graph.is_full:
                self.solutions[r_i]['routes'] = save
            else:
                self.solutions[r_i]['routes'] = receiver
        self.graph.routes = min(self.solutions, key=lambda x: x['distance'])['routes']

    def mutation(self):
        pass

    def compute(self):
        self.reproduction()
        self.crossover()
        self.mutation()
