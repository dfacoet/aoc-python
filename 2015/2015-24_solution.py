from functools import reduce
from itertools import chain, combinations


def read_input(input_file) -> list[int]:
    with open(input_file, "r") as f:
        return [int(line.strip()) for line in f]


def entanglement(group: tuple[int, ...]) -> int:
    return reduce(lambda x, y: x * y, group)


def find_minimum_first_group_size(
    packages: list[int], target_weight: int
) -> int:
    first_group_size = 0
    while True:
        if sum(packages[:first_group_size]) >= target_weight:
            break
        first_group_size += 1
    return first_group_size


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def balance_two_groups(packages: list[int], target_weight: int) -> bool:
    assert sum(packages) == target_weight * 2
    for group in powerset(packages):
        if sum(group) == target_weight:
            return True
    return False


def balance_three_groups(packages: list[int], target_weight: int) -> bool:
    assert sum(packages) == target_weight * 3
    for group1 in powerset(packages):
        if sum(group1) == target_weight:
            complement = [x for x in packages if x not in group1]
            if balance_two_groups(complement, target_weight):
                return True
    return False


def part1(input: list[int]) -> int:
    total_weight = sum(input)
    target_weight = total_weight // 3
    assert target_weight * 3 == total_weight

    packages = sorted(input, reverse=True)
    first_group_size = find_minimum_first_group_size(packages, target_weight)

    while first_group_size < len(packages):
        candidate_first_groups = [
            group
            for group in combinations(packages, first_group_size)
            if sum(group) == target_weight
        ]
        candidate_first_groups = sorted(
            candidate_first_groups, key=entanglement
        )
        for group1 in candidate_first_groups:
            complement = [x for x in packages if x not in group1]
            if balance_two_groups(complement, target_weight):
                return entanglement(group1)
        first_group_size += 1

    raise ValueError("No solution found")


def part2(input: list[int]) -> int:
    total_weight = sum(input)
    target_weight = total_weight // 4
    assert target_weight * 4 == total_weight

    packages = sorted(input, reverse=True)
    first_group_size = find_minimum_first_group_size(packages, target_weight)

    while first_group_size < len(packages):
        candidate_first_groups = [
            group
            for group in combinations(packages, first_group_size)
            if sum(group) == target_weight
        ]
        candidate_first_groups = sorted(
            candidate_first_groups, key=entanglement
        )

        for group1 in candidate_first_groups:
            complement = [x for x in packages if x not in group1]
            if balance_three_groups(complement, target_weight):
                return entanglement(group1)

        first_group_size += 1

    raise ValueError("No solution found")


def main() -> None:
    input = read_input("2015-24_input.txt")
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
