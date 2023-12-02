from dataclasses import dataclass


def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


@dataclass
class Draw:
    red: int = 0
    green: int = 0
    blue: int = 0

    def _tuple(self):
        return self.red, self.green, self.blue

    def __le__(self, other):
        return all(a <= b for a, b in zip(self._tuple(), other._tuple()))

    @classmethod
    def from_string(cls, string: str):
        colors = {}
        for color_s in string.split(", "):
            value, color = color_s.split(" ")
            colors[color] = int(value)
        return cls(**colors)

    def power(self):
        return self.red * self.green * self.blue


@dataclass
class Game:
    id: int
    draws: list[Draw]

    def is_possible(self, max_draw: Draw) -> bool:
        return all(draw <= max_draw for draw in self.draws)

    @classmethod
    def from_string(cls, string):
        id_s, game_draws = string.split(": ")
        id = int(id_s.lstrip("Game "))
        draws = [
            Draw.from_string(draw_string)
            for draw_string in game_draws.split("; ")
        ]
        return cls(id, draws)

    def minimal_bag(self) -> Draw:
        return Draw(
            max(draw.red for draw in self.draws),
            max(draw.green for draw in self.draws),
            max(draw.blue for draw in self.draws),
        )


def part1(puzzle_input: list[str]) -> int:
    bag = Draw(12, 13, 14)
    games = [Game.from_string(game_string) for game_string in puzzle_input]
    return sum(game.id for game in games if game.is_possible(bag))


def part2(puzzle_input: list[str]) -> int:
    games = [Game.from_string(game_string) for game_string in puzzle_input]
    return sum(game.minimal_bag().power() for game in games)


def main() -> None:
    puzzle_input = read_input("2023-02_input.txt")
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
