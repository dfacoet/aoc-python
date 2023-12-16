def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.readline().strip().split(",")


def hash(s: str) -> int:
    v = 0
    for c in s:
        v = ((v + ord(c)) * 17) % 256
    return v


class Boxes:
    def __init__(self, n: int) -> None:
        self.boxes: list[dict[str, int]] = [{} for _ in range(n)]

    def run_instruction(self, instruction: str) -> None:
        if instruction.endswith("-"):
            label = instruction[:-1]
            self.boxes[hash(label)].pop(label, None)
        elif "=" in instruction:
            label, fs = instruction.split("=")
            focal_length = int(fs)
            self.boxes[hash(label)][label] = focal_length

    def run(self, instructions: list[str]) -> None:
        for instruction in instructions:
            self.run_instruction(instruction)

    def power(self) -> int:
        return sum(
            (b + 1) * (i + 1) * focal_length
            for b, box in enumerate(self.boxes)
            for i, focal_length in enumerate(box.values())
        )


def part1(puzzle_input: list[str]) -> int:
    return sum(hash(s) for s in puzzle_input)


def part2(puzzle_input: list[str]) -> int:
    boxes = Boxes(256)
    boxes.run(puzzle_input)
    return boxes.power()


def main() -> None:
    puzzle_input = read_input("2023-15_input.txt")
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
