import math


def read_input(input_file) -> list[tuple[int, int]]:
    with open(input_file, "r") as f:
        times = map(int, f.readline().strip().split()[1:])
        distances = map(int, f.readline().strip().split()[1:])
    return list(zip(times, distances))


def count_ways(time: int, distance: int) -> int:
    if (d2 := time**2 - 4 * (distance + 1)) < 0:
        return 0
    cmax = int(math.floor((time + math.sqrt(d2)) / 2))
    cmin = int(math.ceil((time - math.sqrt(d2)) / 2))
    return cmax - cmin + 1


def prod(iterable, base=1):
    p = base
    for i in iterable:
        p *= i
    return p


def part1(puzzle_input: list[tuple[int, int]]) -> int:
    return prod(count_ways(*t) for t in puzzle_input)


def reparse(numbers: list[int]) -> int:
    return int("".join(map(str, numbers)))


def part2(puzzle_input: list[tuple[int, int]]) -> int:
    time, distance = map(reparse, zip(*puzzle_input))
    return count_ways(time, distance)


def main() -> None:
    puzzle_input = read_input("2023-06_input.txt")
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
