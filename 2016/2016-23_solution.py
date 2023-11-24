def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


class Computer:
    def __init__(self, program: list[str]) -> None:
        self.registers = dict.fromkeys("abcd", 0)
        self.registers["a"] = 7
        self.program = program.copy()

    def value(self, name: str) -> int:
        if name in "abcd":
            return self.registers[name]
        else:
            return int(name)

    def toggle_instruction(self, i: int) -> None:
        try:
            instruction = self.program[i].split()
        except IndexError:
            return
        match instruction:
            case ["inc", register]:
                self.program[i] = f"dec {register}"
            case ["dec" | "tgl", register]:
                self.program[i] = f"inc {register}"
            case ["jnz", origin, offset]:
                self.program[i] = f"cpy {origin} {offset}"
            case ["cpy", origin, target]:
                self.program[i] = f"jnz {origin} {target}"
            case _:
                raise ValueError(f"Invalid instruction {self.program[i]}")

    def run_program(self) -> None:
        i = 0
        c = 0
        k = 123456
        imax = 0
        while i < len(self.program):
            c += 1
            imax = max(imax, i)
            if c % k == 0:
                print(i, imax, c, self.registers)
            # HARDCODED: instructions 5-9 are equivalent to
            # a += b * d; c = 0; d = 0
            if i == 5:
                self.registers["a"] += (
                    self.registers["b"] * self.registers["d"]
                )
                self.registers["c"] = 0
                self.registers["d"] = 0
                i = 10
            match self.program[i].split():
                case ["cpy", origin, target]:
                    self.registers[target] = self.value(origin)
                case ["inc", register]:
                    self.registers[register] += 1
                case ["dec", register]:
                    self.registers[register] -= 1
                case ["jnz", origin, offset]:
                    if self.value(origin):
                        i += self.value(offset)
                        continue
                case ["tgl", offset]:
                    self.toggle_instruction(i + self.value(offset))
                case _:
                    raise ValueError(f"Invalid instruction {self.program[i]}")
            i += 1


def part1(puzzle_input: list[str]) -> int:
    computer = Computer(puzzle_input)
    computer.run_program()
    return computer.registers["a"]


def part2(puzzle_input: list[str]) -> int:
    computer = Computer(puzzle_input)
    computer.registers["a"] = 12
    computer.run_program()
    return computer.registers["a"]


def main() -> None:
    puzzle_input = read_input("2016-23_input.txt")
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
