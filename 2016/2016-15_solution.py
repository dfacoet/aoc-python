import math
from dataclasses import dataclass

# find the solution in t to
#  t % k == (initial + delta_t) % k


@dataclass(frozen=True)
class Disc:
    k: int  # number of positions
    i: int  # initial position

    def is_open(self, time: int) -> bool:
        return (self.i + time) % self.k == 0


def read_input(input_file) -> list[Disc]:
    discs = []
    with open(input_file, "r") as f:
        for line in f:
            words = line.split()
            discs.append(Disc(int(words[3]), int(words[-1][:-1])))
    return discs


def product(numbers: list[int]) -> int:
    p = 1
    for n in numbers:
        p *= n
    return p


def part1(discs: tuple[tuple[int, int], ...]) -> int:
    divisors = [disc.k for disc in discs]
    period = math.lcm(*divisors)
    # TODO: make faster using Chinese Remainder Theorem
    # # check that divisors are coprime
    # assert period == product(divisors)

    for t in range(period):
        if all(disc.is_open(t + i + 1) for i, disc in enumerate(discs)):
            return t


def part2(discs: tuple[tuple[int, int], ...]) -> int:
    new_disc = Disc(11, 0)
    # return part1(discs + [new_disc])
    part1_solution = part1(discs)
    period = math.lcm(*[disc.k for disc in discs])
    for i in range(1, 12):
        t = part1_solution + i * period
        if new_disc.is_open(t + len(discs) + 1):
            return t
    raise RuntimeError("No solution found")


def main() -> None:
    discs = read_input("2016-15_input.txt")
    print("Part 1: ")
    print("-------")
    print(part1(discs))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(discs))
    print("=======\n")


if __name__ == "__main__":
    main()
