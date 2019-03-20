from .population import Population
from random import uniform, randint
from copy import deepcopy


class Nature:
    def __init__(self, g, POP_SIZE=100) -> None:
        self.generation = 0
        self.pop = Population(list(g.get_vertices())[:], POP_SIZE)
        self.POP_SIZE = POP_SIZE
        self.env = g

    def run(self, termination_condition):
        count = 0
        minimum = float('inf')
        best = None
        while count < termination_condition:
            self.calc_fitness()
            self.new_generation()
            new_min = self.pop.minimum
            if new_min < minimum:
                minimum = new_min
                best = deepcopy(self.pop.get_best())
                print(f'BEST: {best.get_dir()}\nMIN: {best.get_dist()}')
                count = 0
            else:
                count += 1
        return best

    def calc_fitness(self):
        '''
        Calculates all fitnesses
        '''
        self.pop.calc_fitness(self.env)

    def new_generation(self):
        self.natural_selection()
        p1 = None
        for s in self.pop.sale_squad:
            if s.get_fitness() == 1.0:
                p1 = s
                break
        p2 = self.pop.sale_squad[randint(0, len(self.pop.sale_squad)-1)]
        self.make_baby(p1, p2)
        while len(self.pop.sale_squad) < self.POP_SIZE:
            p1 = self.pop.sale_squad[randint(0, len(self.pop.sale_squad)-1)]
            p2 = self.pop.sale_squad[randint(0, len(self.pop.sale_squad)-1)]
            self.make_baby(p1, p2)
        for s in self.pop.sale_squad:
            s.brain.mutate()

    def natural_selection(self):
        '''
        Removing unfit salesman based on natural selection
        '''
        self.generation += 1
        for s in self.pop.sale_squad:
            rand = uniform(0, 1)
            if rand > s.get_fitness():
                self.pop.sale_squad.remove(s)

    def make_baby(self, p1, p2):
        '''
        This is the crossover function of the agent
        '''
        source = p1.get_dir()[0:1]
        p1_dir = p1.get_dir()[1:len(p1.get_dir())-1]
        p2_dir = p2.get_dir()[1:len(p2.get_dir())-1]
        splice_point = randint(0, len(p1_dir))
        p2_spliced = [x for x in p2_dir if x not in p1_dir[0:splice_point]]
        p1_spliced = [x for x in p1_dir if x not in p2_dir[0:splice_point]]
        c1 = source + p1_dir[0:splice_point] + p2_spliced + source
        c2 = source + p2_dir[0:splice_point] + p1_spliced + source
        self.pop.add_salesman(c1)
        self.pop.add_salesman(c2)

        # source = p1.get_dir()[0:1]
        # p1_dir = p1.get_dir()[1:len(p1.get_dir())-1]
        # p2_dir = p2.get_dir()[1:len(p2.get_dir())-1]
        # num1 = randint(0, len(p1_dir))
        # num2 = randint(0, len(p1_dir))
        # start = min(num1, num2)
        # end = max(num1, num2)
        # p2_dir = [x for x in p2_dir if x not in p1_dir[start:end]]
        # p1_dir = p1_dir[start:end]
        # child_1 = source + p2_dir[0:start] + p1_dir + p2_dir[start:] + source
        # self.pop.add_salesman(child_1)
