import math
from collections import defaultdict

INPUT = 34000000


def get_divisors(n: int) -> list[int]:
    divisors = [i for i in range(1, int(math.sqrt(n)) + 1) if n % i == 0]
    divisors += [n // d for d in divisors if d * d != n]
    return divisors


def prime_factorisation(n: int) -> dict[int, int]:
    i = 2
    factors = defaultdict(int)
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors[i] += 1
    if n > 1:
        factors[n] = 1
    return factors


def sigma_f(n: int) -> int:
    # divisor function oeis.org/A000203
    # Berndt 1985
    s = 1
    for p, a in prime_factorisation(n).items():
        s *= (p ** (a + 1) - 1) // (p - 1)
    return s


def part1(min_presents: int) -> int:
    min_sigma = min_presents / 10
    n = int(min_sigma ** (2 / 3))  # sigma(n) < n^3/2
    max_sigma = 0
    while True:
        n += 1
        value = sigma_f(n)
        if value >= min_sigma:
            return n
        max_sigma = max(max_sigma, value)


def truncated_divisor(n: int, largest_k: int) -> int:
    divisors = [i for i in get_divisors(n) if i * largest_k >= n]
    return sum(divisors)


def part2(min_presents: int, n_presents: int = 11, n_houses: int = 50) -> int:
    house = 0
    min_value = min_presents / n_presents
    while truncated_divisor(house, n_houses) < min_value:
        house += 1
    return house


def main() -> None:
    input: int = INPUT
    print("Part 1: ")
    print("-------")
    part1_answer = part1(input)
    print(part1_answer)
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(input))
    print("=======\n")


if __name__ == "__main__":
    main()
