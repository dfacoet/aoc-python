def read_input(input_file) -> list[str]:
    with open(input_file) as f:
        return f.read().splitlines()


def has_abba(s: str) -> bool:
    assert set("[]").intersection(s) == set()
    for a, b, c, d in zip(s, s[1:], s[2:], s[3:]):
        if a != b and a == d and b == c:
            return True
    return False


def supports_tls(s: str) -> bool:
    words = s.replace("[", "]").split("]")
    # odd elements are inside brackets
    if any(has_abba(hypernet) for hypernet in words[1::2]):
        return False
    return any(has_abba(word) for word in words[::2])


def match_brackets(s: str) -> bool:
    open_idx = []
    closed_idx = []
    for i, c in enumerate(s):
        if c == "[":
            open_idx.append(i)
        elif c == "]":
            closed_idx.append(i)
        else:
            assert c.isalpha()
    assert len(open_idx) == len(closed_idx)
    return all(o < c for o, c in zip(open_idx, closed_idx))


def part1(input: list[str]) -> int:
    for s in input:
        assert match_brackets(s)
    return sum(supports_tls(s) for s in input)


def find_aba(s: str, reverse: bool = False) -> set[tuple[str, str]]:
    assert set("[]").intersection(s) == set()
    abas = set()
    for a, b, c in zip(s, s[1:], s[2:]):
        if a != b and a == c:
            if reverse:
                abas.add((b, a))
            else:
                abas.add((a, b))
    return abas


def supports_ssl(s: str) -> bool:
    words = s.replace("[", "]").split("]")
    supernets = words[::2]
    hypernets = words[1::2]
    abas = set()
    babs = set()
    for supernet in supernets:
        abas |= find_aba(supernet)
    for hypernet in hypernets:
        babs |= find_aba(hypernet, reverse=True)
    return bool(abas.intersection(babs))


def part2(input: list[str]) -> int:
    return sum(supports_ssl(s) for s in input)


def main() -> None:
    input = read_input("2016-07_input.txt")
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
