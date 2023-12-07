from collections import Counter


def read_input(input_file) -> list[tuple[str, int]]:
    with open(input_file, "r") as f:
        split_lines = [line.split() for line in f]
    return [(hand, int(bid)) for hand, bid in split_lines]


def sort_key(handbid: tuple[str, int]) -> tuple[list[int], str]:
    hand, _ = handbid
    return (
        sorted(Counter(hand).values(), reverse=True),
        hand.replace("T", "B").replace("K", "X").replace("A", "Z"),
    )


def part1(puzzle_input: list[tuple[str, int]]) -> int:
    return sum(
        (k + 1) * bid
        for k, (_, bid) in enumerate(sorted(puzzle_input, key=sort_key))
    )


def sort_key2(handbid: tuple[str, int]) -> tuple[list[int], str]:
    hand, _ = handbid
    counts = sorted(Counter(hand.replace("J", "")).values(), reverse=True)
    try:
        counts[0] += hand.count("J")
    except IndexError:
        # hand is "JJJJJ"
        counts = [5]
    return (
        counts,
        hand.replace("J", "0")
        .replace("T", "B")
        .replace("K", "X")
        .replace("A", "Z "),
    )


def part2(puzzle_input: list[tuple[str, int]]) -> int:
    return sum(
        (k + 1) * bid
        for k, (_, bid) in enumerate(sorted(puzzle_input, key=sort_key2))
    )


def main() -> None:
    puzzle_input = read_input("2023-07_input.txt")
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
