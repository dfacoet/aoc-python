from collections import Counter


def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


def is_valid(passphrase: str) -> bool:
    words = passphrase.split()
    return len(words) == len(set(words))


def part1(puzzle_input: list[str]) -> int:
    return sum(is_valid(passphrase) for passphrase in puzzle_input)


def is_valid2(passphrase: str) -> bool:
    words = passphrase.split()
    return len(words) == len(
        set(frozenset(Counter(word).items()) for word in words)
    )


def part2(puzzle_input: list[str]) -> int:
    return sum(is_valid2(passphrase) for passphrase in puzzle_input)


def main() -> None:
    puzzle_input = read_input("2017-04_input.txt")
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
