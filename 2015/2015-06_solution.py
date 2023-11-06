from dataclasses import dataclass
from typing import Literal

import numpy as np


@dataclass
class Coord:
    x: int
    y: int


@dataclass
class Instruction:
    operation: Literal["turn on", "turn off", "toggle"]
    start: Coord
    end: Coord

    @classmethod
    def from_string(cls, s: str) -> "Instruction":
        tokens = s.split()
        start, _through, end = tokens[-3:]
        operation = " ".join(tokens[:-3])
        assert _through == "through"
        start = Coord(*map(int, start.split(",")))
        end = Coord(*map(int, end.split(",")))
        return cls(operation, start, end)


def read_input(input_file) -> list[Instruction]:
    with open(input_file, "r") as f:
        return [Instruction.from_string(line) for line in f.readlines()]


def part1(instructions: list[Instruction]) -> int:
    grid = np.zeros((1000, 1000), dtype=bool)
    for instruction in instructions:
        match instruction.operation:
            case "turn on":
                grid[
                    instruction.start.x : instruction.end.x + 1,
                    instruction.start.y : instruction.end.y + 1,
                ] = True
            case "turn off":
                grid[
                    instruction.start.x : instruction.end.x + 1,
                    instruction.start.y : instruction.end.y + 1,
                ] = False
            case "toggle":
                grid[
                    instruction.start.x : instruction.end.x + 1,
                    instruction.start.y : instruction.end.y + 1,
                ] = np.logical_not(
                    grid[
                        instruction.start.x : instruction.end.x + 1,
                        instruction.start.y : instruction.end.y + 1,
                    ]
                )
    return grid.sum()


def part2(instructions: list[Instruction]) -> int:
    grid = np.zeros((1000, 1000), dtype=int)
    for instruction in instructions:
        match instruction.operation:
            case "turn on":
                grid[
                    instruction.start.x : instruction.end.x + 1,
                    instruction.start.y : instruction.end.y + 1,
                ] += 1
            case "turn off":
                grid[
                    instruction.start.x : instruction.end.x + 1,
                    instruction.start.y : instruction.end.y + 1,
                ] -= 1
                grid[grid < 0] = 0
            case "toggle":
                grid[
                    instruction.start.x : instruction.end.x + 1,
                    instruction.start.y : instruction.end.y + 1,
                ] += 2
    return grid.sum()


def main() -> None:
    instructions = read_input("2015-06_input.txt")
    print("Part 1: ")
    print("-------")
    print(part1(instructions))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(instructions))
    print("=======\n")


if __name__ == "__main__":
    main()
