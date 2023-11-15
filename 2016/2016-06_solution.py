def read_input(input_file) -> list[str]:
    with open(input_file) as f:
        return f.readlines()


def part1(input: list[str]) -> ...:
    ...


def part2(input: list[str]) -> ...:
    ...


def main() -> None:
    input = read_input("2016-05_input.txt")
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
