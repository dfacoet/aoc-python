import hashlib

import tqdm


def read_input(input_file) -> str:
    with open(input_file) as f:
        [line] = f.readlines()
        return line


def part1(input: str) -> str:
    password = ""
    i = 0
    pbar = tqdm.tqdm(total=8)
    while len(password) < 8:
        hash = hashlib.md5(f"{input}{i}".encode()).hexdigest()
        if hash.startswith("00000"):
            password += hash[5]
            pbar.update()
        i += 1
    return password


def part2(input: str) -> str:
    password = [None] * 8
    i = 0
    pbar = tqdm.tqdm(total=8)
    while None in password:
        hash = hashlib.md5(f"{input}{i}".encode()).hexdigest()
        if hash.startswith("00000"):
            try:
                position = int(hash[5])
            except ValueError:
                pass
            else:
                if position < 8 and password[position] is None:
                    password[position] = hash[6]
                    pbar.update()
        i += 1
    return "".join(password)


def main() -> None:
    input = read_input("2016-05_input.txt")
    print("Part 1: ")
    # print("-------")
    print(part1(input))
    print("=======\n")
    print("Part 2: ")
    # print("-------")
    print(part2(input))
    print("=======\n")


if __name__ == "__main__":
    main()
