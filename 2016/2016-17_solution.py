import hashlib
from collections import Counter


def md5_string(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()


def position(path: str) -> tuple[int, int]:
    counts = Counter(path)
    return counts["R"] - counts["L"], counts["D"] - counts["U"]


def part1(passcode: str) -> str:
    paths = [""]
    while paths:
        new_paths = []
        for path in paths:
            # find possible directions
            path_hash = md5_string(passcode + path)
            for c, step in zip(path_hash, "UDLR"):
                # check if open
                if c in "bcdef":
                    if position(new_path := path + step) == (3, 3):
                        return new_path
                    new_paths.append(new_path)
        paths = new_paths

    raise RuntimeError("No path found")


def part2(passcode: str) -> str:
    paths = [("", 0, 0)]
    longest: int | None = None
    while paths:
        new_paths = []
        for path in paths:
            path_hash = md5_string(passcode + path[0])
            for c, step in zip(path_hash, "UDLR"):
                new_path_str = path[0] + step
                new_position = (
                    path[1] + (step == "R") - (step == "L"),
                    path[2] + (step == "D") - (step == "U"),
                )
                if (
                    c in "bcdef"
                    and 0 <= new_position[0] <= 3
                    and 0 <= new_position[1] <= 3
                ):
                    if new_position == (3, 3):
                        longest = len(new_path_str)
                    else:
                        new_paths.append((new_path_str, *new_position))
        paths = new_paths
    return longest


def main() -> None:
    puzzle_input = "rrrbmfta"
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
