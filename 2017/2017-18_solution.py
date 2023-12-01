from collections import defaultdict
from dataclasses import dataclass


def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


class Registers(dict):
    def __missing__(self, key):
        match key:
            case str() if len(key) == 1 and key.isalpha():
                self[key] = 0
                return self[key]
            case _:
                try:
                    return int(key)
                except ValueError:
                    raise KeyError(f"Invalid register: {key}")


@dataclass(frozen=True)
class Sound(Exception):
    frequency: int


class Synth:
    def __init__(self) -> None:
        self.registers = Registers()

    def run_instruction(self, instruction: str) -> int:
        match instruction.split():
            case ["snd", x]:
                self.registers["sound"] = self.registers[x]
            case ["set", x, y]:
                self.registers[x] = self.registers[y]
            case ["add", x, y]:
                self.registers[x] += self.registers[y]
            case ["mul", x, y]:
                self.registers[x] *= self.registers[y]
            case ["mod", x, y]:
                self.registers[x] %= self.registers[y]
            case ["rcv", x]:
                if self.registers[x] != 0:
                    raise Sound(frequency=self.registers["sound"])
            case ["jgz", x, y]:
                if self.registers[x] > 0:
                    return self.registers[y]
            case _:
                raise ValueError(f"Invalid instruction: {instruction}")
        return 1

    def run_until_sound(self, instructions: list[str]) -> int:
        i = 0
        while 0 <= i < len(instructions):
            try:
                i += self.run_instruction(instructions[i])
            except Sound as e:
                return e.frequency
        raise ValueError("No sound played")


def part1(puzzle_input: list[str]) -> int:
    s = Synth()
    return s.run_until_sound(puzzle_input)


def part2(puzzle_input: list[str]) -> int:
    ...


def main() -> None:
    puzzle_input = read_input("2017-18_input.txt")
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
