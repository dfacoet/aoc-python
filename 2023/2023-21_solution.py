from collections import Counter

import networkx as nx


def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


def create_graph(
    puzzle_input: list[str],
) -> tuple[nx.Graph, tuple[int, int], int]:
    assert all(len(row) == (n := len(puzzle_input)) for row in puzzle_input)
    g = nx.Graph()
    for i, row in enumerate(puzzle_input):
        for j, c in enumerate(row):
            if c == "S":
                start = (i, j)
            if c in ".S":
                for ni, nj in [(i + 1, j), (i, j + 1)]:
                    if (
                        0 <= ni < n
                        and 0 <= nj < n
                        and puzzle_input[ni][nj] in ".S"
                    ):
                        g.add_edge((i, j), (ni, nj))
    return g, start, n


def count_accessible(
    g: nx.Graph, start: tuple[int, int], max_steps: int
) -> int:
    lengths = nx.single_source_shortest_path_length(g, start, max_steps)
    parity = max_steps % 2
    # print(max(lengths.values()))
    return sum(1 for d in lengths.values() if d % 2 == parity)


def part1(puzzle_input: list[str]) -> int:
    g, start, _ = create_graph(puzzle_input)
    return count_accessible(g, start, 64)


def part2(puzzle_input: list[str]) -> int:
    max_d = 26501365
    g, start, n = create_graph(puzzle_input)

    # Check that that there are not obstacles between start and edges,
    # or between tiles along the edges
    assert (
        set(puzzle_input[start[0]])
        == set(r[start[1]] for r in puzzle_input)
        == set(".S")
    )
    assert (
        set(puzzle_input[0] + puzzle_input[-1])
        == set(row[0] for row in puzzle_input)
        == set(row[-1] for row in puzzle_input)
        == {"."}
    )
    d = max_d // n
    assert max_d % n == n // 2
    assert max_d % 2 == 1
    assert n % 2 == 1
    assert d % 2 == 0

    # Within the bulk, cells reachable in an odd number of steps are
    # the odd cells in even tiles, or even cells in odd tiles
    n_cells_by_parity = Counter(
        d % 2 for d in nx.single_source_shortest_path_length(g, start).values()
    )
    reachable = (d - 1) ** 2 * n_cells_by_parity[
        1
    ] + d**2 * n_cells_by_parity[0]
    # Can enter vertex tiles (one per direction) with n-1 steps left
    for start in ((0, n // 2), (n // 2, 0), (n - 1, n // 2), (n // 2, n - 1)):
        reachable += count_accessible(g, start, n - 1)
    # Can enter edge tiles (d-1 per direction) with 2n-n//2-2 steps left
    # second edge tiles (d per direction) with n-n//2-2 steps left
    for start in ((0, 0), (0, n - 1), (n - 1, 0), (n - 1, n - 1)):
        reachable += (d - 1) * count_accessible(g, start, 2 * n - n // 2 - 2)
        reachable += d * count_accessible(g, start, n - n // 2 - 2)

    return reachable


def main() -> None:
    puzzle_input = read_input("2023-21_input.txt")
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
