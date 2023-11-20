import math


def highest_power(n: int, base: int = 2) -> int:
    """Return the highest power of base <= n."""
    math.log(n, base)
    return base ** (int(math.floor(math.log(n, base))))


def part1(puzzle_input: int) -> int:
    return 2 * (puzzle_input % highest_power(puzzle_input)) + 1


def part2(puzzle_input: int) -> int:
    p = highest_power(puzzle_input, 3)
    r = puzzle_input % p
    if r == 0:
        return puzzle_input
    if r < p:
        return r
    return r + 2 * p


def main() -> None:
    puzzle_input = 3012210
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
