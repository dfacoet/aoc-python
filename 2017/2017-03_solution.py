import math
from collections.abc import Iterator


def read_input(input_file) -> int:
    with open(input_file, "r") as f:
        return int(f.read().strip())


def part1(puzzle_input: int) -> int:
    # (2*k+1)**2 is the largest square of an odd number smaller than input
    # it sits in the bottom right corner of the square, at distance 2k.
    k = int((math.sqrt(puzzle_input) - 1) // 2)
    if puzzle_input == (2 * k + 1) ** 2:
        return 2 * k
    r = (puzzle_input - (2 * k + 1) ** 2) % (2 * k + 2)
    # the input is at distance r from one of the corners in the next layer
    return 2 * (k + 1) - min(r, 2 * k + 2 - r)


def spiral_indices() -> Iterator[tuple[int, int]]:
    # yield 0, 0
    k = 0
    while True:
        k += 1
        for y in range(-k + 1, k + 1):
            yield k, y
        for x in range(k - 1, -k - 1, -1):
            yield x, k
        for y in range(k - 1, -k - 1, -1):
            yield -k, y
        for x in range(-k + 1, k + 1):
            yield x, -k


def neighbors(p: tuple[int, int]) -> Iterator[tuple[int, int]]:
    x, y = p
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx != 0 or dy != 0:
                yield x + dx, y + dy


def part2(puzzle_input: int) -> int:
    values = {(0, 0): 1}
    for p in spiral_indices():
        value = sum(values.get(n, 0) for n in neighbors(p))
        if value > puzzle_input:
            return value
        values[p] = value
    raise RuntimeError("No solution found")


def main() -> None:
    puzzle_input = read_input("2017-03_input.txt")
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
