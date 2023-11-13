def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return [line.strip() for line in f]


class Computer:
    def __init__(
        self, instructions: list[str], a: int = 0, b: int = 0
    ) -> None:
        self.p: list[tuple[str, ...]] = [s.split() for s in instructions]
        self.registers = {"a": a, "b": b}

    def run_instruction(self, instruction: tuple[str, ...]) -> None:
        jump = 1
        match instruction:
            case "hlf", r:
                self.registers[r] //= 2
            case "tpl", r:
                self.registers[r] *= 3
            case "inc", r:
                self.registers[r] += 1
            case "jmp", offset:
                jump = int(offset)
            case "jie", r, offset if self.registers[r[0]] % 2 == 0:
                jump = int(offset)
            case "jio", r, offset if self.registers[r[0]] == 1:
                jump = int(offset)
        return jump

    def run_program(self) -> None:
        i = 0
        while i < len(self.p):
            # print(i, self.registers)
            i += self.run_instruction(self.p[i])


def part1(instructions: list[str]) -> int:
    computer = Computer(instructions)
    computer.run_program()
    return computer.registers["b"]


def part2(instructions: list[str]) -> int:
    computer = Computer(instructions, a=1)
    computer.run_program()
    return computer.registers["b"]


def main() -> None:
    input = read_input("2015-23_input.txt")
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
