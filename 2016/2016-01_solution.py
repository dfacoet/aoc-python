from dataclasses import dataclass
from typing import Literal, TypeAlias

Directions: TypeAlias = list[tuple[Literal["L", "R"], int]]


def read_input(input_file) -> Directions:
    with open(input_file, "r") as f:
        return [(s[0], int(s[1:])) for s in f.readline().split(", ")]


def part1(input: Directions) -> int:
    cardinal_directions = ["N", "E", "S", "W"]
    steps = dict.fromkeys(cardinal_directions, 0)
    i = 0
    for turn, s in input:
        i = (i + (1 if turn == "R" else -1)) % 4
        steps[cardinal_directions[i]] += s
    x = steps["E"] - steps["W"]
    y = steps["N"] - steps["S"]
    return abs(x) + abs(y)


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def distance(self) -> int:
        return abs(self.x) + abs(self.y)


def part2(input: Directions) -> int:
    direction_steps = [Coord(0, 1), Coord(1, 0), Coord(0, -1), Coord(-1, 0)]
    i = 0
    visited = set()
    position = Coord(0, 0)
    for turn, s in input:
        i = (i + (1 if turn == "R" else -1)) % 4
        for _ in range(s):
            position += direction_steps[i]
            if position in visited:
                return position.distance()
            visited.add(position)
    return -1


def main() -> None:
    input = read_input("2016-01_input.txt")
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
