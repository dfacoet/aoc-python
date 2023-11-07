INPUT = "hepxcrrq"

FORBIDDEN_CHARS = set(ord(c) - ord("a") for c in "iol")


def increment_char(c: int) -> tuple[chr, bool]:
    match c:
        case 25:
            return 0, True
        case c if c in (7, 10, 13):
            return c + 2, False
        case _:
            return c + 1, False


class Password:
    len = 8
    forbidden = set(ord(c) - ord("a") for c in "iol")

    def __init__(self, s: str) -> None:
        assert len(s) == self.len
        self.chars = [ord(c) - ord("a") for c in s]

    @property
    def s(self) -> str:
        return "".join(chr(c + ord("a")) for c in self.chars)

    @property
    def value(self) -> int:
        return sum(c * 26**i for i, c in enumerate(reversed(self.chars)))

    def increment(self) -> None:
        i = self.len - 1
        carry = True
        while carry:
            self.chars[i], carry = increment_char(self.chars[i])
            i -= 1

    def has_increasing_triple(self) -> bool:
        for i in range(self.len - 2):
            if (
                self.chars[i + 1] == self.chars[i] + 1
                and self.chars[i + 2] == self.chars[i] + 2
            ):
                return True
        return False

    def has_two_pairs(self) -> bool:
        pairs = set()
        for i in range(self.len - 1):
            if self.chars[i] == self.chars[i + 1]:
                pairs.add(self.chars[i])
        return len(pairs) >= 2

    def is_valid(self) -> bool:
        return (
            not self.forbidden.intersection(self.chars)
            and self.has_increasing_triple()
            and self.has_two_pairs()
        )

    def find_next_valid(self) -> None:
        k = 1
        self.increment()
        while not self.is_valid():
            k += 1
            self.increment()


def part1(s: str) -> str:
    password = Password(s)
    password.find_next_valid()
    return password.s


def part2(s: str) -> str:
    password = Password(s)
    password.find_next_valid()
    password.find_next_valid()
    return password.s


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
