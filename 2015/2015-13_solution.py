from dataclasses import dataclass, field
from itertools import permutations


class Table(list[str]):
    def __getitem__(self, idx: int) -> str:
        return super().__getitem__(idx % len(self))


@dataclass
class Party:
    guests: set[str] = field(default_factory=set)
    happiness: dict[str, dict[str, int]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        assert set(self.happiness) == self.guests
        for guest, values in self.happiness.items():
            assert set(values).union({guest}) == self.guests
            assert guest not in values

    def evaluate_table(self, table: Table) -> int:
        assert set(table) == self.guests
        happiness = 0
        for i, guest in enumerate(table):
            happiness += self.happiness[guest][table[i - 1]]
            happiness += self.happiness[guest][table[i + 1]]
        return happiness

    def find_max_happiness(self) -> int:
        fixed, *rotating = self.guests
        tables = (Table([fixed] + list(p)) for p in permutations(rotating))
        return max(self.evaluate_table(t) for t in tables)

    def evaluate_list(self, guests: list[str]) -> int:
        assert set(guests) == self.guests
        happiness = 0
        for i, guest in enumerate(guests):
            if i > 0:
                happiness += self.happiness[guest][guests[i - 1]]
            if i < len(guests) - 1:
                happiness += self.happiness[guest][guests[i + 1]]
        return happiness

    def find_max_happiness2(self) -> int:
        return max(
            self.evaluate_list(list(p)) for p in permutations(self.guests)
        )


def parse_line(line: str) -> tuple[str, str, int]:
    line = line.strip().rstrip(".").split()
    sign = 1 if line[2] == "gain" else -1
    return line[0], line[-1], sign * int(line[3])


def read_input(input_file: str) -> Party:
    with open(input_file, "r") as f:
        lines = [parse_line(line) for line in f.readlines()]
    guests = set(guest for guest, _, _ in lines)
    happiness = {
        guest: {other: None for other in guests if other != guest}
        for guest in guests
    }
    for guest, other, value in lines:
        happiness[guest][other] = value
    party = Party(guests, happiness)
    return party


def part1(party: Party) -> int:
    return party.find_max_happiness()


def part2(party: Party) -> ...:
    return party.find_max_happiness2()


def main() -> None:
    party = read_input("2015-13_input.txt")
    print("Part 1: ")
    print("-------")
    print(part1(party))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(party))
    print("=======\n")


if __name__ == "__main__":
    main()
