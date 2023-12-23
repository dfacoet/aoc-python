from collections import defaultdict
from typing import Iterator


def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


def neighbours(char: str) -> Iterator[tuple[int, int]]:
    if char == "#":
        return
    if char in ".>":
        yield (0, 1)
    if char in ".<":
        yield (0, -1)
    if char in ".^":
        yield (-1, 0)
    if char in ".v":
        yield (1, 0)


def parse_map(
    grid: list[str],
) -> dict[tuple[int, int], list[tuple[int, int]]]:
    map_graph = defaultdict(list)
    assert {c for row in grid for c in row} <= set(".#^v<>")
    assert all(len(row) == (n := len(grid)) for row in grid)
    assert grid[0][1] == grid[-1][-2] == "."
    assert set(grid[0][2:]) == set(grid[-1][:-2]) == {"#"}
    assert all(row[-1] == "#" for row in grid)
    map_graph[(0, 1)] = [(1, 1)]
    map_graph[(n - 1, n - 2)] = [(n - 2, n - 2)]
    for i, row in enumerate(grid):
        if i in (0, n - 1):
            continue
        for j, c in enumerate(row):
            if j in (0, n - 1):
                continue
            if c != "#":
                for di, dj in neighbours(c):
                    if grid[i + di][j + dj] != "#":
                        map_graph[(i, j)].append((i + di, j + dj))
    return dict(map_graph)


def find_longest_path(
    map_graph: dict[tuple[int, int], list[tuple[int, int]]],
    start: tuple[int, int],
    end: tuple[int, int],
) -> int:
    open_paths = [[start]]
    max_len = 0
    while open_paths:
        path = open_paths.pop()
        for next_node in map_graph[path[-1]]:
            if next_node == end:
                max_len = max(max_len, len(path))
            elif next_node not in path:
                open_paths.append(path + [next_node])
    return max_len


def condense_graph(graph):
    # node -> [(neighbour, distance)]
    condensed_graph = {k: [(x, 1) for x in v] for k, v in graph.items()}
    while links := [k for k, v in condensed_graph.items() if len(v) == 2]:
        for link in links:
            left, right = condensed_graph[link]
            condensed_graph[left[0]].remove((link, left[1]))
            condensed_graph[right[0]].remove((link, right[1]))
            condensed_graph[left[0]].append((right[0], left[1] + right[1]))
            condensed_graph[right[0]].append((left[0], left[1] + right[1]))
            del condensed_graph[link]
    return condensed_graph


def parse_map2(grid):
    # Ignore slopes
    new_grid = []
    for row in grid:
        for s in "^v<>":
            row = row.replace(s, ".")
        new_grid.append(row)
    return condense_graph(parse_map(new_grid))


def find_longest_path_weighted(
    map_graph: dict[tuple[int, int], list[tuple[tuple[int, int], int]]],
    start: tuple[int, int],
    end: tuple[int, int],
) -> int:
    open_paths = [([start], 0)]
    max_len = 0
    while open_paths:
        path, length = open_paths.pop()
        for next_node, dist in map_graph[path[-1]]:
            if next_node == end:
                max_len = max(max_len, length + dist)
            elif next_node not in path:
                open_paths.append((path + [next_node], length + dist))
    return max_len


def part1(puzzle_input: list[str]) -> int:
    assert all(len(row) == (n := len(puzzle_input)) for row in puzzle_input)
    map_graph = parse_map(puzzle_input)
    return find_longest_path(map_graph, (0, 1), (n - 1, n - 2))


def part2(puzzle_input: list[str]) -> int:
    assert all(len(row) == (n := len(puzzle_input)) for row in puzzle_input)
    map_graph = parse_map2(puzzle_input)
    return find_longest_path_weighted(map_graph, (0, 1), (n - 1, n - 2))


def main() -> None:
    puzzle_input = read_input("2023-23_input.txt")
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
