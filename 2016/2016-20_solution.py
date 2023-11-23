from typing import Literal


def read_input(input_file) -> dict[Literal["left", "right"], list[int]]:
    endpoints = {"left": [], "right": []}
    with open(input_file, "r") as f:
        for line in f:
            left, right = line.strip().split("-")
            endpoints["left"].append(int(left))
            endpoints["right"].append(int(right))
    return endpoints


def part1(puzzle_input: dict[Literal["left", "right"], list[int]]) -> int:
    endpoints = sorted(
        [(v, -1) for v in puzzle_input["left"]]
        + [(v, 1) for v in puzzle_input["right"]]
    )
    level = 0
    for k, (v, change) in enumerate(endpoints):
        level += change
        if level == 0:
            if k >= len(endpoints) or endpoints[k + 1][0] > v + 1:
                # last endpoint, or there's a gap
                return v + 1

    raise RuntimeError("No solution found")


def part2(puzzle_input: dict[Literal["left", "right"], list[int]]) -> int:
    endpoints = sorted(
        [(v, -1) for v in puzzle_input["left"]]
        + [(v, 1) for v in puzzle_input["right"]]
    )
    level = 0
    total = 0
    for k, (v, change) in enumerate(endpoints):
        level += change
        if level == 0:
            if k == len(endpoints) - 1:
                # last interval
                total += 2**32 - v - 1
            elif (gap := endpoints[k + 1][0] - v - 1) > 0:
                total += gap
    return total


# 448 TOO HIGH


def main() -> None:
    puzzle_input = read_input("2016-20_input.txt")
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
