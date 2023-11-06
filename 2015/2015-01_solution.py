from collections import Counter


def read_input(input_file) -> str:
    with open(input_file, "r") as f:
        return f.read()


def part1(input_string: str) -> int:
    counts = Counter(input_string)
    return counts["("] - counts[")"]


def part2(input_string: str) -> int:
    level = 0
    for i, c in enumerate(input_string):
        match c:
            case "(":
                level += 1
            case ")":
                level -= 1
            case _:
                raise ValueError
        if level < 0:
            return i + 1


def main(input_string: str) -> None:
    print("Part 1: ")
    print("-------")
    print(part1(input_string))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(input_string))
    print("=======\n")


if __name__ == "__main__":
    input_string = read_input("input.txt")
    main(input_string)
