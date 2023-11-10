import operator


def read_input(input_file) -> dict[int, dict[str, int]]:
    sues = {}
    with open(input_file, "r") as f:
        for k, line in enumerate(f):
            sue, n, *data = line.strip().split()
            assert sue == "Sue"
            n = int(n.rstrip(":"))
            new_sue = {}
            for d in " ".join(data).split(", "):
                key, value = d.split(": ")
                new_sue[key] = int(value)
            sues[n] = new_sue
    return sues


real_sue = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


def part1(sues: dict[int, dict[str, int]]) -> int:
    sues_left = sues.copy()
    for key, value in real_sue.items():
        not_real_sues = []
        for n, sue in sues_left.items():
            if key in sue and sue[key] != value:
                not_real_sues.append(n)
        for n in not_real_sues:
            del sues_left[n]

    # check only one left and return corresponding key
    assert len(sues_left) == 1
    return next(iter(sues_left))


conditions = dict.fromkeys(real_sue.keys(), operator.eq)
conditions["cats"] = operator.gt
conditions["trees"] = operator.gt
conditions["pomeranians"] = operator.lt
conditions["goldfish"] = operator.lt


def part2(sues: dict[int, dict[str, int]]) -> int:
    sues_left = sues.copy()
    for key, value in real_sue.items():
        not_real_sues = []
        for n, sue in sues_left.items():
            if key in sue and not conditions[key](sue[key], value):
                not_real_sues.append(n)
        for n in not_real_sues:
            del sues_left[n]

    # check only one left and return corresponding key
    assert len(sues_left) == 1
    return next(iter(sues_left))


def main() -> None:
    sues = read_input("2015-16_input.txt")
    print("Part 1: ")
    print("-------")
    print(part1(sues))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(sues))
    print("=======\n")


if __name__ == "__main__":
    main()
