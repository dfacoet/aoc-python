from collections.abc import Iterator


def read_input(input_file) -> list[list[str]]:
    with open(input_file, "r") as f:
        return [b.splitlines() for b in f.read().split("\n\n")]


def is_reflection(s: str, i: int) -> bool:
    return all(a == b for a, b in zip(s[:i][::-1], s[i:]))


def find_reflections(pattern: list[str]):
    for i in range(1, len(pattern[0])):
        if all(is_reflection(row, i) for row in pattern):
            yield i
    cols = ["".join(row[i] for row in pattern) for i in range(len(pattern[0]))]
    for i in range(1, len(pattern)):
        if all(is_reflection(col, i) for col in cols):
            yield i * 100


def evaluate_reflections(pattern: list[str]):
    reflections = list(find_reflections(pattern))
    assert len(reflections) == 1
    return reflections[0]


def part1(puzzle_input: list[list[str]]) -> int:
    return sum(evaluate_reflections(pattern) for pattern in puzzle_input)


def _replace(c: str) -> str:
    match c:
        case "#":
            return "."
        case ".":
            return "#"
        case _:
            raise ValueError(f"Unknown character {c}")


def substitutions(pattern: list[str]) -> Iterator[list[str]]:
    for i, row in enumerate(pattern):
        for j, c in enumerate(row):
            yield pattern[:i] + [
                row[:j] + _replace(c) + row[j + 1 :]
            ] + pattern[i + 1 :]


def evaluate_new_reflections(pattern: list[str]) -> int:
    old_reflection = evaluate_reflections(pattern)
    new_reflections = {
        r
        for substitution in substitutions(pattern)
        for r in find_reflections(substitution)
        if r != old_reflection
    }
    assert len(new_reflections) == 1
    return new_reflections.pop()


def part2(puzzle_input: list[list[str]]) -> int:
    return sum(evaluate_new_reflections(pattern) for pattern in puzzle_input)


def main() -> None:
    puzzle_input = read_input("2023-13_input.txt")
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
