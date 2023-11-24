from itertools import permutations

import matplotlib.pyplot as plt
import networkx as nx


def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


class Maze:
    def __init__(self, map: list[str]) -> None:
        self.map = [[int(c == "#") for c in line] for line in map]

        self.locations: list[tuple[int, tuple[int, int]]] = []
        for i, row in enumerate(map):
            for j, c in enumerate(row):
                if c.isdigit():
                    self.locations.append((int(c), (i, j)))
        self.locations.sort()

        big_graph = nx.Graph()
        for i, line in enumerate(map):
            for j, c in enumerate(line):
                if c == "#":
                    continue
                else:
                    big_graph.add_node((i, j))
                    if map[i - 1][j] != "#":
                        big_graph.add_edge((i, j), (i - 1, j))
                    if map[i][j - 1] != "#":
                        big_graph.add_edge((i, j), (i, j - 1))

        self.distances = [
            [
                nx.shortest_path_length(big_graph, n1, n2)
                for _, n1 in self.locations
            ]
            for _, n2 in self.locations
        ]

    def plot(self) -> None:
        plt.imshow(self.map)
        for v, (i, j) in self.locations:
            if v == 0:
                color = "green"
            else:
                color = "red"
            plt.plot(j, i, ".", color=color)

        plt.show()

    def path_length(self, path: tuple[int, ...]) -> int:
        return sum(self.distances[i][j] for i, j in zip(path, path[1:]))

    def find_shortest_path(self) -> int:
        return min(
            self.path_length((0,) + p)
            for p in permutations(range(1, len(self.locations)))
        )

    def find_shortest_cycle(self) -> int:
        return min(
            self.path_length((0,) + p + (0,))
            for p in permutations(range(1, len(self.locations)))
        )


def part1(puzzle_input: list[str]) -> int:
    maze = Maze(puzzle_input)
    return maze.find_shortest_path()


def part2(puzzle_input: list[str]) -> int:
    maze = Maze(puzzle_input)
    return maze.find_shortest_cycle()


def main() -> None:
    puzzle_input = read_input("2016-24_input.txt")
    print("Part 1: ")
    print("-------")
    print(part1(puzzle_input))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(puzzle_input))
    print("=======\n")


if __name__ == "__main__":
    main()
