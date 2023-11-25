from collections import Counter
from collections.abc import Iterator
from dataclasses import dataclass, field
from functools import cached_property


def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return [line.strip() for line in f.readlines()]


def part1(puzzle_input: list[str]) -> str:
    parents: set[str] = set()
    children: set[str] = set()
    for line in puzzle_input:
        match line.split():
            case [name, _]:
                # assuming a connected non trivial DAG with a single
                # root, we can ignore the leaves
                pass
            case [name, _, "->", *children_names]:
                parents.add(name)
                children.update((c.rstrip(",") for c in children_names))
    roots = parents - children
    assert len(roots) == 1
    return roots.pop()


@dataclass
class Program:
    name: str
    weight: int
    programs: dict[str, "Program"]
    children_names: list[str] = field(default_factory=list)

    @property
    def children(self) -> Iterator["Program"]:
        return (self.programs[c] for c in self.children_names)

    @cached_property
    def total_weight(self) -> int:
        return self.weight + sum(c.total_weight for c in self.children)

    def is_balanced(self) -> bool:
        return len(set(c.total_weight for c in self.children)) <= 1


def weight_key(p: Program) -> int:
    return p.total_weight


def part2(puzzle_input: list[str]) -> int:
    programs: dict[str, Program] = {}
    for line in puzzle_input:
        match line.split():
            case [name, weight]:
                children_names: list[str] = []
            case [name, weight, "->", *children_names]:
                children_names = [c.rstrip(",") for c in children_names]
            case _:
                raise ValueError(f"Invalid input: {line}")
        programs[name] = Program(
            name, int(weight[1:-1]), programs, children_names
        )

    for program in programs.values():
        if not program.is_balanced():
            (balanced_weight, _), (unbalanced_weight, n) = Counter(
                c.total_weight for c in program.children
            ).most_common()
            assert n == 1
            correction = balanced_weight - unbalanced_weight
            unbalanced_program_weight = next(
                c.weight
                for c in program.children
                if c.total_weight == unbalanced_weight
            )
            return unbalanced_program_weight + correction

    raise ValueError("No unbalanced program found")


def main() -> None:
    puzzle_input = read_input("2017-07_input.txt")
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
