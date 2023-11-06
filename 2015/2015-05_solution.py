from collections import Counter


def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.readlines()


FORBIDDEN_SUBSTRINGS = {"ab", "cd", "pq", "xy"}


def is_nice(s: str) -> bool:
    counts = Counter(s)
    n_vowels = sum(counts[vowel] for vowel in "aeiou")
    if n_vowels < 3:
        return False

    consecutive_pairs = set(s[i : i + 2] for i in range(len(s) - 1))

    for p in consecutive_pairs:
        if len(set(p)) == 1:
            break
    else:
        return False

    return consecutive_pairs.isdisjoint(FORBIDDEN_SUBSTRINGS)


def part1(input_strings: list[str]) -> int:
    return sum(is_nice(s) for s in input_strings)


def is_very_nice(s: str) -> bool:
    if len(s) < 4:
        return False

    consecutive_pairs = [s[i : i + 2] for i in range(len(s) - 1)]
    for i, pair in enumerate(consecutive_pairs[:-2]):
        if pair in consecutive_pairs[i + 2 :]:
            break
    else:
        return False

    for i, c in enumerate(s[:-2]):
        if c == s[i + 2]:
            return True
    return False


def part2(input_strings: list[str]) -> int:
    return sum(is_very_nice(s) for s in input_strings)


def main() -> None:
    input_strings = read_input("2015-05_input.txt")
    print("Part 1: ")
    print("-------")
    print(part1(input_strings))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(input_strings))
    print("=======\n")


if __name__ == "__main__":
    main()
