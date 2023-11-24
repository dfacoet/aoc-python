import tqdm


def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


def run_program(a: int) -> ...:
    # HARDCODED / COMPILED PROGRAM:
    # lines 0, 1 are assignments
    # 2-7 is a loop implementing multiplication
    d = a + 182 * 14  # = a + 2548
    # the rest of the program is an infinite loop
    # that can be simplified to:
    while True:
        a = d
        while a:
            b = a
            a = b // 2
            print(1 - b % 2)
    # it prints the binary representation of d
    # repeatedly


def part1(offset: int) -> int:
    # solve min_a | a + offset = k,
    # where k has binary representation alternating ones
    # and zeros, with the same number of digits as offset
    k = sum(2**i for i in range(offset.bit_length()) if i % 2 == 1)
    return k - offset


def part2(puzzle_input) -> ...:
    ...


def main() -> None:
    # puzzle_input = read_input("2016-25_input.txt")
    offset = 182 * 14
    print("Part 1: ")
    print("-------")
    print(part1(offset))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(offset))
    print("=======\n")


if __name__ == "__main__":
    main()
