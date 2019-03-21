from .vertex import Vertex


class Graph:
    def __init__(self):
        self.vert_dict = dict()
        self.num_vertices = 0

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, v0, v1, cost=0):
        if v0 not in self.vert_dict:
            self.add_vertex(v0)
        if v1 not in self.vert_dict:
            self.add_vertex(v1)

        self.vert_dict[v0].add_neighbor(self.vert_dict[v1], cost)
        self.vert_dict[v1].add_neighbor(self.vert_dict[v0], cost)

    def get_vertices(self):
        return self.vert_dict.keys()