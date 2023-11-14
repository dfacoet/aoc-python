Triangle = tuple[int, int, int]


def read_input(input_file) -> list[Triangle]:
    with open(input_file) as f:
        return [tuple(map(int, line.split())) for line in f.readlines()]


def part1(input: list[Triangle]) -> int:
    c = 0
    for t in input:
        longest, *other = sorted(t, reverse=True)
        if longest < sum(other):
            c += 1
    return c


def part2(input: list[Triangle]) -> int:
    actual_triangles = [
        (input[i][c], input[i + 1][c], input[i + 2][c])
        for i in range(0, len(input) - 2, 3)
        for c in range(3)
    ]
    return part1(actual_triangles)


def main() -> None:
    input = read_input("2016-03_input.txt")
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
