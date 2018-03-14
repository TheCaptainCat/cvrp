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
            v1 = v2 = None
            while v1 is None or v2 is None or (v1.id, v2.id) in self.tabu or (v1.id, v2.id) in permutations.keys():
                v1, v2 = self.graph.pick_random_vertices()
            return v1, v2

        while len(permutations) < self.neighbors_limit * 2:
            v1_id, v2_id = pick_vertices()
            self.graph.swap_vertices(v1_id, v2_id)
            if not self.graph.is_full:
                permutations[(v1_id.id, v2_id.id)] = self.graph.distance
                permutations[(v2_id.id, v1_id.id)] = self.graph.distance
            self.graph.swap_vertices(v1_id, v2_id)

        v1_id, v2_id = min(permutations.keys(), key=lambda x: permutations[x])
        min_dist = min(permutations.values())
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
