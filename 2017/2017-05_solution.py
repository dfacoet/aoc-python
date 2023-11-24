def read_input(input_file) -> tuple[int, ...]:
    with open(input_file, "r") as f:
        return tuple(int(line) for line in f.read().splitlines())


def part1(puzzle_input: tuple[int, ...]) -> int:
    instructions = list(puzzle_input)
    i = 0
    steps = 0
    while i < len(instructions):
        j = instructions[i]
        instructions[i] += 1
        i += j
        steps += 1
    return steps


def part2(puzzle_input: tuple[int, ...]) -> int:
    instructions = list(puzzle_input)
    i = 0
    steps = 0
    while i < len(instructions):
        if (j := instructions[i]) >= 3:
            instructions[i] -= 1
        else:
            instructions[i] += 1
        i += j
        steps += 1
    return steps


def main() -> None:
    puzzle_input = read_input("2017-05_input.txt")
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
