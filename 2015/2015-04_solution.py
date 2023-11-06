import hashlib


def read_input(input_file) -> str:
    with open(input_file, "r") as f:
        return f.read()


def check_hash(n: int, input_string: str, starts_with: str = "00000") -> bool:
    return (
        hashlib.md5(f"{input_string}{n}".encode())
        .hexdigest()
        .startswith(starts_with)
    )


def part1(input_string: str) -> int:
    n = 1
    while not check_hash(n, input_string):
        n += 1
    return n


def part2(input_string: str) -> int:
    n = 1
    while not check_hash(n, input_string, "000000"):
        n += 1
    return n


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
    input_string = read_input("2015-04_input.txt")
    main(input_string)
