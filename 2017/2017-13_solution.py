def read_input(input_file) -> list[tuple[int, int]]:
    with open(input_file, "r") as f:
        return [
            tuple(int(x) for x in line.split(": "))
            for line in f.read().splitlines()
        ]


def is_caught(depth, range):
    return depth % (2 * (range - 1)) == 0


def severity(depth, range):
    return depth * range


def part1(puzzle_input: list[tuple[int, int]]) -> int:
    return sum(
        severity(depth, range)
        for depth, range in puzzle_input
        if is_caught(depth, range)
    )


def part2(puzzle_input: list[tuple[int, int]]) -> int:
    delay = 0
    while any(
        is_caught(depth + delay, range) for depth, range in puzzle_input
    ):
        delay += 1
    return delay


def main() -> None:
    puzzle_input = read_input("2017-13_input.txt")
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
