from random import uniform, randint, shuffle

class Brain:
    def __init__(self, cities):
        self.dir = cities
        shuffle(self.dir)

    def get_dir(self):
        return self.dir
    
    def clone(self):
        clone = Brain(self.dir)
        return clone
    
    def mutate(self, mutate_rate=0.01):
        for x in self.dir:
            if uniform(0.0, 1.0) < mutate_rate:
                r = randint(0, len(self.dir))
                i = self.dir.index(x)
                self.dir[i], self.dir[r] = self.dir[r], self.dir[i]