import operator
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable, Literal

BINARY_OPERATORS = {
    "AND": operator.and_,
    "OR": operator.or_,
    "LSHIFT": operator.lshift,
    "RSHIFT": operator.rshift,
}


@dataclass
class Wire:
    name: str
    inputs: list["Wire"] = field(default_factory=list)
    operator: Literal["AND", "OR", "LSHIFT", "RSHIFT", "NOT", ""] = ""
    _value: int | None = None

    def value(self) -> int:
        if self._value is None:
            try:
                self._value = int(self.name)
            except ValueError:
                match self.operator:
                    case "":
                        self._value = self.inputs[0].value()
                    case "NOT":
                        self._value = ~self.inputs[0].value()
                    case _:
                        self._value = BINARY_OPERATORS[self.operator](
                            self.inputs[0].value(), self.inputs[1].value()
                        )
        return self._value


class DefaultDictKey(defaultdict):
    default_factory: Callable[[], Any]

    def __missing__(self, key):
        self[key] = self.default_factory(key)
        return self[key]


@dataclass
class Circuit:
    wires: dict[str, Wire] = field(
        default_factory=lambda: DefaultDictKey(Wire)
    )

    def evaluate(self, wire: str = "a") -> int:
        return self.wires[wire].value()

    def add_wire(self, instruction: str) -> None:
        input_string, output = instruction.split(" -> ")

        match input_string.split():
            case [input]:
                inputs = [self.wires[input]]
                operator = ""
            case ["NOT", input]:
                inputs = [self.wires[input]]
                operator = "NOT"
            case [input1, operator, input2]:
                inputs = [self.wires[input1], self.wires[input2]]

        self.wires[output].inputs = inputs
        self.wires[output].operator = operator

    def reset(self) -> None:
        for wire in self.wires.values():
            wire._value = None


def read_input(input_file) -> Circuit:
    circuit = Circuit()
    with open(input_file, "r") as f:
        for line in f:
            circuit.add_wire(line.strip())
    return circuit


def part1(circuit: Circuit) -> int:
    return circuit.evaluate()


def part2(circuit: Circuit) -> int:
    value_a = circuit.evaluate()
    circuit.reset()
    circuit.wires["b"]._value = value_a
    return circuit.evaluate()


def main() -> None:
    circuit = read_input("2015-07_input.txt")
    print("Part 1: ")
    print("-------")
    print(part1(circuit))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(circuit))
    print("=======\n")


if __name__ == "__main__":
    main()
