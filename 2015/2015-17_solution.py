import tqdm


def read_input(input_file) -> list[int]:
    with open(input_file, "r") as f:
        return [int(line.strip()) for line in f]


TOTAL_VOLUME = 150


def find_combinations(sizes: list[int]) -> list[list[int]]:
    combinations = []
    n = len(sizes)
    for i in tqdm.trange(2**n):
        digits = [int(d) for d in f"{i:0{n}b}"]
        volume = sum(s for d, s in zip(digits, sizes) if d)
        if volume == TOTAL_VOLUME:
            combinations.append(digits)
    return combinations


def part1(combinations: list[list[int]]) -> int:
    return len(combinations)


def part2(combinations: list[list[int]]) -> int:
    n_containers = [sum(x) for x in combinations]
    min_containers = min(n_containers)
    return n_containers.count(min_containers)


def main() -> None:
    sizes = read_input("2015-17_input.txt")
    combinations = find_combinations(sizes)
    print("Part 1: ")
    print("-------")
    print(part1(combinations))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(combinations))
    print("=======\n")


if __name__ == "__main__":
    main()
