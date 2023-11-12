from collections import Counter, defaultdict
from collections.abc import Iterator
from dataclasses import dataclass, field


@dataclass
class Molecule:
    atoms: tuple[str, ...] = field(default_factory=tuple)

    def __str__(self):
        return "".join(self.atoms)

    @classmethod
    def from_str(cls, string: str) -> "Molecule":
        molecule_list = []
        current = ""
        for c in string + "X":
            if c.isupper():
                molecule_list.append(current)
                current = c
            else:
                current += c
        assert molecule_list[0] == ""
        return cls(tuple(molecule_list[1:]))

    @classmethod
    def electron(cls) -> "Molecule":
        return cls(atoms=("e",))

    def __add__(self, other) -> "Molecule":
        match other:
            case str():
                return Molecule(self.atoms + (other,))
            case Molecule():
                return Molecule(self.atoms + other.atoms)
            case _:
                raise NotImplementedError

    def __len__(self) -> int:
        return len(self.atoms)

    def split(self, i: int) -> tuple["Molecule", "Molecule"]:
        return Molecule(self.atoms[:i]), Molecule(self.atoms[i + 1 :])

    def insert(self, i: int, other: "Molecule") -> "Molecule":
        a, b = self.split(i)
        return a + other + b

    def replace(
        self, target_atom: str, possible_replacements: list["Molecule"]
    ) -> Iterator["Molecule"]:
        for i, a in enumerate(self.atoms):
            if a == target_atom:
                for replacement in possible_replacements:
                    yield self.insert(i, replacement)

    def replace_all(
        self,
        replacements: dict[str, list["Molecule"]],
        names_only: bool = False,
    ) -> Iterator["Molecule"]:
        for i, a in enumerate(self.atoms):
            if a in replacements:
                for replacement in replacements[a]:
                    new_molecule = self.insert(i, replacement)
                    if names_only:
                        yield str(new_molecule)
                    else:
                        yield new_molecule


def read_input(input_file) -> tuple[dict[str, list[Molecule]], Molecule]:
    replacements = defaultdict(list)
    with open(input_file, "r") as f:
        lines = f.readlines()
    for line in lines[:-2]:
        k, v = line.rstrip().split(" => ")
        replacements[k].append(Molecule.from_str(v))
    assert lines[-2] == "\n"
    molecule = Molecule.from_str(lines[-1].strip())
    return replacements, molecule


def part1(replacements: dict[str, list[Molecule]], molecule: Molecule) -> int:
    return len(set(molecule.replace_all(replacements, names_only=True)))


def part2(_: dict[str, list[Molecule]], target_molecule: Molecule) -> int:
    element_counts = Counter(target_molecule.atoms)
    assert element_counts["Rn"] == element_counts["Ar"]
    return (
        sum(element_counts.values())
        - 2 * element_counts["Rn"]
        - 2 * element_counts["Y"]
        - 1
    )


def main() -> None:
    replacements, molecule = read_input("2015-19_input.txt")
    print("Part 1: ")
    print("-------")
    print(part1(replacements, molecule))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(replacements, molecule))
    print("=======\n")


if __name__ == "__main__":
    main()
