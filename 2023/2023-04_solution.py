def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


def count_winning(string: str) -> int:
    _, all_numbers = string.split(": ")
    winning_s, numbers_s = all_numbers.split(" | ")
    winning = {int(i) for i in winning_s.split()}
    numbers = {int(i) for i in numbers_s.split()}
    return len(winning.intersection(numbers))


def points(n: int) -> int:
    if n == 0:
        return 0
    return 2 ** (n - 1)


def part1(puzzle_input: list[str]) -> int:
    return sum(points(count_winning(s)) for s in puzzle_input)


def part2(puzzle_input: list[str]) -> int:
    wins = [count_winning(s) for s in puzzle_input]
    n_cards = [1 for _ in puzzle_input]
    for i, n in enumerate(wins):
        for j in range(i + 1, i + n + 1):
            n_cards[j] += n_cards[i]
    return sum(n_cards)


def main() -> None:
    puzzle_input = read_input("2023-04_input.txt")
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
