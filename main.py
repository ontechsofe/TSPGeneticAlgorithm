from pandas import read_csv, DataFrame
from time import time
from data_structs.graph import Graph
from objects.nature import Nature
from math import sqrt
from matplotlib.pyplot import plot, show


def euclidean_distance(x1, y1, x2, y2):
    if x2 == x1 and y2 == y1:
        return 0
    elif x2 - x1 == 0:
        return abs(y2-y1)
    elif y2 - y1 == 0:
        return abs(x2-x1)
    return sqrt((y2-y1)**2 + (x2-x1)**2)


def generate_df(pos, cities):
    df = DataFrame()
    for i in cities:
        d = list()
        for j in cities:
            d.append(euclidean_distance(
                pos[i][0], pos[i][1], pos[j][0], pos[j][1]))
        df[i] = d
    return df


def setup_graph(df, cities) -> Graph:
    g = Graph()
    for v in cities:
        g.add_vertex(v)
    for v0 in range(0, len(cities)):
        for v1 in range(v0+1, len(cities)):
            g.add_edge(cities[v0], cities[v1], df[cities[v0]][v1])
    return g


def main():
    distance = input(
        "Click ENTER for the distances data set\nOR any other key for the (x, y) positional data set: ")
    positions = None
    df = None
    cities = None
    population_size = None
    termination_condition = None
    if not distance:
        df = read_csv('./data/data_distances.csv', index_col=False)
        cities = list(df.columns)[1:]
        population_size = 100
        termination_condition = 80
    else:
        positions = read_csv('./data/data_positional.csv', index_col=False)
        cities = list(positions.columns)[1:]
        df = generate_df(positions, cities)
        population_size = 1000
        termination_condition = 80

    g = setup_graph(df, cities)

    start = time()
    n = Nature(g, population_size)

    count = 0
    minimum = float('inf')
    best = None
    while count < termination_condition:
        n.calc_fitness()
        n.new_generation()
        new_min = n.pop.minimum
        if new_min < minimum:
            minimum = new_min
            best = n.pop.best
            print(f'BEST: {best.get_dir()}\nMIN: {best.dist}')
            count = 0
        else:
            count += 1

    end = time()
    print(f'Total Runtime: {end - start}')
    # print(best.get_dir()[:len(best.get_dir())-1])
    if distance:
        x_values = [positions[i][0]
                    for i in best.get_dir()[:len(best.get_dir())-1]]
        y_values = [positions[i][1]
                    for i in best.get_dir()[:len(best.get_dir())-1]]
        print(best.get_dir())
        # print(x_values)
        # print(y_values)
        plot_data = DataFrame({'x': x_values, 'y': y_values})
        plot('x', 'y', data=plot_data, linestyle='-', marker='o')
        show()


if __name__ == '__main__':
    main()
