class Tabu:
    def __init__(self, graph, tabu_limit, neighbors_limit):
        self.graph = graph
        self.tabu = []
        self.tabu_2 = []
        self.tabu_limit = tabu_limit
        self.neighbors_limit = neighbors_limit
        self.coin = 1

    def find_best_permutation(self):
        """
        Permet de récupérer la meilleur permutation possible parmis les (neighbors_limit) différentes
        :return: Les deux vertices à permuter pour effectuer la meilleur des permutations
        """
        permutations = {}
        start_dist = self.graph.distance

        def pick_vertices():
            """
            Sélectionne deux vertices parmis tous les vertices du graphe,
            sauf si le couple se trouve déjà dans la liste Tabou
            """
            _v1 = _v2 = None
            while _v1 is None or _v2 is None or (_v1.id, _v2.id) in self.tabu:
                _v1, _v2 = self.graph.pick_random_vertices()
            return _v1, _v2

        while len(permutations) < self.neighbors_limit * 2:
            # Récupère deux vertices et effectue la permutaiton
            v1, v2 = pick_vertices()
            self.graph.swap_vertices(v1, v2)
            is_full = self.graph.is_full
            # Insère la fitness du graphe obtenu dans un tableau puis reviens au graphe initial
            permutations[(v1.id, v2.id)] = (self.graph.distance, is_full)
            permutations[(v2.id, v1.id)] = (self.graph.distance, is_full)
            self.graph.swap_vertices(v1, v2)

        # Récupère le couple donnant le graphe avec la fitness la plus petite
        # En ne traitant que les permutations vérifiant si le graphe est complet ou non
        # (respectant la contrainte de capacité)
        v1_id, v2_id = min(permutations.keys(),
                           key=lambda x: permutations[x][0] if not permutations[x][1] else float('infinity'))
        # Si la fitness est supérieur à celle initiale, on ajoute le couple dans le liste Tabou
        min_dist = permutations[(v1_id, v2_id)][0]
        if min_dist > start_dist:
            self.tabu.append((v1_id, v2_id))
            self.tabu.append((v2_id, v1_id))
            if len(self.tabu) >= self.tabu_limit * 2:
                del self.tabu[0]
                del self.tabu[0]
        return self.graph.vertices[v1_id], self.graph.vertices[v2_id]

    def find_best_insertion(self):
        """
        Permet de récupérer la meilleur insertion possible parmis les (neighbors_limit) différentes
        :return: Le vertex v1 dans la route r2 à l'index v2_index
        """
        insertions = {}
        start_dist = self.graph.distance

        def pick_vertices():
            """
            Sélectionne deux vertices parmis tous les vertices du graphe,
            Puis récupère l'index des vertices dans leur route
            """
            _v1 = _v2 = _v1_index = _v2_index = None
            _r1 = _r2 = None
            while _v1 is None or _v2 is None or (_v1.id, _r1, _r2, _v2_index) in self.tabu_2:
                _v1, _v2 = self.graph.pick_random_vertices()
                _r1, _v1_index = self.graph.find_vertex_coordinates(_v1.id)
                _r2, _v2_index = self.graph.find_vertex_coordinates(_v2.id)
            return _r1, _r2, _v1, _v2, _v1_index, _v2_index

        while len(insertions) < self.neighbors_limit:
            # Récupère deux vertices et effectue la l'insertion de v1 dans r2 à l'emplacement de v2
            r1, r2, v1, v2, v1_index, v2_index = pick_vertices()
            self.graph.move_vertex(v1, r1, r2, v2_index)
            is_full = self.graph.is_full
            # Insère la fitness du graphe obtenu dans un tableau puis reviens au graphe initial
            insertions[(v1.id, r1, r2, v2_index)] = (self.graph.distance, is_full)
            self.graph.move_vertex(v1, r2, r1, v1_index)

        # Récupère le quadruplet donnant le graphe avec la fitness la plus petite
        # En ne traitant que les insertions vérifiant si le graphe est complet ou non
        # (respectant la contrainte de capacité)
        v1_id, r1, r2, v2_index = min(insertions.keys(),
                                      key=lambda x: insertions[x][0] if not insertions[x][1] else float('infinity'))
        min_dist = insertions[(v1_id, r1, r2, v2_index)][0]
        # Si la fitness est supérieur à celle initiale, on ajoute le quadruplet dans le liste Tabou
        if min_dist > start_dist:
            self.tabu.append((v1_id, r1, r2, v2_index))
            if len(self.tabu) >= self.tabu_limit:
                del self.tabu[0]
        return self.graph.vertices[v1_id], r1, r2, v2_index

    def compute(self):
        # 50 itérations de permutaions pour 1 itération d'insertion
        if self.coin < 50:
            v1, v2 = self.find_best_permutation()
            self.graph.swap_vertices(v1, v2)
            self.coin += 1
        else:
            v1, r1, r2, index = self.find_best_insertion()
            self.graph.move_vertex(v1, r1, r2, index)
            self.coin = 1
