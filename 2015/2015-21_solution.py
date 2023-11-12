import math
from collections.abc import Sequence
from dataclasses import dataclass

INPUT = """Hit Points: 109
Damage: 8
Armor: 2
"""

SHOP = """Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage+1    25     1       0
Damage+2    50     2       0
Damage+3   100     3       0
Defense+1   20     0       1
Defense+2   40     0       2
Defense+3   80     0       3
"""


@dataclass
class Item:
    name: str
    cost: int
    damage: int
    armor: int

    @classmethod
    def from_string(cls, string: str) -> "Item":
        name, cost, damage, armor = string.split()
        return cls(name, int(cost), int(damage), int(armor))

    @classmethod
    def null(cls) -> "Item":
        return cls("None", 0, 0, 0)


@dataclass
class Player:
    hp: int
    damage: int
    armor: int
    cost: int = 0

    def attack(self, other: "Player") -> int:
        return max(1, self.damage - other.armor)

    def fight(self, other: "Player") -> bool:
        turns_to_win = math.ceil(other.hp / self.attack(other))
        turns_to_lose = math.ceil(self.hp / other.attack(self))
        return turns_to_win <= turns_to_lose

    @classmethod
    def from_items(cls, items: Sequence[Item], hp: int = 100) -> "Player":
        return cls(
            hp,
            sum(item.damage for item in items),
            sum(item.armor for item in items),
            sum(item.cost for item in items),
        )


def parse_input(
    input: str, shop_str: str
) -> tuple[Player, dict[str, list[Item]]]:
    boss = Player(*(int(line.split(": ")[1]) for line in input.splitlines()))
    shop = {}
    for block in shop_str.split("\n\n"):
        shop_lines = block.splitlines()
        section, title = shop_lines[0].split(": ")
        print(section)
        assert title.strip() == "Cost  Damage  Armor"
        # print(shop_lines)
        shop[section] = [Item.from_string(s) for s in shop_lines[1:]]
    return boss, shop


from itertools import combinations, product


def generate_equipment(shop: dict[str, list[Item]]) -> ...:
    for weapon in shop["Weapons"]:
        for armor in shop["Armor"] + [Item.null()]:
            for ring1, ring2 in combinations(shop["Rings"] + [Item.null()], 2):
                yield weapon, armor, ring1, ring2
            # no rings
            yield weapon, armor


def part1(boss: Player, shop: ...) -> int:
    return min(
        p.cost
        for items in generate_equipment(shop)
        if (p := Player.from_items(items)).fight(boss)
    )


def part2(boss: Player, shop: ...) -> ...:
    return max(
        p.cost
        for items in generate_equipment(shop)
        if not (p := Player.from_items(items)).fight(boss)
    )


def main() -> None:
    boss, shop = parse_input(INPUT, SHOP)
    print("Part 1: ")
    print("-------")
    print(part1(boss, shop))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(boss, shop))
    print("=======\n")


if __name__ == "__main__":
    main()
