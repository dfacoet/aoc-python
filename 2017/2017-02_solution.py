def read_input(input_file) -> list[list[int]]:
    with open(input_file, "r") as f:
        return [list(map(int, line.split())) for line in f.readlines()]


def part1(puzzle_input: str) -> int:
    return sum(max(row) - min(row) for row in puzzle_input)


def divide_row(row: list[int]) -> int:
    numbers = sorted(row)
    for i, a in enumerate(numbers):
        for b in numbers[i + 1 :]:
            if b % a == 0:
                return b // a


def part2(puzzle_input: str) -> int:
    return sum(divide_row(row) for row in puzzle_input)


def main() -> None:
    puzzle_input = read_input("2017-02_input.txt")
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
