import hashlib
from collections import defaultdict

import tqdm


class DefaultDictKey(defaultdict):
    def __missing__(self, key):
        self[key] = self.default_factory(key)
        return self[key]


class HashDict(DefaultDictKey):
    def __init__(self, salt: str, n_repeats: int) -> None:
        def default_factory(n: int) -> str:
            s = salt + str(n)
            for _ in range(n_repeats):
                s = hashlib.md5(s.encode()).hexdigest()
            return s

        super().__init__(default_factory)


def find_triplet(hash: str) -> str:
    for a, b, c in zip(hash, hash[1:], hash[2:]):
        if a == b == c:
            return c
    return ""


def part1(salt: str, n_repeats: int = 1) -> int:
    n_keys = 64
    keys = []
    hashes = HashDict(salt, n_repeats)
    i = 0

    pbar = tqdm.tqdm(total=n_keys)
    while len(keys) < n_keys:
        if c := find_triplet(hashes[i]):
            if any(c * 5 in hashes[i + j + 1] for j in range(1000)):
                keys.append(i)
                pbar.update()
        i += 1
    return keys[-1]


def part2(salt: str) -> int:
    return part1(salt, 2017)


def main() -> None:
    input_value = "qzyelonm"
    print("Part 1: ")
    print("-------")
    print(part1(input_value))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(input_value))
    print("=======\n")


if __name__ == "__main__":
    main()
