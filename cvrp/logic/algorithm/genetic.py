import copy
import random

from cvrp.logic import Graph


class Genetic:
    """
    Algorithme génétique.
    """
    def __init__(self, graph, solution_cnt):
        self.graph = graph
        self.solution_cnt = solution_cnt
        self.solutions = []
        self.random_solutions()

    def random_solutions(self):
        """
        Génère les solutions de base de façon complètement aléatoire.
        :return: None
        """
        while len(self.solutions) < self.solution_cnt:
            solution = Graph.random_routes(self.graph.vertices, self.graph.capacity)
            self.graph.routes = solution
            # les solutions sont stockées sous la forme d'une liste de routes et une distance
            self.solutions.append({'routes': solution, 'distance': self.graph.distance})

    def selection(self):
        """
        Procède à la sélection des solutions viables selon une méthode de roulette.
        :return: None
        """
        # calcul de la somme des distance
        total_distance = sum(solution['distance'] for solution in self.solutions)
        roulette = {}
        for i in range(0, len(self.solutions)):
            # calcul du rapport de chaque solution
            roulette[i] = self.solutions[i]['distance'] / total_distance
        # une liste d'entiers, correspond à l'index des solutions
        ranks = list(range(0, len(self.solutions)))
        # on trie les index en fonction du rapport de la solution. Les plus petits sont en premiers
        ranks = sorted(ranks, key=lambda j: roulette[j])
        new_solutions = []
        while len(new_solutions) < self.solution_cnt:
            # on tire un nombre aléatoire en 0 et 1
            r = random.random()
            w = 1
            rank = 0
            while 1 - w < r:
                rank += 1
                w /= 1.5
            # une fois la solution trouvée, elle est copiée
            new_solutions.append(copy.deepcopy(self.solutions[ranks[min(rank - 1, len(ranks) - 1)]]))
        self.solutions = new_solutions

    def crossover(self):
        """
        Effectue le croisement des solutions.
        :return: None
        """
        for i in range(0, len(self.solutions)):
            # chaque solution est donneur potentiel
            giver = self.solutions[i]['routes']
            r_i = random.randint(0, len(self.solutions) - 1)
            # on choisit un receveur aléatoire
            receiver = copy.deepcopy(self.solutions[r_i]['routes'])

            self.graph.routes = giver
            # choix d'un vertex au hasard
            r_vertex = self.graph.vertices[random.randint(1, len(self.graph.vertices))]
            route_id, v_index = self.graph.find_vertex_coordinates(r_vertex.id)
            route_length = len(self.graph.routes[route_id])
            # choix d'une longueur de sous-route aléatoire, bornée par la longueur de la route d'origine
            r_length = min(route_length - v_index, random.randint(1, 5))
            # construction du fragment de route
            route_fragment = self.graph.routes[route_id][v_index:v_index + r_length]

            self.graph.routes = receiver
            # on détermine quel vertex va recevoir le fragment
            r_vertex = self.graph.vertices[random.randint(1, len(self.graph.vertices))]
            route_id, v_index = self.graph.find_vertex_coordinates(r_vertex.id)
            # insertion du fragment
            self.graph.insert_route_fragment(route_id, route_fragment, v_index)
            if not self.graph.is_full:
                # si les contraintes ne sont pas dépassées, on accepte le croisement
                self.solutions[r_i]['routes'] = receiver
                self.solutions[r_i]['distance'] = self.graph.distance

    def mutation(self):
        """
        Fait muter les solutions.
        :return: None
        """
        for i in range(0, len(self.solutions)):
            # chaque solution peut muter dans 5% des cas.
            if random.random() < 0.05:
                # entre 1 et 10 mutations
                for j in range(0, random.randint(1, 10)):
                    mutation = copy.deepcopy(self.solutions[i]['routes'])
                    self.graph.routes = mutation
                    # choix de 2 vertices
                    r_vertex1 = self.graph.vertices[random.randint(1, len(self.graph.vertices))]
                    r_vertex2 = self.graph.vertices[random.randint(1, len(self.graph.vertices))]
                    # dans 50% des cas, on insère un vertex après l'autre
                    if random.random() < 0.5:
                        route_id2, v_index2 = self.graph.find_vertex_coordinates(r_vertex2.id)
                        self.graph.insert_route_fragment(route_id2, [r_vertex1.id], v_index2)
                    # sinon, on échange les deux vertices
                    else:
                        self.graph.swap_vertices(r_vertex1, r_vertex2)
                    if not self.graph.is_full:
                        # si les contraintes ne sont pas dépassées, on accepte la mutation
                        self.solutions[i]['routes'] = mutation
                        self.solutions[i]['distance'] = self.graph.distance

    def compute(self):
        self.selection()
        self.crossover()
        self.mutation()
        self.graph.routes = min(self.solutions, key=lambda x: x['distance'])['routes']
