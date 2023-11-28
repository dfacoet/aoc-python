from collections.abc import Iterator

import tqdm


def read_input(input_file) -> dict[str, int]:
    with open(input_file, "r") as f:
        return {line.split()[1]: int(line.split()[-1]) for line in f}


def modular_geometric_generator(
    start: int, base: int, modulus: int, multiple_only: int | None = None
) -> Iterator[int]:
    while True:
        start = (start * base) % modulus
        if multiple_only is None or start % multiple_only == 0:
            yield start


def part1(puzzle_input: dict[str, int]) -> int:
    a = puzzle_input["A"]
    b = puzzle_input["B"]
    c = 2147483647  # 2**31 - 1 (prime)
    a_base = 16807  # 7 ** 5
    b_base = 48271  # prime

    # TODO: can we do something smart with modular arithmetic?
    # we are counting the solutions to
    # (a_base ** n * a) == (b_base ** n * b) (mod c) (mod 2**16)

    a_gen = modular_geometric_generator(a, a_base, c)
    b_gen = modular_geometric_generator(b, b_base, c)
    count = 0
    for _ in tqdm.trange(40_000_000):
        a = next(a_gen)
        b = next(b_gen)
        if a % 65536 == b % 65536:
            count += 1
    return count


def part2(puzzle_input: dict[str, int]) -> int:
    a = puzzle_input["A"]
    b = puzzle_input["B"]
    c = 2147483647  # 2**31 - 1 (prime)
    a_base = 16807  # 7 ** 5
    b_base = 48271  # prime

    a_gen = modular_geometric_generator(a, a_base, c, 4)
    b_gen = modular_geometric_generator(b, b_base, c, 8)
    count = 0
    for _ in tqdm.trange(5_000_000):
        a = next(a_gen)
        b = next(b_gen)
        if a % 65536 == b % 65536:
            count += 1
    return count


def main() -> None:
    puzzle_input = read_input("2017-15_input.txt")
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
