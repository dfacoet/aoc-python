from dataclasses import dataclass


@dataclass
class Reindeer:
    name: str
    max_speed: int
    fly_time: int
    rest_time: int

    points: int = 0

    @property
    def period(self) -> int:
        return self.fly_time + self.rest_time

    def distance(self, time: int) -> int:
        full_cycles, rest = divmod(time, self.period)
        time_in_motion = self.fly_time * full_cycles + min(rest, self.fly_time)
        return self.max_speed * time_in_motion

    @classmethod
    def from_string(cls, line: str) -> "Reindeer":
        line = line.strip().split()
        return cls(
            name=line[0],
            max_speed=int(line[3]),
            fly_time=int(line[6]),
            rest_time=int(line[13]),
        )


def read_input(input_file) -> list[Reindeer]:
    with open(input_file, "r") as f:
        return [Reindeer.from_string(line) for line in f.readlines()]


def part1(reindeers: list[Reindeer]) -> int:
    return max(reindeer.distance(2503) for reindeer in reindeers)


def part2(reindeers: list[Reindeer]) -> int:
    for t in range(1, 2504):
        max_distance = max(reindeer.distance(t) for reindeer in reindeers)
        for reindeer in reindeers:
            if reindeer.distance(t) == max_distance:
                reindeer.points += 1
    return max(reindeer.points for reindeer in reindeers)


def main() -> None:
    reindeer = read_input("2015-14_input.txt")
    print("Part 1: ")
    print("-------")
    print(part1(reindeer))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(reindeer))
    print("=======\n")


if __name__ == "__main__":
    main()
