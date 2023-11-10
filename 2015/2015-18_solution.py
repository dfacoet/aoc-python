from dataclasses import dataclass

import tqdm


@dataclass
class Lights:
    grid: list[list[bool]]

    def __post_init__(self) -> None:
        assert all(len(row) == len(self.grid) for row in self.grid)

    @property
    def n(self) -> int:
        return len(self.grid)

    def print(self) -> None:
        for row in self.grid:
            print("".join("#" if c else "." for c in row))
        print()

    def neighbours(self, i: int, j: int) -> int:
        n_x = [i]
        n_y = [j]
        if i > 0:
            n_x.append(i - 1)
        if i < self.n - 1:
            n_x.append(i + 1)
        if j > 0:
            n_y.append(j - 1)
        if j < self.n - 1:
            n_y.append(j + 1)
        return sum(self.grid[x][y] for x in n_x for y in n_y) - self.grid[i][j]

    def update(self, fixed: bool = False) -> "Lights":
        new_grid = [[False] * self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j]:
                    new_grid[i][j] = self.neighbours(i, j) in (2, 3)
                else:
                    new_grid[i][j] = self.neighbours(i, j) == 3
        if fixed:
            new_grid[0][0] = True
            new_grid[0][self.n - 1] = True
            new_grid[self.n - 1][0] = True
            new_grid[self.n - 1][self.n - 1] = True
        return Lights(new_grid)

    def count_on(self) -> int:
        return sum(sum(r) for r in self.grid)


def read_input(input_file) -> Lights:
    with open(input_file, "r") as f:
        grid = [[c == "#" for c in line.strip()] for line in f]
    return Lights(grid)


def part1(lights: Lights) -> int:
    for _ in tqdm.trange(100):
        lights = lights.update()
    return lights.count_on()


def part2(lights: Lights) -> int:
    for _ in tqdm.trange(100):
        lights = lights.update(fixed=True)
    return lights.count_on()


def main() -> None:
    input = read_input("2015-18_input.txt")
    print("Part 1: ")
    print("-------")
    print(part1(input))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(input))
    print("=======\n")


if __name__ == "__main__":
    main()
