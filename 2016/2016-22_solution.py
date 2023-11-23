from dataclasses import dataclass
from itertools import product


@dataclass
class Node:
    x: int
    y: int
    size: int
    used: int

    @property
    def avail(self) -> int:
        return self.size - self.used

    @property
    def used_percent(self) -> float:
        return self.used / self.size

    @classmethod
    def from_string(cls, s: str) -> "Node":
        path, size, used, avail, used_percent = s.split()
        devgrid, x, y = path.split("-")
        assert devgrid == "/dev/grid/node"

        assert x.startswith("x")
        x = int(x[1:])
        assert y.startswith("y")
        y = int(y[1:])
        assert size.endswith("T")
        size = int(size[:-1])
        assert used.endswith("T")
        used = int(used[:-1])

        node = cls(x, y, size, used)

        assert avail.endswith("T")
        assert node.avail == int(avail[:-1])
        assert used_percent.endswith("%")
        assert int(node.used_percent * 100) == int(used_percent[:-1])

        return node


def read_input(input_file) -> list[Node]:
    with open(input_file, "r") as f:
        assert f.readline().strip().endswith("df -h")
        assert f.readline().strip().startswith("Filesystem")
        return [Node.from_string(line.rstrip()) for line in f]


def part1(puzzle_input: list[Node]) -> int:
    return sum(
        0 < node_a.used <= node_b.avail
        for node_a, node_b in product(puzzle_input, puzzle_input)
        if node_a != node_b
    )


import matplotlib.pyplot as plt


class Grid:
    def __init__(self, nodes: list[Node]) -> None:
        self.max_x = max(node.x for node in nodes)
        self.max_y = max(node.y for node in nodes)
        self.grid = [
            [None for _ in range(self.max_x + 1)]
            for _ in range(self.max_y + 1)
        ]
        for node in nodes:
            self.grid[node.y][node.x] = node

    def avail_grid(self) -> list[list[int]]:
        return [[node.avail for node in row] for row in self.grid]

    def used_grid(self) -> list[list[int]]:
        return [[node.used for node in row] for row in self.grid]

    def plot(self, title: str = "") -> None:
        plt.imshow(self.avail_grid(), interpolation="none", origin="lower")
        plt.plot(self.max_x, 0, "r.")
        plt.plot(0, 0, "g.")
        if title:
            plt.title(title)
        for row in self.grid:
            for node in row:
                e = self.max_avail()
                if node.used > self.grid[e[0]][e[1]].avail:
                    plt.plot(node.x, node.y, "rx")
        plt.colorbar()
        plt.show()

    def max_avail(self) -> tuple[int, int]:
        free_node = max(
            (node for row in self.grid for node in row),
            key=lambda node: node.avail,
        )
        return free_node.y, free_node.x

    def swap(self, x1: int, y1: int, x2: int, y2: int) -> None:
        node_a, node_b = self.grid[y1][x1], self.grid[y2][x2]
        self.grid[y1][x1], self.grid[y2][x2] = node_b, node_a
        node_a.x, node_a.y, node_b.x, node_b.y = (
            node_b.x,
            node_b.y,
            node_a.x,
            node_a.y,
        )

    def move_data(self, x1: int, y1: int, x2: int, y2: int) -> None:
        if self.grid[y1][x1].avail < self.grid[y2][x2].used:
            raise ValueError("Not enough space")
        self.grid[y2][x2].used += self.grid[y1][x1].used
        self.grid[y1][x1].used = 0


def part2(puzzle_input: list[Node]) -> ...:
    grid = Grid(puzzle_input)
    empty_y, empty_x = grid.max_avail()
    grid.plot()
    assert empty_y < grid.max_y
    moves = 0
    # if all moves were possible, the optimal solution would be:
    # move empty node to (xmax, 0):
    moves += empty_y + (grid.max_x - empty_x)
    # move data left by one node by moving the empty node
    # around it (5 moves per step):
    moves += 5 * (grid.max_x - 1)

    # grid.plot()
    # by inspection, we need 4 extra moves to move the empty
    # node around a line of nodes with too much data
    moves += 4

    return moves


def main() -> None:
    puzzle_input = read_input("2016-22_input.txt")
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
