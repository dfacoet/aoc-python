import random
from dataclasses import dataclass

import numpy as np

INPUT = [
    "Sugar: capacity 3, durability 0, flavor 0, texture -3, calories 2",
    "Sprinkles: capacity -3, durability 3, flavor 0, texture 0, calories 9",
    "Candy: capacity -1, durability 0, flavor 4, texture 0, calories 1",
    "Chocolate: capacity 0, durability 0, flavor -2, texture 2, calories 8",
]


@dataclass
class Ingredients:
    values: dict[str, dict[str, int]]

    def __post_init__(self) -> None:
        one_ingredient = next(iter(self.values))
        self.features = list(self.values[one_ingredient].keys())
        assert all(
            list(values.keys()) == self.features
            for values in self.values.values()
        )
        self.score_features = [f for f in self.features if f != "calories"]

    @property
    def names(self) -> list[str]:
        return list(self.values.keys())

    def items(self):
        return self.values.items()

    def __getitem__(self, key: str) -> dict[str, int]:
        return self.values[key]

    def __next__(self) -> str:
        return next(iter(self.values))

    def __iter__(self):
        return iter(self.values)


@dataclass
class Recipe:
    ingredients: Ingredients
    quantities: dict[str, int]

    max_quantity: int = 100

    def __post_init__(self) -> None:
        assert self.ingredients.names == list(self.quantities)
        assert all(q >= 0 for q in self.quantities.values())
        assert sum(self.quantities.values()) == self.max_quantity

    def feature_amount(self, feature: str) -> int:
        total_feature = sum(
            self.quantities[ingredient] * self.ingredients[ingredient][feature]
            for ingredient in self.ingredients
        )
        return max(total_feature, 0)

    def value1(self) -> int:
        prod = 1
        for f in self.ingredients.score_features:
            if (a := self.feature_amount(f)) == 0:
                return 0
            prod *= a
        return prod

    def moves(self):
        for ingredient1 in self.ingredients:
            if self.quantities[ingredient1] == 0:
                continue
            for ingredient2 in self.ingredients:
                if (
                    ingredient1 == ingredient2
                    or self.quantities[ingredient2] == self.max_quantity
                ):
                    continue
                q = self.quantities.copy()
                q[ingredient1] -= 1
                q[ingredient2] += 1
                yield Recipe(self.ingredients, q)

    def moves_dict(self) -> dict[int, "Recipe"]:
        return {move.value1(): move for move in self.moves()}

    def delta_c(self) -> int:
        return (self.feature_amount("calories") - 500) ** 2

    def moves_dict2(self) -> dict[int, "Recipe"]:
        return {move.delta_c(): move for move in self.moves()}


def read_input(input: list[str]) -> Ingredients:
    ingredients: dict[str, dict[str, int]] = {}
    features: list[str] = []
    for line in input:
        ingredient, remaining = line.split(":")
        values = {}
        for s in remaining.strip().split(","):
            feature, value = s.strip().split()
            values[feature] = int(value)
        if features:
            assert features == values.keys()
        else:
            features = values.keys()
        ingredients[ingredient] = values

    return Ingredients(ingredients)


def find_recipe(
    ingredients: Ingredients,
    initial_quantities: dict[str, int],
    verbose: bool = False,
) -> Recipe:
    assert sum(initial_quantities.values()) == 100
    recipe = Recipe(ingredients, initial_quantities)
    max_value = recipe.value1()
    k = 0

    while True:
        moves = recipe.moves_dict()
        proposed_value = max(moves)
        if proposed_value < max_value:
            break
        recipe = moves[proposed_value]
        max_value = proposed_value
        k += 1
        if verbose:
            print(f"Step {k}, value: {max_value}")

    return recipe


def part1(ingredients: Ingredients) -> int:
    # pick a non-zero initial value
    # otherwise, need to avoid going back
    initial_quantities = {
        "Sugar": 25,
        "Sprinkles": 14,
        "Candy": 25,
        "Chocolate": 36,
    }

    recipe = find_recipe(ingredients, initial_quantities, verbose=False)
    return recipe.value1()


def part2(ingredients: Ingredients) -> int:
    # The constraint are strict enough that we can enumerate all
    # possible recipes
    cal = np.array([v["calories"] for v in ingredients.values.values()])

    constraint_solutions = []
    for a in range(101):
        for b in range(101):
            if a + b > 100:
                continue
            for c in range(101):
                if (d := 100 - a - b - c) < 0:
                    continue
                q = np.array([a, b, c, d])
                if cal @ q == 500:
                    constraint_solutions.append(q)

    # And evaluate them
    constrained_max = max(
        Recipe(ingredients, quantities=dict(zip(ingredients, q))).value1()
        for q in constraint_solutions
    )
    return constrained_max


def main() -> None:
    ingredients = read_input(INPUT)
    print("Part 1: ")
    print("-------")
    print(part1(ingredients))
    print("=======\n")
    print("Part 2: ")
    print("-------")
    print(part2(ingredients))
    print("=======\n")


if __name__ == "__main__":
    main()
