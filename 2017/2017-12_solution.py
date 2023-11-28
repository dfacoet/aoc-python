def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


class Components:
    def __init__(self, n: int) -> None:
        self.components = [{i} for i in range(n)]

    def find(self, a: int) -> tuple[int, set[int]]:
        for i, component in enumerate(self.components):
            if a in component:
                return i, component
        raise ValueError(f"Component {a} not found")

    def add_link(self, a: int, b: int) -> None:
        i, component_a = self.find(a)
        j, component_b = self.find(b)
        if i == j:
            return
        component_a |= component_b
        del self.components[j]

    def add_from_string(self, s: str) -> None:
        a, bs = s.split(" <-> ")
        a = int(a)
        for b in bs.split(", "):
            self.add_link(a, int(b))

    def __len__(self) -> int:
        return len(self.components)


def part1(puzzle_input: list[str]) -> int:
    components = Components(len(puzzle_input))
    for s in puzzle_input:
        components.add_from_string(s)
    _, component0 = components.find(0)
    return len(component0)


def part2(puzzle_input: list[str]) -> int:
    components = Components(len(puzzle_input))
    for s in puzzle_input:
        components.add_from_string(s)
    return len(components)


def main() -> None:
    puzzle_input = read_input("2017-12_input.txt")
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
