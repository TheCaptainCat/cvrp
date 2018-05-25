from cvrp.logic.algorithm import Tabu, Genetic


class Console:
    """Permet la gestion de l'application sur la console."""

    @staticmethod
    def algorithm(graph):
        print(f"Nombre de clients de ce graphe : {graph.vertices_cnt}")
        print("Choisissez un algorithme\n1) Tabu\n"
              + "2) Génétique\n3) Stop")
        c = None
        while c is None or not 1 <= c <= 3:
            try:
                c = int(input('Faites votre choix : '))
            except ValueError:
                print('Erreur de saisie')
                continue
        if c == 3:
            print('Au revoir !')
            exit()
        if c == 1:
            tabu_limit = None
            while tabu_limit is None or not 1 <= tabu_limit:
                try:
                    tabu_limit = int(input('Choisissez la taille de la liste Tabu : '))
                except ValueError:
                    print('Erreur de saisie')
                    continue
            neighbors_limit = None
            while neighbors_limit is None or not 1 <= neighbors_limit:
                try:
                    neighbors_limit = int(input('Choisissez le nombre de voisins d\'une solution '
                                                '(attention à la taille de l\'échantillon) : '))
                except ValueError:
                    print('Erreur de saisie')
                    continue
            algorithm = Tabu(graph, tabu_limit, neighbors_limit)
        else:
            solution_cnt = None
            while solution_cnt is None or not 1 <= solution_cnt:
                try:
                    solution_cnt = int(input('Choisissez la taille de la population à générer : '))
                except ValueError:
                    print('Erreur de saisie')
                    continue
            algorithm = Genetic(graph, solution_cnt)
        return algorithm

    @staticmethod
    def file():
        file = None
        while file is None or not 0 <= file <= 5:
            try:
                file = int(input('Choisissez un échantillon de données (entre 0 et 5) : '))
            except ValueError:
                print('Erreur de saisie')
                continue
        return 'data/data0{0}.csv'.format(file)
