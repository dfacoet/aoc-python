def read_input(input_file) -> str:
    with open(input_file, "r") as f:
        return f.read()


def remove_canceled(s: str) -> str:
    i = 0
    chars = list(s)
    while i < len(chars):
        if chars[i] == "!":
            chars.pop(i)
            chars.pop(i)
        else:
            i += 1
    return "".join(chars)


def remove_garbage(s: str) -> str:
    stream = ""
    i = 0
    while i < len(s):
        if s[i] == "<":
            while s[i] != ">":
                i += 1
        else:
            stream += s[i]
        i += 1
    return stream.replace(",", "")


def score(stream: str) -> int:
    total = 0
    level = 0
    for c in stream:
        if c == "{":
            level += 1
        elif c == "}":
            total += level
            level -= 1
        else:
            raise ValueError(f"Invalid character: {c}")
    return total


def part1(puzzle_input: str) -> int:
    clean_stream = remove_garbage(remove_canceled(puzzle_input))
    assert (
        clean_stream.count("{")
        == clean_stream.count("}")
        == len(clean_stream) // 2
    )
    return score(clean_stream)


def count_garbage(s: str) -> str:
    count = 0
    i = 0
    while i < len(s):
        if s[i] == "<":
            i += 1
            while s[i] != ">":
                count += 1
                i += 1
        i += 1
    return count


def part2(puzzle_input: str) -> int:
    return count_garbage(remove_canceled(puzzle_input))


def main() -> None:
    puzzle_input = read_input("2017-09_input.txt")
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
