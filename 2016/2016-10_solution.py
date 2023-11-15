from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable, Union


def read_input(input_file) -> list[str]:
    with open(input_file) as f:
        return f.read().splitlines()


class Compare61and17(Exception):
    pass


@dataclass
class Output:
    id: int
    values: list[int] = field(default_factory=list)

    def receive(self, value: int, _: bool) -> None:
        self.values.append(value)


@dataclass
class Bot:
    id: int
    values: list[int] = field(default_factory=list)
    low_target: Union["Bot", Output] | None = None
    high_target: Union["Bot", Output] | None = None

    def receive(self, value: int, part1: bool = False) -> None:
        self.values.append(value)
        if len(self.values) >= 2:
            low, high = sorted(self.values)
            if part1 and (low, high) == (17, 61):
                raise Compare61and17(self.id)
            self.values = []
            self.low_target.receive(low, part1)
            self.high_target.receive(high, part1)


class DefaultDictKey(defaultdict):
    default_factory: Callable[[], Any]

    def __missing__(self, key):
        self[key] = self.default_factory(key)
        return self[key]


# value 5 goes to bot 32
# bot 149 gives low to bot 41 and high to bot 88


def part1(input: list[str]) -> int:
    bots: dict[int, Bot] = DefaultDictKey(Bot)
    outputs: dict[int, Output] = DefaultDictKey(Output)
    initial_values: dict[int, Bot] = {}
    classdict = {"bot": bots, "output": outputs}
    for line in input:
        match line.split():
            case ["value", value, "goes", "to", "bot", bot]:
                initial_values[int(value)] = bots[int(bot)]
            case [
                "bot",
                bot,
                "gives",
                "low",
                "to",
                bot_or_output_low,
                low_id,
                "and",
                "high",
                "to",
                bot_or_output_high,
                high_id,
            ]:
                bots[int(bot)].low_target = classdict[bot_or_output_low][
                    int(low_id)
                ]
                bots[int(bot)].high_target = classdict[bot_or_output_high][
                    int(high_id)
                ]
            case _:
                raise ValueError(f"Invalid instruction: {line}")
    try:
        for value, bot in initial_values.items():
            bot.receive(value, part1=True)
    except Compare61and17 as e:
        return int(e.args[0])
    raise ValueError("No bot compared 61 and 17")


def part2(input: list[str]) -> int:
    bots: dict[int, Bot] = DefaultDictKey(Bot)
    outputs: dict[int, Output] = DefaultDictKey(Output)
    initial_values: dict[int, Bot] = {}
    classdict = {"bot": bots, "output": outputs}
    for line in input:
        match line.split():
            case ["value", value, "goes", "to", "bot", bot]:
                initial_values[int(value)] = bots[int(bot)]
            case [
                "bot",
                bot,
                "gives",
                "low",
                "to",
                bot_or_output_low,
                low_id,
                "and",
                "high",
                "to",
                bot_or_output_high,
                high_id,
            ]:
                bots[int(bot)].low_target = classdict[bot_or_output_low][
                    int(low_id)
                ]
                bots[int(bot)].high_target = classdict[bot_or_output_high][
                    int(high_id)
                ]
            case _:
                raise ValueError(f"Invalid instruction: {line}")
    for value, bot in initial_values.items():
        bot.receive(value)
    prod = 1
    for i in range(3):
        [value] = outputs[i].values
        prod *= value
    return prod


def main() -> None:
    input = read_input("2016-10_input.txt")
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
