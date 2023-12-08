import math


def read_input(input_file) -> tuple[str, dict[str, dict[str, str]]]:
    with open(input_file, "r") as f:
        lines = f.read().splitlines()
    assert lines[1] == ""
    network_map = {}
    for line in lines[2:]:
        parent, children = line.split(" = ")
        network_map[parent] = dict(zip("LR", children.strip("()").split(", ")))
    return lines[0], network_map


def part1(puzzle_input: tuple[str, dict[str, dict[str, str]]]) -> int:
    instructions, network_map = puzzle_input
    current = "AAA"
    c = 0
    while current != "ZZZ":
        current = network_map[current][instructions[c % len(instructions)]]
        c += 1
    return c


def part2(puzzle_input: tuple[str, dict[str, dict[str, str]]]) -> int:
    instructions, network_map = puzzle_input
    starting_positions = [node for node in network_map if node.endswith("A")]
    # find periods
    periods = []
    for current in starting_positions:
        c = 0
        while not current.endswith("Z"):
            current = network_map[current][instructions[c % len(instructions)]]
            c += 1
        period = c
        # check that time to first hit is actually a period
        assert period % len(instructions) == 0
        z = current
        for c in range(period, 2 * period):
            current = network_map[current][instructions[c % len(instructions)]]
        assert current == z
        periods.append(period)
    return math.lcm(*periods)


def main() -> None:
    puzzle_input = read_input("2023-08_input.txt")
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
