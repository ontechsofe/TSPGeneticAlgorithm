from random import shuffle

class Brain:
    def __init__(self, i):
        self.instructs = i
        shuffle(self.instructs)

class Child:
    def __init__(self, i):
        self.brain = Brain(i)

class Parent:
    def __init__(self):
        self.children = list()
        self.instructs = ["stop", "play", "run", "jump", "quiet", "loud"]
        self.birth_children()
    
    def birth_children(self, num=10):
        for _ in range(0, num):
            self.children.append(Child(self.instructs[:]))
    
    def print_child_brains(self):
       for x in self.children:
           print(x.brain.instructs)

p = Parent()
p.print_child_brains()