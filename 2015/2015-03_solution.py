def read_input(input_file) -> str:
    with open(input_file, "r") as f:
        return f.read()


def visit(input_string) -> set[tuple[int, int]]:
    coordinates = (0, 0)
    visited = [coordinates]
    for c in input_string:
        match c:
            case "^":
                coordinates = (coordinates[0], coordinates[1] + 1)
            case "v":
                coordinates = (coordinates[0], coordinates[1] - 1)
            case ">":
                coordinates = (coordinates[0] + 1, coordinates[1])
            case "<":
                coordinates = (coordinates[0] - 1, coordinates[1])
            case _:
                raise ValueError(f"Invalid character {c}")
        visited.append(coordinates)
    return set(visited)


def part1(input_string: str) -> int:
    return len(visit(input_string))


def part2(input_string: str) -> int:
    santa = visit(input_string[::2])
    robot = visit(input_string[1::2])
    return len(santa | robot)


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
    input_string = read_input("2015-03_input.txt")
    main(input_string)
