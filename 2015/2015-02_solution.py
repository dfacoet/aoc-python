Input = list[tuple[int, int, int]]


def read_input(input_file) -> Input:
    with open(input_file, "r") as f:
        lines = f.readlines()
    return [tuple(map(int, line.split("x"))) for line in lines]


def paper_area(d1: int, d2: int, d3: int) -> int:
    faces = [d1 * d2, d2 * d3, d3 * d1]
    return 2 * sum(faces) + min(faces)


def part1(dimensions: Input) -> int:
    return sum(paper_area(*box_dim) for box_dim in dimensions)


def min_perimeter(d1: int, d2: int, d3: int) -> int:
    return 2 * (d1 + d2 + d3 - max(d1, d2, d3))


def volume(d1: int, d2: int, d3: int) -> int:
    return d1 * d2 * d3


def part2(dimensions: Input) -> int:
    return sum(
        min_perimeter(*box_dim) + volume(*box_dim) for box_dim in dimensions
    )


def main() -> None:
    dimensions = read_input("2015-02_input.txt")
    print("Part 1: ")
    print("-------")
    print(part1(dimensions))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(dimensions))
    print("=======\n")


if __name__ == "__main__":
    main()
