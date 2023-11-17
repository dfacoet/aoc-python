import numpy as np


def iterate(data: np.ndarray) -> np.ndarray:
    return np.concatenate((data, [0], np.flip(1 - data)))


def checksum(data: np.ndarray) -> np.ndarray:
    while len(data) % 2 == 0:
        data = 1 - np.abs(data[::2] - data[1::2])
    return data


def part1(initial_data: str, size: int = 272) -> str:
    data = np.array([int(c) for c in initial_data], dtype=int)
    while len(data) < size:
        data = iterate(data)
    data = data[:size]
    return "".join(str(x) for x in checksum(data))


def part2(initial_data: str) -> str:
    return part1(initial_data, 35651584)


def main() -> None:
    initial_data = "10111100110001111"
    print("Part 1: ")
    print("-------")
    print(part1(initial_data))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(initial_data))
    print("=======\n")


if __name__ == "__main__":
    main()
