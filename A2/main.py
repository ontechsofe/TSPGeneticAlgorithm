from pandas import read_csv
from time import time
from graph import Graph
from nature import Nature


def setup_graph(df, cities) -> Graph:
    g = Graph()
    for v in cities:
        g.add_vertex(v)
    for v0 in range(0, len(cities)):
        for v1 in range(v0+1, len(cities)):
            g.add_edge(cities[v0], cities[v1], df[cities[v0]][v1])
    return g

def main():
    start = time()
    start_setup = time()
    df = read_csv('data_set1.csv', index_col=False)
    cities = list(df.columns)[1:]
    g = setup_graph(df, cities)
    end_setup = time()
    
    n = Nature(g)
    
    # Prints all the relations in the graph
    # for v in g:
    #     for w in v.get_connections():
    #         vid = v.get_id()
    #         wid = w.get_id()
    #         print(f'( {vid} , {wid}, {v.get_weight(w)})')
    end = time()
    print(f'Setup Runtime: {end_setup - start_setup}')
    print(f'Total Runtime: {end - start}')

if __name__ == '__main__':
    main()