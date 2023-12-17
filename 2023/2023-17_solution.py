import networkx as nx
import tqdm


def read_input(input_file) -> list[list[int]]:
    with open(input_file, "r") as f:
        return [list(map(int, line)) for line in f.read().splitlines()]


class Map:
    def __init__(
        self,
        grid: list[list[int]],
        min_straight: int = 1,
        max_straight: int = 3,
    ):
        self.grid = grid
        assert all(len(row) == len(grid) for row in grid)
        self.n = len(grid)
        self.min = min_straight
        self.max = max_straight

    def cell_states(self, i: int, j: int):
        if i == j == 0:
            # initial state has no direction
            yield "X", 0
        for d in range(self.max):
            if i - d > 0:
                yield "D", d + 1
            if i + d < self.n - 1:
                yield "U", d + 1
            if j - d > 0:
                yield "R", d + 1
            if j + d < self.n - 1:
                yield "L", d + 1

    def neighbors(self, i: int, j: int, d: str, nd: int):
        if 0 < nd < self.min:
            if d == "D" and i < self.n - 1:
                yield (i + 1, j), ("D", nd + 1)
            elif d == "U" and i > 0:
                yield (i - 1, j), ("U", nd + 1)
            elif d == "R" and j < self.n - 1:
                yield (i, j + 1), ("R", nd + 1)
            elif d == "L" and j > 0:
                yield (i, j - 1), ("L", nd + 1)
            return
        if i < self.n - 1:
            if d == "D":
                if nd < self.max:
                    yield (i + 1, j), ("D", nd + 1)
            elif d != "U":
                yield (i + 1, j), ("D", 1)
        if i > 0:
            if d == "U":
                if nd < self.max:
                    yield (i - 1, j), ("U", nd + 1)
            elif d != "D":
                yield (i - 1, j), ("U", 1)
        if j < self.n - 1:
            if d == "R":
                if nd < self.max:
                    yield (i, j + 1), ("R", nd + 1)
            elif d != "L":
                yield (i, j + 1), ("R", 1)
        if j > 0:
            if d == "L":
                if nd < self.max:
                    yield (i, j - 1), ("L", nd + 1)
            elif d != "R":
                yield (i, j - 1), ("L", 1)

    def generate_graph(self) -> nx.DiGraph:
        g = nx.DiGraph()
        for i in range(self.n):
            for j in range(self.n):
                for state in self.cell_states(i, j):
                    for neighbor in self.neighbors(i, j, *state):
                        h = self.grid[neighbor[0][0]][neighbor[0][1]]
                        g.add_edge(((i, j), state), neighbor, weight=h)
        return g

    def min_heat_loss(self) -> int:
        g = self.generate_graph()
        end_nodes = [
            ((self.n - 1, self.n - 1), s)
            for s in self.cell_states(self.n - 1, self.n - 1)
            if s[1] >= self.min
        ]
        return min(
            nx.shortest_path_length(
                g, ((0, 0), ("X", 0)), end_node, weight="weight"
            )
            for end_node in tqdm.tqdm(end_nodes)
        )


def part1(puzzle_input: list[list[int]]) -> int:
    m = Map(puzzle_input)
    return m.min_heat_loss()


def part2(puzzle_input: list[list[int]]) -> int:
    m = Map(puzzle_input, min_straight=4, max_straight=10)
    return m.min_heat_loss()


def main() -> None:
    puzzle_input = read_input("2023-17_input.txt")
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
