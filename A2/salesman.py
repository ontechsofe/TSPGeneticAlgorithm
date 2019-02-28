from brain import Brain

class Salesman:
    def __init__(self, cities):
        self.brain = Brain(cities)
        self.fitness = 0
        # print(self.brain.dir)

    def get_dir(self) -> list:
        return self.brain.get_dir()
    
    def calc_fitness(self, g):
        # print(self.brain.get_dir())
        dist = 0
        for x in range(1, len(self.brain.get_dir())):
            v = g.get_vertex(self.brain.get_dir()[x-1])
            w = g.get_vertex(self.brain.get_dir()[x])
            dist += v.get_weight(w)
        self.fitness = 1000000/(dist*dist)
        print(f'Distance: {dist}\nFitness: {self.fitness}')
