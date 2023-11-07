import json


def read_input(input_file) -> str:
    with open(input_file, "r") as f:
        return json.load(f)


def evaluate(obj) -> int:
    match obj:
        case int():
            return obj
        case list():
            return sum(evaluate(item) for item in obj)
        case dict():
            return sum(
                evaluate(key) + evaluate(value) for key, value in obj.items()
            )
        case str():
            return 0


def part1(input: dict) -> int:
    return evaluate(input)


def evaluate_red(obj) -> int:
    match obj:
        case int():
            return obj
        case list():
            return sum(evaluate_red(item) for item in obj)
        case dict():
            if "red" in obj.values() or "red" in obj.keys():
                return 0
            return sum(
                evaluate_red(key) + evaluate_red(value)
                for key, value in obj.items()
            )
        case str():
            return 0


def part2(input: str) -> int:
    return evaluate_red(input)


def main() -> None:
    input = read_input("2015-12_input.txt")
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
