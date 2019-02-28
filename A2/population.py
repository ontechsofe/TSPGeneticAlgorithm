from salesman import Salesman

class Population:
    def __init__(self, cities, num=100):
        self.sale_squad = list()
        self.num_pop = num
        self.cities = cities
        self.populate()
    
    def populate(self):
        for _ in range(0, self.num_pop):
            self.sale_squad.append(Salesman(self.cities[:]))

    def calc_fitness(self, g):
        # for x in self.sale_squad:
        #     print(x.brain.dir)
        for s in self.sale_squad:
            s.calc_fitness(g)
        pass