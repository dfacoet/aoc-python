def read_input(input_file) -> str:
    with open(input_file, "r") as f:
        return f.read().strip()


def decode(row: str) -> list[bool]:
    assert set(row) == set(".^")
    # True if safe, False if trap
    return [c == "." for c in row]


def encode(tiles: list[bool]) -> str:
    return "".join("." if tile else "^" for tile in tiles)


def next_row(row: list[bool]) -> list[bool]:
    return [l == r for l, r in zip([True] + row, row[1:] + [True])]


def print_rows(starting: str, n: int) -> None:
    print(starting)
    row = decode(starting)
    for _ in range(n - 1):
        row = next_row(row)
        print(encode(row))


def part1(puzzle_input: str, rows: int = 40) -> int:
    row_tiles = decode(puzzle_input)
    safe_tiles = sum(row_tiles)
    for _ in range(rows - 1):
        row_tiles = next_row(row_tiles)
        safe_tiles += sum(row_tiles)
    return safe_tiles


def part2(puzzle_input: str) -> int:
    # TODO: find period and skip ahead
    return part1(puzzle_input, 400000)


def main() -> None:
    puzzle_input = read_input("2016-18_input.txt")
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
