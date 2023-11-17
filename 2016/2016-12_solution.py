from collections import defaultdict
from datetime import datetime


def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


class DefaultDictKey(defaultdict):
    def __missing__(self, key):
        self[key] = self.default_factory(key)
        return self[key]


class Computer:
    def __init__(self) -> None:
        self.registers = dict.fromkeys("abcd", 0)
        for key in "abcd":
            self.registers[key] = 0

    def value(self, name: str) -> int:
        if name in "abcd":
            return self.registers[name]
        else:
            return int(name)

    def eval(self, instruction: str) -> int:
        match instruction.split():
            case ["cpy", origin, target]:
                self.registers[target] = self.value(origin)
            case ["inc", register]:
                self.registers[register] += 1
            case ["dec", register]:
                self.registers[register] -= 1
            case ["jnz", origin, offset]:
                if self.value(origin):
                    return int(offset)
            case _:
                raise ValueError(f"Invalid instruction {instruction}")
        return 1

    def run_program(self, program: list[str]) -> int:
        i = 0
        while i < len(program):
            i += self.eval(program[i])
        return self.registers


def part1(input: list[str]) -> int:
    computer = Computer()
    computer.run_program(input)
    return computer.registers["a"]


def part2(input: list[str]) -> int:
    computer = Computer()
    computer.registers["c"] = 1
    computer.run_program(input)
    return computer.registers["a"]


def main() -> None:
    input = read_input("2016-12_input.txt")
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
