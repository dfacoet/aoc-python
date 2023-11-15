def read_input(input_file) -> str:
    with open(input_file) as f:
        return f.read()


def part1(input: str) -> int:
    i = 0
    total_length = 0
    while i < len(input):
        if input[i] == "(":
            end = input.find(")", i)
            length, times = (int(s) for s in input[i + 1 : end].split("x"))
            total_length += length * times
            i = end + length + 1
        else:
            total_length += 1
            i += 1
    return total_length


def part2(input: str) -> ...:
    i = 0
    total_length = 0
    while i < len(input):
        if input[i] == "(":
            end = input.find(")", i)
            length, times = (int(s) for s in input[i + 1 : end].split("x"))
            total_length += part2(input[end + 1 : end + length + 1]) * times
            i = end + length + 1
        else:
            total_length += 1
            i += 1
    return total_length


def main() -> None:
    input = read_input("2016-09_input.txt")
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
