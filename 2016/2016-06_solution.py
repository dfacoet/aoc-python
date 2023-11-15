from collections import Counter


def read_input(input_file) -> list[str]:
    with open(input_file) as f:
        return f.read().splitlines()


def part1(input: list[str]) -> str:
    n_col = len(input[0])
    assert all(len(line) == n_col for line in input)
    message = ""
    for col in range(n_col):
        counter = Counter(line[col] for line in input)
        message += counter.most_common(1)[0][0]
    return message


def part2(input: list[str]) -> str:
    n_col = len(input[0])
    assert all(len(line) == n_col for line in input)
    message = ""
    for col in range(n_col):
        counter = Counter(line[col] for line in input)
        message += counter.most_common()[-1][0]
    return message


def main() -> None:
    input = read_input("2016-06_input.txt")
    print("Part 1: ")
    print("-------")
    print(part1(input))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(input))
    print("=======\n")


if __name__ == "__main__":
    main()
