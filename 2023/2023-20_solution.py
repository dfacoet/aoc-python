import math
from collections import defaultdict
from dataclasses import dataclass, field


def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


class Module:
    pass


class Broadcaster(Module):
    pass


@dataclass
class FlipFlop(Module):
    state: int = 0

    def flip(self) -> None:
        self.state = 1 - self.state


@dataclass
class Conjunction(Module):
    state: dict[str, int] = field(default_factory=dict)

    def signal(self) -> int:
        return int(not all(self.state.values()))


@dataclass
class Receiver(Module):
    pass


class LowPulseReceived(Exception):
    pass


class Circuit:
    def __init__(self, configuration: list[str]) -> None:
        self.modules, self.targets = self._parse(configuration)
        self.counts = dict.fromkeys((0, 1), 0)

    def push_button(self, final_modules: list[str] | None = None) -> list[str]:
        final_modules = final_modules or []
        sent_low = []

        pulses = [(0, "", "broadcaster")]

        while pulses:
            value, source, receiving = pulses.pop(0)
            self.counts[value] += 1
            if receiving in final_modules and value == 0:
                sent_low.append(receiving)
            module = self.modules[receiving]
            targets = self.targets[receiving]
            match module:
                case Broadcaster():
                    pulses.extend((value, receiving, t) for t in targets)
                case FlipFlop():
                    if value == 0:
                        module.flip()
                        pulses.extend(
                            (module.state, receiving, t) for t in targets
                        )
                case Conjunction():
                    module.state[source] = value
                    pulses.extend(
                        (module.signal(), receiving, t) for t in targets
                    )
                case Receiver():
                    if value == 0:
                        raise LowPulseReceived
                case _:
                    raise ValueError("Unknown module type:", module)
        return sent_low

    def _parse(
        self, configuration: list[str]
    ) -> tuple[dict[str, Module], dict[str, set[str]]]:
        modules: dict[str, Module] = {}
        sources = defaultdict(set)
        targets: dict[str, set[str]] = defaultdict(set)
        module_type: type[Module]
        for line in configuration:
            id, module_targets = line.split(" -> ")
            if id[0] == "%":
                name = id[1:]
                module_type = FlipFlop
            elif id[0] == "&":
                name = id[1:]
                module_type = Conjunction
            elif id == "broadcaster":
                name = id
                module_type = Broadcaster
            else:
                raise ValueError(f"Unknown module type: {id}")
            modules[name] = module_type()
            for t in module_targets.split(", "):
                sources[t].add(name)
                targets[name].add(t)
        # check receiver
        leaves = set(
            t for tl in targets.values() for t in tl if t not in targets
        )
        assert leaves == {"rx"}
        modules["rx"] = Receiver()
        targets["rx"] = set()
        # # initialise conjunctions
        for name, module in modules.items():
            if isinstance(module, Conjunction):
                module.state = dict.fromkeys(sources[name], 0)

        return modules, dict(targets)


def part1(puzzle_input: list[str]) -> int:
    circuit = Circuit(puzzle_input)
    for _ in range(1000):
        circuit.push_button()
    return circuit.counts[0] * circuit.counts[1]


def part2(puzzle_input: list[str]) -> int:
    circuit = Circuit(puzzle_input)
    # "rx" only receives from "hb". Hardcoding the inputs to "hb",
    # get their periods and find the lcm to get the first time hb
    # has all high inputs. Assumes simple periodicity and no phase difference.
    final_modules = ["rr", "js", "zb", "bs"]
    periods: dict[str, int] = {}

    c = 0
    while True:
        try:
            modules = circuit.push_button(final_modules)
            c += 1
            if modules:
                periods |= dict.fromkeys(modules, c)
                if len(periods) == len(final_modules):
                    break
        except LowPulseReceived:
            return c + 1
    return math.lcm(*periods.values())


def main() -> None:
    puzzle_input = read_input("2023-20_input.txt")
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
