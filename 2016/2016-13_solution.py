def is_wall(x: int, y: int, input_value: int = 1358) -> bool:
    if x < 0 or y < 0:
        return True
    n = x * x + 3 * x + 2 * x * y + y + y * y + input_value
    binary_digits = bin(n)[2:]
    return bool(binary_digits.count("1") % 2)


def part1(input_value: int, target: tuple[int, int]) -> int:
    n_steps = 0
    visited = {(1, 1)}
    step_positions = {(1, 1)}

    while step_positions:
        next_positions = set()
        for x, y in step_positions:
            if (x, y) == target:
                return n_steps
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                new_position = (x + dx, y + dy)
                if new_position not in visited and not is_wall(*new_position):
                    visited.add(new_position)
                    next_positions.add(new_position)
        step_positions = next_positions
        n_steps += 1
    raise RuntimeError("No path found")


def part2(input_value: int, target: tuple[int, int]) -> int:
    visited = {(1, 1)}
    step_positions = {(1, 1)}

    for _ in range(50):
        next_positions = set()
        for x, y in step_positions:
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                new_position = (x + dx, y + dy)
                if new_position not in visited and not is_wall(*new_position):
                    visited.add(new_position)
                    next_positions.add(new_position)
        step_positions = next_positions

    return len(visited)


def main() -> None:
    input_value = 1358
    target = (31, 39)
    print("Part 1: ")
    print("-------")
    print(part1(input_value, target))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(input_value, target))
    print("=======\n")


if __name__ == "__main__":
    main()
