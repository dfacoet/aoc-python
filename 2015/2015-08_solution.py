import ast


def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return [line.strip() for line in f.readlines()]


def part1(strings: list[str]) -> int:
    return sum(len(s) - len(ast.literal_eval(s)) for s in strings)


def part2(strings: list[str]) -> int:
    return sum(2 + s.count('"') + s.count("\\") for s in strings)


def main() -> None:
    strings = read_input("2015-08_input.txt")
    print("Part 1: ")
    print("-------")
    print(part1(strings))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(strings))
    print("=======\n")


if __name__ == "__main__":
    main()
