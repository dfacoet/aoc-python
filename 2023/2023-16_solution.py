from dataclasses import dataclass


def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


@dataclass
class Beam:
    position: tuple[int, int]
    direction: int  # 0 = right, 1 = down, 2 = left, 3 = up

    def turn_right(self) -> None:
        self.direction = (self.direction + 1) % 4

    def turn_left(self) -> None:
        self.direction = (self.direction - 1) % 4

    def is_horizontal(self) -> bool:
        return self.direction % 2 == 0

    def slash(self) -> None:
        if self.is_horizontal():
            self.turn_left()
        else:
            self.turn_right()

    def backslash(self) -> None:
        if self.is_horizontal():
            self.turn_right()
        else:
            self.turn_left()

    def move(self) -> None:
        if self.direction == 0:
            self.position = (self.position[0], self.position[1] + 1)
        elif self.direction == 1:
            self.position = (self.position[0] + 1, self.position[1])
        elif self.direction == 2:
            self.position = (self.position[0], self.position[1] - 1)
        elif self.direction == 3:
            self.position = (self.position[0] - 1, self.position[1])


@dataclass(frozen=True)
class Cave:
    tiles: list[str]

    @property
    def shape(self) -> tuple[int, int]:
        return (len(self.tiles[0]), len(self.tiles))

    def in_grid(self, position: tuple[int, int]) -> bool:
        return (
            0 <= position[0] < self.shape[0]
            and 0 <= position[1] < self.shape[1]
        )

    def init_beam(self) -> Beam:
        position = (0, 0)
        match self.tiles[0][0]:
            case "-" | ".":
                direction = 0
            case "|" | "\\":
                direction = 1
            case "/":
                raise ValueError("The beam leaves the grid immediately")
            case other:
                raise ValueError(f"Invalid starting tile: {other}")
        return Beam(position, direction)

    def on(self, init: Beam | None = None) -> int:
        if init is None:
            init = Beam((0, -1), 0)
        beams = [init]
        energized = set()
        seen = set()
        while beams:
            beam = beams.pop()
            if str(beam) in seen:
                continue
            seen.add(str(beam))
            while True:
                energized.add(beam.position)
                beam.move()
                if not self.in_grid(beam.position):
                    break
                match self.tiles[beam.position[0]][beam.position[1]]:
                    case "\\":
                        beam.backslash()
                    case "/":
                        beam.slash()
                    case "-" if not beam.is_horizontal():
                        beams.append(Beam(beam.position, 0))
                        beams.append(Beam(beam.position, 2))
                        break
                    case "|" if beam.is_horizontal():
                        beams.append(Beam(beam.position, 1))
                        beams.append(Beam(beam.position, 3))
                        break
                    case other:
                        assert other in ".|-"
        # Don't count the starting (out of bounds) position
        return len(energized) - 1

    def init_beams(self):
        for i in range(self.shape[0]):
            yield Beam((i, -1), 0)
            yield Beam((i, self.shape[1]), 2)
        for i in range(self.shape[1]):
            yield Beam((-1, i), 1)
            yield Beam((self.shape[0], i), 3)

    def max_energized(self) -> int:
        return max(self.on(beam) for beam in self.init_beams())


def part1(puzzle_input: list[str]) -> int:
    cave = Cave(puzzle_input)
    return cave.on()
    return cave.count_energized()


def part2(puzzle_input: list[str]) -> int:
    cave = Cave(puzzle_input)
    return cave.max_energized()


def main() -> None:
    puzzle_input = read_input("2023-16_input.txt")
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
