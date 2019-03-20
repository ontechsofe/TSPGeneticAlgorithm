from random import uniform, randint, shuffle

class Brain:
    def __init__(self, cities):
        self.dir = cities
    
    def shuffle_dir(self):
        copy = self.dir[1:]
        shuffle(copy)
        self.dir = self.dir[0:1] + copy + self.dir[0:1]

    def get_dir(self):
        return self.dir

    def mutate(self, mutate_rate=0.01):
        directions = self.dir[1:len(self.dir)-1]
        for x in directions:
            if uniform(0.0, 1.0) < mutate_rate:
                i = directions.index(x)
                if i == 0:
                    directions[i], directions[i+1] = directions[i+1], directions[i]
                else:
                    directions[i], directions[i-1] = directions[i-1], directions[i]
        self.dir = self.dir[0:1] + directions + self.dir[0:1]