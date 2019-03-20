from .salesman import Salesman


class Population:
    def __init__(self, cities, num=100):
        self.sale_squad = list()
        self.num_pop = num
        self.populate(cities)
        self.maximum = float('inf')
        self.minimum = -1
        self.best = None

    def populate(self, cities):
        for _ in range(0, self.num_pop):
            self.add_salesman(cities)
        for s in self.sale_squad:
            s.setup_brain()

    def add_salesman(self, cities):
        self.sale_squad.append(Salesman(cities[:]))

    def calc_fitness(self, g):
        for s in self.sale_squad:
            s.calc_dist(g)
        dist = [s.get_dist() for s in self.sale_squad]
        self.minimum = min(dist)
        self.maximum = max(dist)
        self.best = self.sale_squad[dist.index(self.minimum)]
        for s in self.sale_squad:
            s.calc_fitness(self.maximum, self.minimum)

    def get_best(self) -> Salesman:
        return self.best
