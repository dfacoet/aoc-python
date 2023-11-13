import math
from copy import deepcopy
from dataclasses import dataclass, field

INPUT = """Hit Points: 71
Damage: 10
"""


@dataclass
class Boss:
    hp: int = 71
    damage: int = 10


class SpellNotAllowed(Exception):
    pass


class NotEnoughMana(SpellNotAllowed):
    pass


class EffectAlreadyActive(SpellNotAllowed):
    pass


class Dead(SpellNotAllowed):
    pass


class Win(Exception):
    pass


@dataclass
class Wizard:
    boss: Boss = field(default_factory=Boss)
    hp: int = 50
    mana: int = 500
    hard: bool = False
    _turns: dict[str, int] = field(
        default_factory=lambda: dict.fromkeys(
            ["Shield", "Poison", "Recharge"], 0
        )
    )
    _mana_spent: int = 0
    _history: list[str] = field(default_factory=list)

    spells = {  # name: costs
        "Missile": 53,
        "Drain": 73,
        "Shield": 113,
        "Poison": 173,
        "Recharge": 229,
    }

    effect_duration = {  # name: turns
        "Shield": 6,
        "Poison": 6,
        "Recharge": 5,
    }

    @property
    def armor(self) -> int:
        return 7 if self._turns["Shield"] else 0

    def _apply_effects(self) -> None:
        if self._turns["Poison"]:
            self.boss.hp -= 3
        if self._turns["Recharge"]:
            self.mana += 101
        for effect, turns_left in self._turns.items():
            if turns_left:
                self._turns[effect] -= 1

    def turn(self, spell: str) -> None:
        # player turn
        if self.hard:
            self.hp -= 1
        if self.hp <= 0:
            raise Dead

        self._apply_effects()

        if self.spells[spell] > self.mana:
            raise NotEnoughMana
        match spell:
            case "Missile":
                self.boss.hp -= 4
            case "Drain":
                self.boss.hp -= 2
                self.hp += 2
            case effect if effect in ["Shield", "Poison", "Recharge"]:
                if self._turns[effect]:
                    raise EffectAlreadyActive
                self._turns[effect] = self.effect_duration[effect]
        self.mana -= self.spells[spell]
        self._mana_spent += self.spells[spell]
        self._history.append(spell)

        # boss turn
        self._apply_effects()

        if self.boss.hp <= 0:
            raise Win

        self.hp -= max(1, self.boss.damage - self.armor)
        if self.hp <= 0:
            raise Dead

    def turn_copy(self, spell) -> "Wizard":
        w = deepcopy(self)
        w.turn(spell)
        return w


def part1() -> int:
    min_mana_winner = math.inf
    w = Wizard()
    games = [w]
    n_leaves = 0
    n_wins = 0
    while games:
        w = games.pop()
        for spell in w.spells:
            try:
                next = deepcopy(w)
                next.turn(spell)
            except SpellNotAllowed:
                n_leaves += 1
            except Win:
                n_wins += 1
                min_mana_winner = min(min_mana_winner, next._mana_spent)
            else:
                if next._mana_spent < min_mana_winner:
                    games.append(next)
    return min_mana_winner


def part2() -> int:
    min_mana_winner = math.inf
    w = Wizard(hard=True)
    games = [w]
    n_leaves = 0
    n_wins = 0
    while games:
        w = games.pop()
        for spell in w.spells:
            try:
                next = deepcopy(w)
                next.turn(spell)
            except SpellNotAllowed:
                n_leaves += 1
            except Win:
                n_wins += 1
                min_mana_winner = min(min_mana_winner, next._mana_spent)
            else:
                if next._mana_spent < min_mana_winner:
                    games.append(next)
    return min_mana_winner


def main() -> None:
    print("Part 1: ")
    print("-------")
    print(part1())
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2())
    print("=======\n")


if __name__ == "__main__":
    main()
