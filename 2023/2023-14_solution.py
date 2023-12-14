def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


class Platform:
    def __init__(self, map: list[str]) -> None:
        self.grid = [list(row) for row in map]

    def tilt_north(self) -> None:
        for i, row in enumerate(self.grid):
            for j, c in enumerate(row):
                if c == "O":
                    k = i - 1
                    while k > -1 and self.grid[k][j] == ".":
                        k -= 1
                    if i != k + 1:
                        self.grid[i][j] = "."
                        self.grid[k + 1][j] = "O"

    def total_load(self) -> int:
        return sum(
            (k + 1) * row.count("O") for k, row in enumerate(self.grid[::-1])
        )

    def rotate(self) -> None:
        self.grid = list(map(list, zip(*self.grid[::-1])))

    def cycle(self) -> None:
        for _ in range(4):
            self.tilt_north()
            self.rotate()

    def __str__(self) -> str:
        return "\n".join("".join(row) for row in self.grid)

    def cycles(self, n: int) -> None:
        seen = {}
        for i in range(n):
            seen[str(self)] = i
            self.cycle()
            if str(self) in seen:
                period = i + 1 - seen[str(self)]
                break
        print((n - i - 1) % period)
        for _ in range((n - i - 1) % period):
            self.cycle()


def part1(puzzle_input: list[str]) -> int:
    platform = Platform(puzzle_input)
    platform.tilt_north()
    return platform.total_load()


def part2(puzzle_input: list[str]) -> int:
    platform = Platform(puzzle_input)
    platform.cycles(1_000_000_000)
    return platform.total_load()


def main() -> None:
    puzzle_input = read_input("2023-14_input.txt")
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
