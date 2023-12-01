def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


def calibration_value(s: str) -> int:
    digits = [d for d in s if d.isdigit()]
    return int(f"{digits[0]}{digits[-1]}")


def part1(puzzle_input: list[str]) -> int:
    return sum(calibration_value(s) for s in puzzle_input)


spelled_digits = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def letters_to_digits(s: str) -> str:
    digits_string = ""
    i = 0
    while i < len(s):
        for n, d in enumerate(spelled_digits):
            if s[i:].startswith(d):
                print(
                    f"Found {d}, replacing with {n + 1} and skipping {len(d)}"
                )
                digits_string += str(n + 1)
                break
        else:
            digits_string += s[i]
        i += 1
    return digits_string


def part2(puzzle_input: list[str]) -> int:
    return sum(calibration_value(letters_to_digits(s)) for s in puzzle_input)


def main() -> None:
    puzzle_input = read_input("2023-01_input.txt")

    print("TEST")
    for s in puzzle_input:
        print(
            f"{s} -> {letters_to_digits(s)} -> {calibration_value(letters_to_digits(s))}"
        )

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
