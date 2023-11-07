INPUT = "1113122113"


def look_and_say(s: str) -> str:
    k = 0
    new_string = ""
    while k < len(s):
        c = 1
        while k + c < len(s) and s[k + c] == s[k]:
            c += 1
        new_string += str(c) + s[k]
        k += c
    return new_string


def part1(s: str) -> int:
    for _ in range(40):
        s = look_and_say(s)
    return len(s)


def part2(s: str) -> int:
    for _ in range(50):
        s = look_and_say(s)
    return len(s)


def main() -> None:
    print("Part 1: ")
    print("-------")
    print(part1(INPUT))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(INPUT))
    print("=======\n")


if __name__ == "__main__":
    main()
