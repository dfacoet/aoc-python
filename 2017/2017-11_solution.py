from collections import Counter
from typing import Literal


def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().strip().split(",")


cube_directions = {
    "n": (0, -1, 1),
    "ne": (1, -1, 0),
    "se": (1, 0, -1),
    "s": (0, 1, -1),
    "sw": (-1, 1, 0),
    "nw": (-1, 0, 1),
}


class CubeCoord:
    def __init__(self, qrs: tuple[int, int, int] = (0, 0, 0)) -> None:
        assert sum(qrs) == 0
        self.q, self.r, self.s = qrs

    def __add__(self, other: tuple[int, int, int]) -> "CubeCoord":
        return CubeCoord(
            (self.q + other[0], self.r + other[1], self.s + other[2])
        )

    def neighbour(
        self, direction: Literal["n", "ne", "se", "s", "sw", "nw"]
    ) -> dict[str, "CubeCoord"]:
        return self + cube_directions[direction]

    def norm(self) -> int:
        return max(abs(self.q), abs(self.r), abs(self.s))


def part1(puzzle_input: list[str]) -> int:
    steps = Counter(puzzle_input)
    s = steps["n"] - steps["s"] + steps["nw"] - steps["se"]
    r = steps["s"] - steps["n"] + steps["sw"] - steps["ne"]
    q = steps["ne"] + steps["se"] - steps["nw"] - steps["sw"]
    return CubeCoord((q, r, s)).norm()


def part2(puzzle_input: list[str]) -> int:
    x = CubeCoord()
    max_distance = 0
    for step in puzzle_input:
        x = x.neighbour(step)
        max_distance = max(max_distance, x.norm())
    return max_distance


def main() -> None:
    puzzle_input = read_input("2017-11_input.txt")
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
