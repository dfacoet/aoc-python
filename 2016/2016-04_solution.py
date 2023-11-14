from collections import Counter
from dataclasses import dataclass


def read_input(input_file) -> list[str]:
    with open(input_file) as f:
        return f.readlines()


def calculate_checksum(name: str) -> str:
    counter = Counter(name.replace("-", ""))
    ranked_letters = [
        letter
        for letter, _ in sorted(counter.items(), key=lambda x: (-x[1], x[0]))
    ]
    return "".join(ranked_letters[:5])


@dataclass
class Room:
    name: str
    id: int
    checksum: str

    @classmethod
    def from_string(cls, string: str) -> "Room":
        name, id_checksum = string.rsplit("-", 1)
        id, checksum = id_checksum.split("[")
        return cls(name, int(id), checksum[:-2])

    def validate(self) -> bool:
        return self.checksum == calculate_checksum(self.name)

    def decript(self) -> str:
        decripted = ""
        for c in self.name:
            if c == "-":
                decripted += " "
            else:
                # ord('a') == 97
                decripted += chr((ord(c) - 97 + self.id) % 26 + 97)
        return decripted


def part1(input: list[str]) -> int:
    total = 0
    for line in input:
        room = Room.from_string(line)
        if room.validate():
            total += room.id
    return total


def part2(input: list[str]) -> int:
    rooms = [Room.from_string(line) for line in input]
    [room] = [r for r in rooms if r.validate() and "north" in r.decript()]
    return room.id


def main() -> None:
    input = read_input("2016-04_input.txt")
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
