from collections.abc import Iterator


def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


class Pipes:
    def __init__(self, grid: list[str]) -> None:
        self.grid = grid
        self.start = self._find_start()

    def _find_start(self) -> tuple[int, int]:
        for i, row in enumerate(self.grid):
            try:
                return (i, row.index("S"))
            except ValueError:
                continue
        raise ValueError("No start found")

    def _get_neighbor_pipes(self, i: int, j: int) -> list[tuple[int, int]]:
        c = self.grid[i][j]
        match c:
            case "S":
                neighbors = [
                    (k, m)
                    for k, m in [
                        (i + 1, j),
                        (i - 1, j),
                        (i, j + 1),
                        (i, j - 1),
                    ]
                    if (i, j) in self._get_neighbor_pipes(k, m)
                ]
            case "|":
                neighbors = [(i + 1, j), (i - 1, j)]
            case "-":
                neighbors = [(i, j + 1), (i, j - 1)]
            case "L":
                neighbors = [(i - 1, j), (i, j + 1)]
            case "J":
                neighbors = [(i - 1, j), (i, j - 1)]
            case "7":
                neighbors = [(i + 1, j), (i, j - 1)]
            case "F":
                neighbors = [(i + 1, j), (i, j + 1)]
            case ".":
                neighbors = []
        return [
            (k, m)
            for k, m in neighbors
            if 0 <= k < len(self.grid) and 0 <= m < len(self.grid[0])
        ]

    def find_loop(self) -> tuple[int, set[tuple[int, int]]]:
        visited = set()
        to_visit = {self.start}
        d = -1
        while to_visit:
            # print(to_visit)
            next_step: set[tuple[int, int]] = set()
            for current in to_visit:
                visited.add(current)
                next_step.update(
                    neighbor
                    for neighbor in self._get_neighbor_pipes(*current)
                    if neighbor not in visited
                )
            d += 1
            to_visit = next_step
        return d, visited

    def _get_neighbors(self, i: int, j: int) -> Iterator[tuple[int, int]]:
        if i > 0:
            yield (i - 1, j)
        if i < len(self.grid) - 1:
            yield (i + 1, j)
        if j > 0:
            yield (i, j - 1)
        if j < len(self.grid[i]) - 1:
            yield (i, j + 1)

    def triple_grid(self) -> list[list[int]]:
        new_grid = [
            [0 for _ in range(3) for _ in row]
            for _ in range(3)
            for row in self.grid
        ]
        _, loop = self.find_loop()
        for i, j in loop:
            new_grid[3 * i][3 * j] = 1
            for k, m in self._get_neighbor_pipes(i, j):
                di, dj = k - i, m - j
                new_grid[3 * i + di][3 * j + dj] = 1
        # fill external component
        to_visit = {(0, 0)}
        while to_visit:
            i, j = to_visit.pop()
            new_grid[i][j] = 1
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                try:
                    if new_grid[i + di][j + dj] == 0:
                        to_visit.add((i + di, j + dj))
                except IndexError:
                    pass
        return new_grid

    def find_enclosed_tiles(self) -> int:
        triple_grid = self.triple_grid()
        return sum(
            1
            for i, row in enumerate(self.grid)
            for j in range(len(row))
            if triple_grid[3 * i][3 * j] == 0
        )


def part1(puzzle_input: list[str]) -> int:
    pipes = Pipes(puzzle_input)
    max_distance, _ = pipes.find_loop()
    return max_distance


def part2(puzzle_input: list[str]) -> int:
    pipes = Pipes(puzzle_input)
    return pipes.find_enclosed_tiles()


def main() -> None:
    puzzle_input = read_input("2023-10_input.txt")
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
