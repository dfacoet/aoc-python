def read_input(input_file) -> list[list[int]]:
    with open(input_file) as f:
        return [list(map(int, line.split())) for line in f]


def extrapolate(sequence: list[int]) -> int:
    final_values = []
    diff = sequence.copy()
    while any(diff):
        final_values.append(diff[-1])
        diff = [a - b for a, b in zip(diff[1:], diff[:-1])]
    return sum(final_values)


def part1(puzzle_input: list[list[int]]) -> int:
    return sum(extrapolate(sequence) for sequence in puzzle_input)


def extrapolate_left(sequence: list[int]) -> int:
    initial_values = []
    diff = sequence.copy()
    while any(diff):
        initial_values.append(diff[0])
        diff = [a - b for a, b in zip(diff[1:], diff[:-1])]
    return sum(initial_values[::2]) - sum(initial_values[1::2])


def part2(puzzle_input: list[list[int]]) -> int:
    return sum(extrapolate_left(sequence) for sequence in puzzle_input)


def main() -> None:
    puzzle_input = read_input("2023-09_input.txt")
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
