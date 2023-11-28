def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().strip().split(",")


class DancingGroup:
    def __init__(self, s: str) -> None:
        self.p = list(s)

    def step(self, move: str) -> None:
        match move[0]:
            case "s":
                n = int(move[1:])
                self.p = self.p[-n:] + self.p[:-n]
            case "x":
                a, b = map(int, move[1:].split("/"))
                self.p[a], self.p[b] = self.p[b], self.p[a]
            case "p":
                a, b = move[1:].split("/")
                a, b = self.p.index(a), self.p.index(b)
                self.p[a], self.p[b] = self.p[b], self.p[a]
            case _:
                raise ValueError(f"Invalid move: {move}")

    def dance(self, moves: list[str]) -> None:
        for move in moves:
            self.step(move)

    def __repr__(self) -> str:
        return "".join(self.p)


def part1(puzzle_input: list[str]) -> str:
    programs = DancingGroup("abcdefghijklmnop")
    programs.dance(puzzle_input)
    return programs


def part2(puzzle_input: list[str]) -> str:
    programs = DancingGroup("abcdefghijklmnop")

    # Find period
    for i in range(10**9):
        programs.dance(puzzle_input)
        if str(programs) == "abcdefghijklmnop":
            break
    period = i + 1

    for _ in range(10**9 % period):
        programs.dance(puzzle_input)

    return programs


def main() -> None:
    puzzle_input = read_input("2017-16_input.txt")
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
