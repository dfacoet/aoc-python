import numpy as np


def read_input(input_file) -> list[str]:
    with open(input_file) as f:
        return f.read().splitlines()


class Screen:
    def __init__(self) -> None:
        self.pixels = np.zeros((6, 50), dtype=bool)

    def print(self) -> None:
        for row in self.pixels:
            print("".join("#" if x else " " for x in row))

    def rect(self, a: int, b: int) -> None:
        self.pixels[:b, :a] = True

    def rotate_row(self, a: int, b: int) -> None:
        self.pixels[a] = np.roll(self.pixels[a], b)

    def rotate_column(self, a: int, b: int) -> None:
        self.pixels[:, a] = np.roll(self.pixels[:, a], b)

    def execute(self, command: str) -> None:
        match command.split():
            case ["rect", axb]:
                a, b = axb.split("x")
                self.rect(int(a), int(b))
            case ["rotate", "row", y, "by", b]:
                assert y[:2] == "y="
                a = y[2:]
                self.rotate_row(int(a), int(b))
            case ["rotate", "column", x, "by", b]:
                assert x[:2] == "x="
                a = x[2:]
                self.rotate_column(int(a), int(b))
            case _:
                raise ValueError(f"Invalid command: {command}")

    def count_active_pixels(self) -> int:
        return np.sum(self.pixels)


def part1(input: list[str]) -> int:
    screen = Screen()
    for command in input:
        screen.execute(command)
    return screen.count_active_pixels()


def part2(input: list[str]) -> None:
    screen = Screen()
    for command in input:
        screen.execute(command)
    screen.print()


def main() -> None:
    input = read_input("2016-08_input.txt")
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
