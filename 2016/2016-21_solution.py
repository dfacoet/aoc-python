def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


class Scrambler:
    def __init__(self, password: str) -> None:
        self.chars = list(password)

    @property
    def password(self) -> str:
        return "".join(self.chars)

    def swap(self, i: int, j: int) -> None:
        self.chars[i], self.chars[j] = self.chars[j], self.chars[i]

    def rotate(self, n: int) -> None:
        n = n % len(self.chars)
        self.chars = self.chars[n:] + self.chars[:n]

    def eval(self, instruction: str) -> None:
        match instruction.split():
            case ["swap", "position", i, "with", "position", j]:
                self.swap(int(i), int(j))
            case ["swap", "letter", x, "with", "letter", y]:
                i, j = self.chars.index(x), self.chars.index(y)
                self.swap(i, j)
            case ["rotate", "left", n, "steps" | "step"]:
                self.rotate(int(n))
            case ["rotate", "right", n, "steps" | "step"]:
                self.rotate(-int(n))
            case ["rotate", "based", "on", "position", "of", "letter", x]:
                i = self.chars.index(x)
                self.rotate(-(i + 1 + (i >= 4)))
            case ["reverse", "positions", i, "through", j]:
                i, j = int(i), int(j)
                self.chars[i : j + 1] = self.chars[i : j + 1][::-1]
            case ["move", "position", i, "to", "position", j]:
                self.chars.insert(int(j), self.chars.pop(int(i)))
            case _:
                raise ValueError(f"Invalid instruction: {instruction}")

    def reverse_eval(self, instruction: str) -> None:
        match instruction.split():
            case ["swap", "position", i, "with", "position", j]:
                self.swap(int(i), int(j))
            case ["swap", "letter", x, "with", "letter", y]:
                i, j = self.chars.index(x), self.chars.index(y)
                self.swap(i, j)
            case ["rotate", "left", n, "steps" | "step"]:
                self.rotate(-int(n))
            case ["rotate", "right", n, "steps" | "step"]:
                self.rotate(int(n))
            case ["rotate", "based", "on", "position", "of", "letter", x]:
                i = self.chars.index(x)
                # TODO: better way
                if i % 2 != 0:
                    r = (i + 1) // 2
                elif i == 0:
                    r = 1
                elif i == 2:
                    r = -2
                elif i == 4:
                    r = -1
                elif i == 6:
                    r = 0
                self.rotate(r)
            case ["reverse", "positions", i, "through", j]:
                i, j = int(i), int(j)
                self.chars[i : j + 1] = self.chars[i : j + 1][::-1]
            case ["move", "position", i, "to", "position", j]:
                self.chars.insert(int(i), self.chars.pop(int(j)))
            case _:
                raise ValueError(f"Invalid instruction: {instruction}")

    def reverse_run(self, instructions: list[str]) -> None:
        for instruction in instructions[::-1]:
            self.reverse_eval(instruction)

    def run(self, instructions: list[str]) -> None:
        for instruction in instructions:
            self.eval(instruction)


def part1(puzzle_input: list[str]) -> ...:
    s = Scrambler("abcdefgh")
    s.run(puzzle_input)
    return s.password


def part2(puzzle_input: list[str]) -> ...:
    s = Scrambler("fbgdceah")
    s.reverse_run(puzzle_input)
    return s.password


def main() -> None:
    puzzle_input = read_input("2016-21_input.txt")
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
