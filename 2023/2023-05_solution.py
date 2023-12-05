from dataclasses import dataclass


def read_input(input_file) -> list[list[str]]:
    with open(input_file, "r") as f:
        return [b.splitlines() for b in f.read().split("\n\n")]


def string_overlap(s1: str, s2: str) -> str:
    overlap = ""
    for i in range(min(len(s1), len(s2)) + 1):
        if s1[-i:] == s2[:i]:
            overlap = s2[:i]
    return overlap


@dataclass(frozen=True)
class Interval:
    left: int
    right: int

    def __contains__(self, n: int) -> bool:
        return self.left <= n <= self.right

    def __add__(self, n: int) -> "Interval":
        return Interval(self.left + n, self.right + n)


@dataclass(frozen=True)
class IntervalShift(Interval):
    diff: int

    def __call__(
        self, interval: Interval
    ) -> tuple[Interval | None, set[Interval]]:
        if self.left <= interval.left:
            if self.right >= interval.right:
                return interval + self.diff, set()
            elif self.right > interval.left:
                return (
                    Interval(interval.left, self.right) + self.diff,
                    {Interval(self.right + 1, interval.right)},
                )
        elif self.left <= interval.right:
            if self.right < interval.right:
                return (
                    Interval(self.left, self.right) + self.diff,
                    {
                        Interval(interval.left, self.left - 1),
                        Interval(self.right + 1, interval.right),
                    },
                )
            else:
                return Interval(self.left, interval.right) + self.diff, {
                    Interval(interval.left, self.left - 1)
                }
        return None, {interval}

    def apply(
        self, intervals: set[Interval]
    ) -> tuple[set[Interval], set[Interval]]:
        shifted = set()
        leftovers = set()
        for interval in intervals:
            new_interval, leftover = self(interval)
            if new_interval is not None:
                shifted.add(new_interval)
            leftovers.update(leftover)
        return shifted, leftovers


@dataclass
class Map:
    name: str
    intervals: list[IntervalShift]

    @classmethod
    def from_strings(cls, strings: list[str]) -> "Map":
        name = strings[0].split(" ")[0]
        intervals = []
        for s in strings[1:]:
            destination, origin, length = map(int, s.split(" "))
            intervals.append(
                IntervalShift(
                    origin, origin + length - 1, destination - origin
                )
            )
        return cls(name, sorted(intervals, key=lambda i: i.left))

    def __call__(self, n: int) -> int:
        for interval in self.intervals:
            if n in interval:
                return n + interval.diff
        return n

    def apply(self, intervals: set[Interval]) -> set[Interval]:
        new_intervals = set()
        leftovers = intervals
        for s in self.intervals:
            shifted_intervals, leftovers = s.apply(leftovers)
            new_intervals.update(shifted_intervals)
        new_intervals.update(leftovers)
        return new_intervals


def componse(callables):
    def composed(*args, **kwargs):
        result = callables[0](*args, **kwargs)
        for c in callables[1:]:
            result = c(result)
        return result

    return composed


def parse_input(puzzle_input: list[list[str]]) -> tuple[list[int], list[Map]]:
    seeds = list(map(int, puzzle_input[0][0].split(" ")[1:]))
    maps = [Map.from_strings(strings) for strings in puzzle_input[1:]]
    return seeds, maps


def part1(puzzle_input: list[list[str]]) -> int:
    seeds, maps = parse_input(puzzle_input)
    full_map = componse(maps)
    return min(full_map(seed) for seed in seeds)


def parse_input2(
    puzzle_input: list[list[str]],
) -> tuple[set[Interval], list[Map]]:
    seeds = list(map(int, puzzle_input[0][0].split(" ")[1:]))
    intervals = {
        Interval(start, start + length - 1)
        for start, length in zip(seeds[::2], seeds[1::2])
    }
    maps = [Map.from_strings(strings) for strings in puzzle_input[1:]]
    return intervals, maps


def part2(puzzle_input: list[list[str]]) -> int:
    intervals, maps = parse_input2(puzzle_input)
    for map_ in maps:
        intervals = map_.apply(intervals)
    return min(i.left for i in intervals)


def main() -> None:
    puzzle_input = read_input("2023-05_input.txt")
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
