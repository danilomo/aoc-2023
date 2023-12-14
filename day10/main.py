import unittest
import sys

sample_input_1 = """.....
.S-7.
.|.|.
.L-J.
....."""

sample_input_2 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""


def adj(coord, *elements):
    pass

increments_table = {
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "F": [(1, 0), (0, 1)],
    "7": [(1, 0), (0, -1)],
    "S": [(-1, 0), (1, 0), (0, -1), (0, 1)]
}


def parse_input(lines):
    return [
        list(line) 
        for line in lines
    ]

def initial_pos(graph):
    for i in range(0, len(graph)):
        for j in range(0, len(graph[0])):
            if graph[i][j] == "S":
                return (i,j)

def get(graph, pos, default=None):
    i, j = pos
    try:
        return graph[i][j]
    except:
        return default

def adjascent_tiles(graph, pos):
    i, j = pos
    value = get(graph, pos)
    for incr in increments_table.get(value, []):
        incr_i, incr_j = incr
        next_i, next_j = i + incr_i, j + incr_j
        if get(graph, (next_i, next_j)):
            yield (next_i, next_j)

def find_distances_aux(graph, initial_pos, distances):
    tiles = [initial_pos]
    while tiles:
        pos = tiles.pop()

        value = get(graph, pos)

        if not value:
            continue

        i, j = pos

        for tile in adjascent_tiles(graph, pos):
            if pos not in set(adjascent_tiles(graph, tile)):
                continue

            ni, nj = tile

            if distances[ni][nj] >= 0:
                continue

            tiles.append(tile)
            distances[ni][nj] = distances[i][j] + 1

        tiles.sort(key= lambda t: -get(distances, t, float("-inf")))

def find_max_distance(graph):
    m = len(graph)
    n = len(graph[0])

    distances = [list([-1] * n) for _ in range(0, m)]

    pos = initial_pos(graph)
    print(pos)
    pi, pj = pos
    distances[pi][pj] = 0

    find_distances_aux(graph, pos, distances)

    for line in distances:
        print("-", line)

    return max(
        max(val) for val in distances
    )


class TestSuite(unittest.TestCase):
    def test_distances(self):
        cases = [(sample_input_1, 4), (sample_input_2, 8)]

        for input, expected in cases:
            lines = [line.strip() for line in input.split("\n")]
            graph = parse_input(lines)

            max_dst = find_max_distance(graph)
            self.assertEqual(expected, max_dst)


def read_lines(file_name):
    with open(file_name) as handle:
        return [line.strip() for line in handle]

def main():
    lines = read_lines(sys.argv[1])
    graph = parse_input(lines)
    print(find_max_distance(graph))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        unittest.main()
    else:
        main()
