def read_input(filename: str) -> int:
    with open(filename, "r") as f:
        return int(f.read())


def part1(puzzle_input: int) -> int:
    buffer = [0]
    i = 0
    for n in range(2017):
        i = (i + puzzle_input) % (n + 1) + 1
        buffer.insert(i, n + 1)
    return buffer[i + 1]


import tqdm


def part2(puzzle_input: int) -> int:
    i = 0
    v = 0  # value at index 1 (after 0)
    for n in (pbar := tqdm.trange(50_000_000)):
        # current buffer length is n + 1
        i = (i + puzzle_input) % (n + 1) + 1
        if i == 1:
            v = n + 1
            pbar.set_description(f"[0 {v} ...]")
    return v


def main() -> None:
    puzzle_input = read_input("2017-17_input.txt")
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
