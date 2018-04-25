class Tabu:
    def __init__(self, graph, tabu_limit, neighbors_limit):
        self.graph = graph
        self.tabu = []
        self.tabu_limit = tabu_limit
        self.neighbors_limit = neighbors_limit

    def find_best_permutation(self):
        permutations = {}
        start_dist = self.graph.distance

        def pick_vertices():
            _v1 = _v2 = None
            while _v1 is None or _v2 is None or (_v1.id, _v2.id) in self.tabu:
                _v1, _v2 = self.graph.pick_random_vertices()
            return _v1, _v2

        while len(permutations) < self.neighbors_limit * 2:
            v1, v2 = pick_vertices()
            self.graph.swap_vertices(v1, v2)
            is_full = self.graph.is_full
            permutations[(v1.id, v2.id)] = (self.graph.distance, is_full)
            permutations[(v2.id, v1.id)] = (self.graph.distance, is_full)
            self.graph.swap_vertices(v1, v2)

        v1_id, v2_id = min(permutations.keys(),
                           key=lambda x: permutations[x][0] if not permutations[x][1] else float('infinity'))
        min_dist = permutations[(v1_id, v2_id)][0]
        if min_dist > start_dist:
            self.tabu.append((v1_id, v2_id))
            self.tabu.append((v2_id, v1_id))
            if len(self.tabu) >= self.tabu_limit * 2:
                del self.tabu[0]
                del self.tabu[0]
        return self.graph.vertices[v1_id], self.graph.vertices[v2_id]

    def compute(self):
        v1, v2 = self.find_best_permutation()
        self.graph.swap_vertices(v1, v2)
