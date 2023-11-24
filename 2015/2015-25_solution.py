INPUT = (
    "To continue, please consult the code grid in the manual."
    " Enter the code at row 3010, column 3019."
)


def read_input(input_string) -> tuple[int, int]:
    i = input_string.split()
    return int(i[-3].strip(",.")), int(i[-1].strip(",."))


def find_code_id(row: int, col: int) -> int:
    return (row + col - 1) * (row + col - 2) // 2 + col


def generate_code(code: int, n: int) -> int:
    for _ in range(n - 1):
        code = code * 252533 % 33554393
    return code


def part1(row: int, col: int) -> int:
    id = find_code_id(row, col)
    initial_code = 20151125
    code = generate_code(initial_code, id)
    return code


def part2(row: int, col: int) -> int:
    ...


def main() -> None:
    row, col = read_input(INPUT)
    print("Part 1: ")
    print("-------")
    print(part1(row, col))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(row, col))
    print("=======\n")


if __name__ == "__main__":
    main()
