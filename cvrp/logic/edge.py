class Edge:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    @property
    def distance(self):
        return self.v1.distance_to(self.v2)

    def __repr__(self):
        return f'Edge (({self.v1}) >{self.distance}> ({self.v2}))'
