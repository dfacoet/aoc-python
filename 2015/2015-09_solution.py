from dataclasses import dataclass, field
from itertools import permutations


@dataclass
class DistanceMap:
    locations: set[str] = field(default_factory=set)
    distances: dict[(str, str), int] = field(default_factory=dict)

    def add_location(self, node: str) -> None:
        self.locations.add(node)

    def add_distance(self, start: str, end: str, distance: int) -> None:
        self.add_location(start)
        self.add_location(end)
        self.distances[(start, end)] = distance
        self.distances[(end, start)] = distance

    def path_length(self, path: list[str]) -> int:
        return sum(
            self.distances[(path[i], path[i + 1])]
            for i in range(len(path) - 1)
        )

    def shortest_path(self) -> int:
        return min(
            self.path_length(path) for path in permutations(self.locations)
        )

    def longest_path(self) -> int:
        return max(
            self.path_length(path) for path in permutations(self.locations)
        )


def read_input(input_file) -> DistanceMap:
    map = DistanceMap()
    with open(input_file, "r") as f:
        for line in f.readlines():
            line = line.strip()
            start, to, end, equal, distance = line.split(" ")
            assert to == "to"
            assert equal == "="
            map.add_distance(start, end, int(distance))
    return map


def part1(distance_map: DistanceMap) -> int:
    return distance_map.shortest_path()


def part2(distance_map: DistanceMap) -> int:
    return distance_map.longest_path()


def main() -> None:
    distances = read_input("2015-09_input.txt")
    print("Part 1: ")
    print("-------")
    print(part1(distances))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(distances))
    print("=======\n")


if __name__ == "__main__":
    main()
