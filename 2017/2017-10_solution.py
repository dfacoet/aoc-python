import itertools
import operator
from functools import reduce


def read_input(input_file) -> list[int]:
    with open(input_file, "r") as f:
        return [int(n) for n in f.read().split(",")]


class Knot:
    def __init__(self, size: int) -> None:
        self.n = size
        self.knot = list(range(size))

    def reverse(self, start: int, length: int) -> None:
        if length >= self.n:
            # NOTE: length == self.n could be valid but is not used in this puzzle
            raise ValueError("Length cannot be greater than size of knot")
        start %= self.n
        if (stop := start + length) > self.n:
            stop %= self.n
        if start < stop:
            end = start - 1 if start > 0 else None
            self.knot[start:stop] = self.knot[stop - 1 : end : -1]
        elif start > stop:
            reversed = (self.knot[start:] + self.knot[:stop])[::-1]
            self.knot[start:] = reversed[: self.n - start]
            self.knot[:stop] = reversed[self.n - start :]

    def __repr__(self) -> str:
        return f"Knot({self.knot})"

    def dense_hash(self) -> list[int]:
        hash_ints = [
            reduce(operator.xor, self.knot[16 * i : 16 * (i + 1)])
            for i in range(self.n // 16)
        ]
        hash_str = "".join(f"{n:02x}" for n in hash_ints)
        assert len(hash_str) == 32
        return hash_str


def part1(puzzle_input: list[int]) -> int:
    n = 256
    knot = Knot(n)
    i = 0
    s = 0
    for length in puzzle_input:
        knot.reverse(i, length)
        i = i + length + s
        s = s + 1
    return knot.knot[0] * knot.knot[1]


def ascii_lengths(puzzle_input: list[int]) -> list[int]:
    original_input = ",".join(str(n) for n in puzzle_input)
    return [ord(c) for c in original_input] + [17, 31, 73, 47, 23]


def repeated_iterator(iterable, n: int):
    return itertools.chain.from_iterable(itertools.repeat(iterable, n))


def part2(puzzle_input: list[int]) -> int:
    n = 256
    knot = Knot(n)
    s, i = 0, 0
    for length in repeated_iterator(ascii_lengths(puzzle_input), 64):
        knot.reverse(i, length)
        i = i + length + s
        s = s + 1
    return knot.dense_hash()


def main() -> None:
    puzzle_input = read_input("2017-10_input.txt")
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
