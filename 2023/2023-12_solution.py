from functools import cache


def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


def parse(s: str, unfold: bool = False) -> tuple[str, tuple[int, ...]]:
    springs, counts_ = s.split()
    counts = tuple(int(c) for c in counts_.split(","))
    if unfold:
        springs = "?".join(springs for _ in range(5))
        counts = counts * 5
    return springs + ".", counts


@cache
def count_arrangements(s: str, counts: tuple[int, ...]) -> int:
    if len(s) == 0:
        return len(counts) == 0
    match s[0]:
        case ".":
            return count_arrangements(s.lstrip("."), counts)
        case "#":
            if len(counts) < 1 or len(s) < counts[0] or "." in s[: counts[0]]:
                # no space for this group
                return 0
            if len(s) == counts[0] or s[counts[0]] == "#":
                # group is too long
                return 0
            return count_arrangements(s[counts[0] + 1 :], counts[1:])
        case "?":
            return count_arrangements(
                "." + s[1:], counts
            ) + count_arrangements("#" + s[1:], counts)
        case _:
            raise ValueError("Invalid character in input string")


def part1(puzzle_input: list[str]) -> int:
    return sum(count_arrangements(*parse(s)) for s in puzzle_input)


def part2(puzzle_input: list[str]) -> int:
    return sum(
        count_arrangements(*parse(s, unfold=True)) for s in puzzle_input
    )


def main() -> None:
    puzzle_input = read_input("2023-12_input.txt")
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
