# Input state

#########################
# 4 # .  .. .. .. .. .. #
# 3 # .  .. .. .. .. .. #
# 2 # .  .M .M .. .. .. #
# 1 # E  G. G. GM GM GM #
#########################


# Part 1

# The best you can do is to always take two items up and one down.
# To move all items up one floor, you need at least 2 * (10 - 2) + 1 = 17 moves.
# This lower bound is tight:
# For each pair, take both up and go back with the chip (10 moves)
# Then go up with 2 chips and back with 1 three times (16) and
# finally take the last two up (17).

# In the initial configuration, two items are already on the top floor,
# saving up to 4 moves -> need at least 13 moves to get all on the second floor.
# Again, this lower bound is tight:
# Take the unpaired generators up, go back with a chip (2 moves)
# Then proceed as before with 2 * (7 - 2) + 1 = 11 moves (13 total).

# Therefore the minimum number of moves is 13 + 2 * 17 = 47.


# Part 2

# There are two extra matched pairs on the first floor, adding
# a total of 3 * 2 * 4 = 24 moves, so the total is 71.


def part1(input: tuple[int, int, int, int]) -> int:
    n = sum(input)
    assert input[2] == input[3] == 0
    first_to_second = 2 * (input[0] - 2) + 1
    up_one_full_floor = 2 * (n - 2) + 1
    return first_to_second + 2 * up_one_full_floor


def part2(input: tuple[int, int, int, int]) -> int:
    input = (input[0] + 4,) + input[1:]
    return part1(input)


def main() -> None:
    items_in_floor = (8, 2, 0, 0)
    print("Part 1: ")
    print("-------")
    print(part1(items_in_floor))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(items_in_floor))
    print("=======\n")


if __name__ == "__main__":
    main()
