def read_input(input_file) -> str:
    with open(input_file, "r") as f:
        return f.read().strip()


def part1(puzzle_input: str) -> int:
    shifted = puzzle_input[1:] + puzzle_input[0]
    return sum(int(c) for c, d in zip(puzzle_input, shifted) if c == d)


def part2(puzzle_input: str) -> int:
    n = len(puzzle_input) // 2
    shifted = puzzle_input[n:] + puzzle_input[:n]
    return sum(int(c) for c, d in zip(puzzle_input, shifted) if c == d)


def main() -> None:
    puzzle_input = read_input("2017-01_input.txt")
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
