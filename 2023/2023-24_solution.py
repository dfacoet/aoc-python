from functools import cached_property

import numpy as np
from attr import dataclass
from scipy import optimize


def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


class ParallelLines(Exception):
    pass


class CoincidentLines(Exception):
    pass


class PastCrossing(Exception):
    pass


@dataclass
class TCoord:
    r: tuple[int, int, int]
    v: tuple[int, int, int]

    def intersect2d(self, other: "TCoord") -> tuple[float, float]:
        m1 = self.v[1] / self.v[0]
        m2 = other.v[1] / other.v[0]
        if m1 == m2:
            if self.r[1] - m1 * self.r[0] == other.r[1] - m2 * other.r[0]:
                raise CoincidentLines
            else:
                raise ParallelLines
        dy = other.r[1] - self.r[1]
        x = (dy + m1 * self.r[0] - m2 * other.r[0]) / (m1 - m2)
        if any((x - c.r[0]) / c.v[0] < 0 for c in (self, other)):
            raise PastCrossing
        y = self.r[1] + m1 * (x - self.r[0])
        return x, y

    @cached_property
    def rarr(self) -> np.ndarray:
        return np.array(self.r)

    @cached_property
    def varr(self) -> np.ndarray:
        return np.array(self.v)

    def parallel_f(self, rv: np.ndarray) -> np.ndarray:
        return np.cross(rv[:3] - self.rarr, rv[3:] - self.varr)

    @classmethod
    def from_str(cls, s: str) -> "TCoord":
        r, v = map(lambda x: tuple(map(int, x.split(","))), s.split(" @ "))
        assert all(v)
        return cls(r, v)  # type: ignore[arg-type]


def part1(puzzle_input: list[str]) -> int:
    range = 200000000000000, 400000000000000
    initial_conditions = [TCoord.from_str(line) for line in puzzle_input]
    c = 0
    for i, ic1 in enumerate(initial_conditions):
        for ic2 in initial_conditions[i + 1 :]:
            try:
                x, y = ic1.intersect2d(ic2)
            except CoincidentLines:
                c += 1
                pass
            except (ParallelLines, PastCrossing):
                pass
            else:
                if range[0] <= x <= range[1] and range[0] <= y <= range[1]:
                    c += 1
    return c


def part2(puzzle_input: list[str]) -> int:
    initial_conditions = [TCoord.from_str(line) for line in puzzle_input]
    x0 = np.concatenate(
        (
            np.stack([ic.rarr for ic in initial_conditions])
            .mean(axis=0)
            .astype(int),
            np.stack([ic.varr for ic in initial_conditions])
            .mean(axis=0)
            .astype(int),
        )
    )

    def f(x: np.ndarray) -> np.ndarray:
        return np.concatenate(
            [tc.parallel_f(x) for tc in initial_conditions[:3]]
        )

    sol = optimize.least_squares(f, x0)
    assert np.allclose(sol.x, sol.x.astype(int))
    return sol.x[:3].sum().astype(int)


def main() -> None:
    puzzle_input = read_input("2023-24_input.txt")
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
