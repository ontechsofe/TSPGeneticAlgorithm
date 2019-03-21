from pandas import read_csv, DataFrame
from time import time
from data_structs.graph import Graph
from objects.nature import Nature
# from math import sqrt
from matplotlib.pyplot import plot, show, title, text


def calc_coord_two(c0, c1, a, d):
    return c0 + a*(c1 - c0)/d


def circles_intersection_coords(p0, p1, r0, r1, p2=None, r2=None):
    d = ((p1[1]-p0[1])**2 + (p1[0]-p0[0])**2)**(0.5)
    if d > r0 + r1:
        raise Exception(
            'No intersection between circles <{p0[0]}, {p0[1]}, RADIUS: {r0}>, <{p1[0]}, {p1[1]}, RADIUS: {r1}>')
    elif d < abs(r0 - r1):
        raise Exception(
            'No intersection between circles <{p0[0]}, {p0[1]}, RADIUS: {r0}>, <{p1[0]}, {p1[1]}, RADIUS: {r1}>')
    elif d == 0 and r0 == r1:
        raise Exception(
            'Infinite intersection between circles <{p0[0]}, {p0[1]}, RADIUS: {r0}>, <{p1[0]}, {p1[1]}, RADIUS: {r1}>')
    elif d == r0 + r1:
        a = (r0**2 - r1**2 + d**2)/(2*d)
        return [calc_coord_two(p0[0], p1[0], a, d), calc_coord_two(p0[1], p1[1], a, d)]
    elif not p2:
        a = (r0**2 - r1**2 + d**2)/(2*d)
        h = (r0**2 - a**2)**(0.5)
        p2 = [calc_coord_two(p0[0], p1[0], a, d),
              calc_coord_two(p0[1], p1[1], a, d)]
        return [int(p2[0] + h*(p1[1] - p0[1])/d), int(p2[1] - h*(p1[0] - p0[0])/d)], [int(p2[0] - h*(p1[1] - p0[1])/d), int(p2[1] + h*(p1[0] - p0[0])/d)]
    else:
        a = (r0**2 - r1**2 + d**2)/(2*d)
        h = (r0**2 - a**2)**(0.5)
        p2 = [p0[0] + a*(p1[0] - p0[0])/d, p0[1] + a*(p1[1] - p0[1])/d]
        lower = [int(p2[0] + h*(p1[1] - p0[1])/d),
                 int(p2[1] - h*(p1[0] - p0[0])/d)]
        upper = [int(p2[0] - h*(p1[1] - p0[1])/d),
                 int(p2[1] + h*(p1[0] - p0[0])/d)]
        if abs(euclidean_distance(lower[0], lower[1], p2[0], p2[1]) - r2) < abs(euclidean_distance(upper[0], upper[1], p2[0], p2[1]) - r2):
            return lower
        return upper


def euclidean_distance(x0, y0, x1, y1):
    if x1 == x0 and y1 == y0:
        return 0
    elif x1 - x0 == 0:
        return int(abs(y1-y0))
    elif y1 - y0 == 0:
        return int(abs(x1-x0))
    return int(((y1-y0)**2 + (x1-x0)**2)**(0.5))


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
    data_type = input(
        "Click ENTER for the distances data set\nOR any other key for the (x, y) positional data set: ")
    start = time()
    positions = None
    df = None
    cities = None
    population_size = None
    termination_condition = None
    if not data_type:
        df = read_csv('./data/data_distances.csv', index_col=False)
        cities = list(df.columns)[1:]
        population_size = 100
        termination_condition = 100
    else:
        positions = read_csv('./data/data_positional.csv', index_col=False)
        cities = list(positions.columns)[1:]
        df = generate_df(positions, cities)
        population_size = 2500
        termination_condition = 100

    g = setup_graph(df, cities)

    n = Nature(g, population_size)
    best = n.run(termination_condition)

    end = time()
    print(f'Total Runtime: {end - start}')
    x_values = None
    y_values = None
    if data_type:
        x_values = [positions[i][0]
                    for i in best.get_dir()[:len(best.get_dir())-1]]
        y_values = [positions[i][1]
                    for i in best.get_dir()[:len(best.get_dir())-1]]
        x_values.append(positions[cities[0]][0])
        y_values.append(positions[cities[0]][1])
    else:
        coords = dict()
        coords[cities[0]] = [0, 0]
        coords[cities[1]] = [df[cities[1]][0], 0]
        coords[cities[2]] = circles_intersection_coords(
            coords[cities[0]], coords[cities[1]], df[cities[2]][0], df[cities[2]][1])[1]
        for x in cities[3:len(cities)]:
            coords[x] = circles_intersection_coords(
                coords[cities[0]], coords[cities[1]], df[x][0], df[x][1], coords[cities[2]], df[x][2])
        x_values = [coords[i][0]
                    for i in best.get_dir()[:len(best.get_dir())-1]]
        y_values = [coords[i][1]
                    for i in best.get_dir()[:len(best.get_dir())-1]]
        x_values.append(coords[cities[0]][0])
        y_values.append(coords[cities[0]][1])
    plot_data = DataFrame({'x_val': x_values, 'y_val': y_values})
    plot('x_val', 'y_val', data=plot_data, linestyle='-', marker='o')
    title(f'Total Distance Travelled: {best.get_dist()}')
    for i, label in enumerate(best.get_dir()):
        x = x_values[i]
        y = y_values[i]
        text(x+5, y+5, label, fontsize=9)
    show()


if __name__ == '__main__':
    main()
