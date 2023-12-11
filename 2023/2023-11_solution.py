def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


class Image:
    def __init__(self, grid: list[str], scale: int = 2) -> None:
        self.grid = grid
        self.scale = scale
        assert all(len(row) == len(grid[0]) for row in grid)
        self.galaxies = tuple(self._find_galaxies())
        self.empty_rows = tuple(self._iter_empty_rows())
        self.empty_cols = tuple(self._iter_empty_cols())

    @property
    def m(self) -> int:
        assert all(len(row) == len(self.grid[0]) for row in self.grid)
        return len(self.grid[0])

    def _iter_empty_rows(self):
        for i, row in enumerate(self.grid):
            if not any(c == "#" for c in row):
                yield i

    def _iter_empty_cols(self):
        for j in range(self.m):
            if not any(row[j] == "#" for row in self.grid):
                yield j

    def _find_galaxies(self):
        for i, row in enumerate(self.grid):
            for j, c in enumerate(row):
                if c == "#":
                    yield (i, j)

    def total_distance(self):
        total_distance = 0
        for i1, g1 in enumerate(self.galaxies):
            for g2 in self.galaxies[:i1]:
                total_distance += self.dist(*g1, *g2)
        return total_distance

    def dist(self, i1, j1, i2, j2):
        # TODO: avoid iterations by storing n_empty_rows_up_to
        extra_space = sum(
            i in self.empty_rows for i in range(min(i1, i2), max(i1, i2))
        ) + sum(j in self.empty_cols for j in range(min(j1, j2), max(j1, j2)))
        return abs(i1 - i2) + abs(j1 - j2) + (self.scale - 1) * extra_space


def part1(puzzle_input: list[str]) -> int:
    image = Image(puzzle_input)
    return image.total_distance()


def part2(puzzle_input: list[str]) -> int:
    image = Image(puzzle_input, scale=1_000_000)
    return image.total_distance()


def main() -> None:
    puzzle_input = read_input("2023-11_input.txt")
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
