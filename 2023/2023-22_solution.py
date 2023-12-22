from collections.abc import Iterator
from dataclasses import dataclass


def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


@dataclass
class Brick:
    id: int
    pos: dict[str, int]  # x, y, z -> vector
    orientation: str  # x, y, or z
    length: int

    def down(self) -> None:
        if self.pos["z"] == 1:
            raise ValueError("Brick is on the ground")
        self.pos["z"] -= 1

    def cells(self) -> Iterator[tuple[int, int, int]]:
        for i in range(self.length):
            yield tuple(  # type: ignore[misc]
                (
                    self.pos
                    | {self.orientation: self.pos[self.orientation] + i}
                ).values()
            )

    def supported(
        self, floor: dict[tuple[int, int], tuple[int, int]]
    ) -> set[int]:
        return {
            floor[(x, y)][1]
            for x, y, z in self.cells()
            if (x, y) in floor and z == floor[(x, y)][0] + 1
        }

    @classmethod
    def from_string(cls, id: int, string: str) -> "Brick":
        assert id > 0
        a, b = string.split("~")
        pos = {}
        orientation = "x"
        length = 1
        for ca, cb, d in zip(
            map(int, a.split(",")), map(int, b.split(",")), "xyz"
        ):
            if ca == cb:
                pos[d] = ca
            else:
                pos[d] = min(ca, cb)
                orientation = d
                length = abs(ca - cb) + 1
        return cls(id, pos, orientation, length)


def parse(puzzle_input: list[str]) -> list[Brick]:
    return [Brick.from_string(i + 1, s) for i, s in enumerate(puzzle_input)]


def settle(bricks: list[Brick]) -> dict[int, set[int]]:
    cells = {c for b in bricks for c in b.cells()}
    # (x, y) -> (z, id)
    floor = dict.fromkeys(((x, y) for x, y, _ in cells), (0, 0))
    supported_by = {}
    for brick in sorted(bricks, key=lambda b: b.pos["z"]):
        while not (supporters := brick.supported(floor)):
            brick.down()
        supported_by[brick.id] = supporters
        for x, y, z in brick.cells():
            floor[(x, y)] = (z, brick.id)
    return supported_by


def part1(puzzle_input: list[str]) -> int:
    bricks = parse(puzzle_input)
    supported_by = settle(bricks)
    safe_to_remove = {b.id for b in bricks}
    for supporters in supported_by.values():
        if len(supporters) == 1:
            safe_to_remove -= supporters
    return len(safe_to_remove)


def invert_tree(tree: dict[int, set[int]]) -> dict[int, set[int]]:
    inverted: dict[int, set[int]] = {k: set() for k in tree}
    for supported, supporters in tree.items():
        for supporter in supporters - {0}:
            inverted[supporter].add(supported)
    return inverted


def remove(id: int, supported_by: dict[int, set[int]]) -> int:
    supported_by = {k: v.copy() for k, v in supported_by.items()}
    support_tree = invert_tree(supported_by)
    to_remove = {id}
    while to_remove:
        removed = to_remove.pop()
        for supported in support_tree[removed]:
            supported_by[supported] -= {removed}
            if not supported_by[supported]:
                to_remove.add(supported)
    return sum(len(s) == 0 for s in supported_by.values())


def part2(puzzle_input: list[str]) -> int:
    bricks = parse(puzzle_input)
    supported_by = settle(bricks)
    return sum(remove(id, supported_by) for id in range(1, len(bricks) + 1))


def main() -> None:
    puzzle_input = read_input("2023-22_input.txt")
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
