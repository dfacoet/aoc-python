import operator
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable


def read_input(input_file) -> tuple[list[str], list[str]]:
    with open(input_file, "r") as f:
        workflows, inputs = (b.splitlines() for b in f.read().split("\n\n"))
        return workflows, inputs


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def from_string(cls, s: str) -> "Part":
        assert s[0] == "{" and s[-1] == "}"
        vars = {}
        for assignment in s[1:-1].split(","):
            var, val = assignment.split("=")
            vars[var] = int(val)
        return cls(**vars)

    def total(self) -> int:
        return self.x + self.m + self.a + self.s


class Outcome(Exception):
    pass


class Rejected(Outcome):
    pass


class Accepted(Outcome):
    pass


@dataclass
class PartRange:
    # range = [min, max)
    x: tuple[int, int]
    m: tuple[int, int]
    a: tuple[int, int]
    s: tuple[int, int]

    def split(self, d: str, c: int) -> tuple["PartRange", "PartRange"]:
        a, b = getattr(self, d)
        less = self.__dict__ | {d: (a, c)}
        more = self.__dict__ | {d: (c, b)}
        return PartRange(**less), PartRange(**more)

    def n(self):
        if not self:
            raise ValueError("Empty range")
        return max(
            0,
            (
                (self.x[1] - self.x[0])
                * (self.m[1] - self.m[0])
                * (self.a[1] - self.a[0])
                * (self.s[1] - self.s[0])
            ),
        )

    def __bool__(self):
        for d in "xmas":
            if getattr(self, d)[0] >= getattr(self, d)[1]:
                return False
        return True


@dataclass
class Rule:
    attr: str
    op: Callable[[int, int], bool]
    val: int
    next: str

    def __call__(self) -> str:
        match self.next:
            case "A":
                raise Accepted
            case "R":
                raise Rejected
            case _:
                return self.next

    @classmethod
    def from_string(cls, s: str) -> "Rule":
        condition, next = s.split(":")
        attr = condition[0]
        op_s = condition[1]
        assert attr in "xmas"
        assert op_s in "<>"
        op = {"<": operator.lt, ">": operator.gt}[op_s]
        val = int(condition[2:])
        return cls(attr, op, val, next)

    def apply(self, range: PartRange) -> tuple[PartRange, PartRange]:
        if self.op == operator.gt:
            n, y = range.split(self.attr, self.val + 1)
        else:
            y, n = range.split(self.attr, self.val)
        return y, n


@dataclass
class Workflow:
    name: str
    rules: list[Rule]
    final: str

    def __call__(self, part: Part) -> str:
        for rule in self.rules:
            if rule.op(getattr(part, rule.attr), rule.val):
                return rule()
        match self.final:
            case "A":
                raise Accepted
            case "R":
                raise Rejected
            case _:
                return self.final

    def apply(self, range: PartRange) -> dict[str, list[PartRange]]:
        next_workflows = defaultdict(list)
        for rule in self.rules:
            y, n = rule.apply(range)
            if y:
                next_workflows[rule.next].append(y)
            range = n
        next_workflows[self.final].append(range)
        return dict(next_workflows)  # type: ignore[arg-type]

    @classmethod
    def from_string(cls, s: str) -> "Workflow":
        name, rules_string = s.split("{")
        assert rules_string[-1] == "}"
        *rule_strings, final = rules_string[:-1].split(",")
        rules = [Rule.from_string(s) for s in rule_strings]
        return cls(name, rules, final)


class System:
    def __init__(self, instructions: list[str]):
        self.workflows = {
            w.name: w for w in map(Workflow.from_string, instructions)
        }
        self.start = "in"

    def accept(self, part: Part) -> bool:
        wf_name = self.start
        while True:
            try:
                wf_name = self.workflows[wf_name](part)
            except Accepted:
                return True
            except Rejected:
                return False

    def process_range(self, range: PartRange) -> int:
        q = [(self.start, range)]
        accepted = 0
        while q:
            wf, range = q.pop()
            if wf == "A":
                accepted += range.n()
            elif wf == "R":
                continue
            else:
                for next_wf, ranges in self.workflows[wf].apply(range).items():
                    q.extend((next_wf, r) for r in ranges)
        return accepted


def part1(puzzle_input: tuple[list[str], list[str]]) -> int:
    system = System(puzzle_input[0])
    parts = [Part.from_string(p) for p in puzzle_input[1]]
    return sum(part.total() for part in parts if system.accept(part))


def part2(puzzle_input: tuple[list[str], list[str]]) -> int:
    system = System(puzzle_input[0])
    return system.process_range(
        PartRange((1, 4001), (1, 4001), (1, 4001), (1, 4001))
    )


def main() -> None:
    puzzle_input = read_input("2023-19_input.txt")
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
