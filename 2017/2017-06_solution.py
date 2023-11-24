def read_input(input_file) -> tuple[int, ...]:
    with open(input_file, "r") as f:
        return tuple(int(i) for i in f.read().split())


def part1(puzzle_input: tuple[int, ...]) -> int:
    state = puzzle_input
    seen = set()
    n_banks = len(state)
    c = 0
    while state not in seen:
        seen.add(state)
        k, n_blocks = max(enumerate(state), key=lambda x: x[1])
        new_state = list(state)
        new_state[k] = 0
        for i in range(n_blocks):
            new_state[(k + i + 1) % n_banks] += 1
        state = tuple(new_state)
        c += 1
    return c


def part2(puzzle_input: tuple[int, ...]) -> int:
    state = puzzle_input
    seen = {}
    n_banks = len(state)
    c = 0
    while state not in seen:
        seen[state] = c
        k, n_blocks = max(enumerate(state), key=lambda x: x[1])
        new_state = list(state)
        new_state[k] = 0
        for i in range(n_blocks):
            new_state[(k + i + 1) % n_banks] += 1
        state = tuple(new_state)
        c += 1
    return c - seen[state]


def main() -> None:
    puzzle_input = read_input("2017-06_input.txt")
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
