from population import Population

class Nature:
    def __init__(self, g, POP_SIZE=100):
        self.pop = Population(list(g.get_vertices())[:], POP_SIZE)
        self.env = g
        self.calc_fitness()
    
    def calc_fitness(self):
        self.pop.calc_fitness(self.env)