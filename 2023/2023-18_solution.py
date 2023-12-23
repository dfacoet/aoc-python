def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


def parse(s: str) -> tuple[str, int]:
    direction, ds, _ = s.split()
    return direction, int(ds)


def parse_hex(s: str) -> tuple[str, int]:
    *_, n = s.split()
    assert n[:2] == "(#" and n[-1] == ")", n
    return "RDLU"[int(n[-2])], int(n[2:-2], 16)


def find_vertices(
    instructions: list[str], hex: bool = False
) -> tuple[list[tuple[int, int]], int]:
    i, j = 0, 0
    vertices: list[tuple[int, int]] = [(i, j)]
    parse_f = parse_hex if hex else parse
    total_length = 0
    for direction, distance in map(parse_f, instructions):
        match direction:
            case "U":
                i -= distance
            case "D":
                i += distance
            case "R":
                j += distance
            case "L":
                j -= distance
            case _:
                raise ValueError(f"Invalid direction {direction}")
        total_length += distance
        vertices.append((i, j))
    assert (i, j) == (0, 0)

    return (vertices, total_length)


def block_grid(
    vertices: list[tuple[int, int]]
) -> tuple[
    list[list[int]],
    dict[tuple[int, int], list[tuple[int, int]]],
    tuple[int, int],
]:
    igrid = sorted(set(i for i, _ in vertices))
    jgrid = sorted(set(j for _, j in vertices))
    idiff = [i2 - i1 for i1, i2 in zip(igrid, igrid[1:])]
    jdiff = [j2 - j1 for j1, j2 in zip(jgrid, jgrid[1:])]
    blocks = [[x * y for y in jdiff] for x in idiff]
    neighbors = {
        (i, j): [
            (i + di, j + dj) for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1))
        ]
        for i, row in enumerate(blocks)
        for j in range(len(row))
    }
    # cut links across the trench
    for v1, v2 in zip(vertices, vertices[1:]):
        if (x := v1[0]) == v2[0]:
            i = igrid.index(x)
            vj = (jgrid.index(v1[1]), jgrid.index(v2[1]))
            for j in range(min(vj), max(vj)):
                try:
                    neighbors[(i, j)].remove((i - 1, j))
                except KeyError:
                    pass
                try:
                    neighbors[(i - 1, j)].remove((i, j))
                except KeyError:
                    pass
        elif (y := v1[1]) == v2[1]:
            j = jgrid.index(y)
            vi = (igrid.index(v1[0]), igrid.index(v2[0]))
            for i in range(min(vi), max(vi)):
                try:
                    neighbors[(i, j)].remove((i, j - 1))
                except KeyError:
                    pass
                try:
                    neighbors[(i, j - 1)].remove((i, j))
                except KeyError:
                    pass
        else:
            raise ValueError("Consecutive vertices are not aligned")

    start_block = (igrid.index(vertices[0][0]), jgrid.index(vertices[0][1]))

    return blocks, neighbors, start_block


def fill_blocks(
    blocks: list[list[int]],
    neighbors: dict[tuple[int, int], list[tuple[int, int]]],
    start_block: tuple[int, int],
) -> int:
    to_visit = {start_block}
    visited = set()
    area = 0
    while to_visit:
        block = to_visit.pop()
        visited.add(block)
        area += blocks[block[0]][block[1]]
        for neighbor in neighbors[block]:
            if neighbor not in visited:
                to_visit.add(neighbor)
    return area


def part1(puzzle_input: list[str]) -> int:
    vertices, edge_length = find_vertices(puzzle_input, hex=False)
    return fill_blocks(*block_grid(vertices)) + edge_length // 2 + 1


def part2(puzzle_input: list[str]) -> int:
    vertices, edge_length = find_vertices(puzzle_input, hex=True)
    return fill_blocks(*block_grid(vertices)) + edge_length // 2 + 1


def main() -> None:
    puzzle_input = read_input("2023-18_input.txt")
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
