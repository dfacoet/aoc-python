from dataclasses import dataclass
from functools import cached_property


def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


@dataclass
class Engine:
    schematic: list[str]

    def neighbors(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == dy == 0:
                    continue
                try:
                    yield self.schematic[y + dy][x + dx]
                except IndexError:
                    continue

    def numbers(self):
        for y, row in enumerate(self.schematic):
            i = 0
            while i < len(row):
                if row[i].isdigit():
                    length = 1
                    while i + length < len(row) and row[i + length].isdigit():
                        length += 1
                    # number, coordinates of first digit, length
                    yield int(row[i : i + length]), (i, y), length
                    i += length
                else:
                    i += 1

    def number_neighbours(self, coords, length):
        x, y = coords
        for i in range(length):
            yield from self.neighbors(x + i, y)

    def is_part(self, coords, length):
        return any(
            neighbor != "." and not neighbor.isdigit()
            for neighbor in self.number_neighbours(coords, length)
        )

    def sum_part_numbers(self):
        return sum(
            number
            for number, coords, length in self.numbers()
            if self.is_part(coords, length)
        )

    @cached_property
    def parts_map(self):
        parts_map = {}
        for number, coords, length in self.numbers():
            if self.is_part(coords, length):
                for i in range(length):
                    parts_map[(coords[0] + i, coords[1])] = number
        return parts_map

    def neighbor_parts(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == dy == 0:
                    continue
                try:
                    yield self.parts_map[(x + dx, y + dy)]
                except (IndexError, KeyError):
                    continue

    def gears(self):
        for y, row in enumerate(self.schematic):
            for x, char in enumerate(row):
                if char == "*":
                    neighbor_parts = set(self.neighbor_parts(x, y))
                    if len(neighbor_parts) == 2:
                        yield neighbor_parts.pop() * neighbor_parts.pop()


def part1(puzzle_input: list[str]) -> int:
    schematic = Engine(puzzle_input)
    return schematic.sum_part_numbers()


def part2(puzzle_input: list[str]) -> int:
    schematic = Engine(puzzle_input)
    return sum(schematic.gears())


def main() -> None:
    puzzle_input = read_input("2023-03_input.txt")
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
