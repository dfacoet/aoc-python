from dataclasses import dataclass


def read_input(input_file) -> list[str]:
    with open(input_file) as f:
        return f.readlines()


class Coordinate(int):
    def __add__(self, other):
        return Coordinate(max(min(int(self) + other, 2), 0))


@dataclass
class Key:
    x: Coordinate
    y: Coordinate

    @property
    def digit(self) -> int:
        return int(self.y) * 3 + int(self.x) + 1

    @classmethod
    def from_digit(cls, digit: int) -> "Key":
        x = Coordinate((digit - 1) % 3)
        y = Coordinate((digit - 1) // 3)
        return cls(x, y)

    def move(self, move: str):
        if move == "U":
            self.y += -1
        elif move == "D":
            self.y += 1
        elif move == "L":
            self.x += -1
        elif move == "R":
            self.x += 1


def digit_to_coord(digit: int) -> tuple[int, int]:
    return (digit - 1) % 3, (digit - 1) // 3


def coord_to_digit(x: int, y: int) -> int:
    return y * 3 + x + 1


def part1(input: list[str]) -> int:
    digits = []
    key = Key.from_digit(5)
    for line in input:
        for c in line:
            key.move(c)
        digits.append(key.digit)
    return "".join(str(d) for d in digits)


@dataclass
class KeyNode:
    digit: str
    neighbours: dict[str, str]


@dataclass
class Keypad:
    keys: dict[str, KeyNode]
    current: str

    def move(self, c: str) -> None:
        try:
            self.current = self.keys[self.current].neighbours[c]
        except KeyError:
            pass


def part2(input: list[str]) -> str:
    digits = []
    keys = {
        "1": KeyNode("1", {"D": "3"}),
        "2": KeyNode("2", {"R": "3", "D": "6"}),
        "3": KeyNode("3", {"U": "1", "R": "4", "D": "7", "L": "2"}),
        "4": KeyNode("4", {"L": "3", "D": "8"}),
        "5": KeyNode("5", {"R": "6"}),
        "6": KeyNode("6", {"U": "2", "R": "7", "D": "A", "L": "5"}),
        "7": KeyNode("7", {"U": "3", "R": "8", "D": "B", "L": "6"}),
        "8": KeyNode("8", {"U": "4", "R": "9", "D": "C", "L": "7"}),
        "9": KeyNode("9", {"L": "8"}),
        "A": KeyNode("A", {"U": "6", "R": "B"}),
        "B": KeyNode("B", {"U": "7", "R": "C", "D": "D", "L": "A"}),
        "C": KeyNode("C", {"U": "8", "L": "B"}),
        "D": KeyNode("D", {"U": "B"}),
    }
    keypad = Keypad(keys, "5")
    for line in input:
        for c in line:
            keypad.move(c)
        digits.append(keypad.current)
    return "".join(digits)


def main() -> None:
    input = read_input("2016-02_input.txt")
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
