from collections import defaultdict


def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return [line.strip() for line in f.readlines()]


class Registers(defaultdict):
    def __init__(self):
        super().__init__(int)

    def check(self, condition: str) -> bool:
        name, op, value = condition.split()
        return eval(" ".join([str(self[name]), op, value]))

    def execute(self, instruction: str) -> None:
        match instruction.split():
            case [name, "inc", value]:
                self[name] += int(value)
            case [name, "dec", value]:
                self[name] -= int(value)
            case _:
                raise ValueError(f"Invalid instruction: {instruction}")

    def run_line(self, line: str) -> None:
        instruction, condition = line.split(" if ")
        if self.check(condition):
            self.execute(instruction)


def part1(puzzle_input: list[str]) -> int:
    registers = Registers()
    for line in puzzle_input:
        registers.run_line(line)
    return max(registers.values())


def part2(puzzle_input: list[str]) -> int:
    registers = Registers()
    max_value = 0
    for line in puzzle_input:
        registers.run_line(line)
        max_value = max(max_value, max(registers.values()))
    return max_value


def main() -> None:
    puzzle_input = read_input("2017-08_input.txt")
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
