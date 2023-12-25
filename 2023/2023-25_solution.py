import networkx as nx
import numpy as np
from scipy import optimize, sparse


def read_input(input_file) -> list[str]:
    with open(input_file, "r") as f:
        return f.read().splitlines()


def parse_input(puzzle_input: list[str]) -> nx.Graph:
    g = nx.Graph()
    for line in puzzle_input:
        node, neighbors = line.split(": ")
        for neighbor in neighbors.split(" "):
            g.add_edge(node, neighbor)
    return g


def split_graph(
    nodes: list[str], cutoff: float, v1: np.ndarray, v2: np.ndarray
) -> tuple[set[str], set[str]]:
    c1 = {n for n, v in zip(nodes, np.abs(v1)) if v > cutoff}
    c2 = {n for n, v in zip(nodes, np.abs(v2)) if v > cutoff}
    return c1, c2


def part1(puzzle_input: list[str]) -> int:
    g = parse_input(puzzle_input)
    adj = nx.adjacency_matrix(g).astype(float)
    _, eigvecs = sparse.linalg.eigsh(adj, k=2)
    v2, v1 = eigvecs.T

    def f(cutoff: float) -> float:
        c1, c2 = split_graph(g.nodes, cutoff, v1, v2)
        return len(c1) + len(c2) - len(g.nodes)

    cutoff = optimize.root_scalar(f, bracket=[0.01, 0.2]).root
    c1, c2 = split_graph(g.nodes, cutoff, v1, v2)
    return len(c1) * len(c2)


def main() -> None:
    puzzle_input = read_input("2023-25_input.txt")
    print("Part 1: ")
    print("-------")
    print(part1(puzzle_input))
    print("=======\n")


if __name__ == "__main__":
    main()
