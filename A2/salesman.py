from brain import Brain

class Salesman:
    def __init__(self, cities):
        self.brain = Brain(cities)
        self.fitness = 0
        self.dist = 0
        # print(self.brain.dir)

    def setup_brain(self):
        self.brain.shuffle_dir()

    def get_dir(self) -> list:
        return self.brain.get_dir()
    
    def get_fitness(self) -> float:
        return self.fitness
    
    def calc_dist(self, g):
        # print(self.brain.get_dir())
        for x in range(1, len(self.brain.get_dir())):
            v = g.get_vertex(self.brain.get_dir()[x-1])
            w = g.get_vertex(self.brain.get_dir()[x])
            self.dist += v.get_weight(w)
    
    def calc_fitness(self, max_dist, min_dist):
        self.fitness = 1 - (self.dist - min_dist)/max_dist
        # print(f'Distance: {self.dist}\nFitness: {self.fitness}')
