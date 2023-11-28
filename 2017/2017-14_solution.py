import operator
from collections import defaultdict
from functools import reduce
from itertools import product


def read_input(input_file) -> str:
    with open(input_file, "r") as f:
        return f.read().strip()


class Knot:
    def __init__(self, size: int) -> None:
        self.n = size
        self.knot = list(range(size))

    def reverse(self, start: int, length: int) -> None:
        if length >= self.n:
            # NOTE: length == self.n could be valid but is not used in this puzzle
            raise ValueError("Length cannot be greater than size of knot")
        start %= self.n
        if (stop := start + length) > self.n:
            stop %= self.n
        if start < stop:
            end = start - 1 if start > 0 else None
            self.knot[start:stop] = self.knot[stop - 1 : end : -1]
        elif start > stop:
            reversed = (self.knot[start:] + self.knot[:stop])[::-1]
            self.knot[start:] = reversed[: self.n - start]
            self.knot[:stop] = reversed[self.n - start :]

    def __repr__(self) -> str:
        return f"Knot({self.knot})"

    def dense_hash(self) -> list[int]:
        hash_ints = [
            reduce(operator.xor, self.knot[16 * i : 16 * (i + 1)])
            for i in range(self.n // 16)
        ]
        hash_str = "".join(f"{n:08b}" for n in hash_ints)
        return hash_str


def knot_hash(string: str) -> str:
    knot = Knot(256)
    s, i = 0, 0
    lengths = [ord(c) for c in string] + [17, 31, 73, 47, 23]
    for _ in range(64):
        for length in lengths:
            knot.reverse(i, length)
            i = i + length + s
            s = s + 1
    return knot.dense_hash()


def part1(puzzle_input: str) -> int:
    return sum(knot_hash(f"{puzzle_input}-{i}").count("1") for i in range(128))


class Graph:
    def __init__(self) -> None:
        self.edges = defaultdict(set)

    def add_edge(self, node1: tuple[int, int], node2: tuple[int, int]) -> None:
        self.edges[node1].add(node2)
        self.edges[node2].add(node1)

    def find_connected(self, start: tuple[int, int]) -> set[tuple[int, int]]:
        component = set()
        to_visit = {start}
        while to_visit:
            node = to_visit.pop()
            component.add(node)
            to_visit.update(self.edges[node] - component)
        return component


def part2(puzzle_input: str) -> int:
    used_grid = [
        [c == "1" for c in knot_hash(f"{puzzle_input}-{i}")]
        for i in range(128)
    ]
    g = Graph()

    not_visited = set()
    for i in range(128):
        for j in range(128):
            if used_grid[i][j]:
                not_visited.add((i, j))
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    try:
                        if used_grid[i + dx][j + dy]:
                            g.add_edge((i, j), (i + dx, j + dy))
                    except IndexError:
                        pass

    n_components = 0
    while not_visited:
        component = g.find_connected(not_visited.pop())
        not_visited -= component
        n_components += 1
    return n_components


def main() -> None:
    puzzle_input = read_input("2017-14_input.txt")
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
