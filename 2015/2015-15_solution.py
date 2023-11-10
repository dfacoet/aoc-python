from dataclasses import dataclass
from functools import cached_property

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
    kcal: int | None = None,
) -> Recipe:
    assert sum(initial_quantities.values()) == 100
    recipe = Recipe(ingredients, initial_quantities)
    max_value = recipe.value1()
    k = 0
    visited = []

    while True:
        visited.append(recipe.quantities)
        moves = {
            score: recipe
            for score, recipe in recipe.moves_dict().items()
            if recipe.quantities not in visited
        }
        if kcal:
            moves = {
                value: move
                for value, move in moves.items()
                if move.feature_amount("calories") == kcal
            }
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

    recipe = find_recipe(ingredients, initial_quantities, verbose=True)
    return recipe.value1()


def five_hundred_calories(recipe: Recipe, verbose: bool = False) -> Recipe:
    k = 0

    min_dc = recipe.delta_c()
    k = 0

    while True:
        moves = recipe.moves_dict2()
        proposed_value = min(moves)
        if proposed_value > min_dc:
            break
        recipe = moves[proposed_value]
        min_dc = proposed_value
        k += 1
        if verbose:
            print(f"Step {k}, value: {min_dc}")

    return recipe


def part2(ingredients: Ingredients) -> int:
    initial_quantities = {
        "Sugar": 25,
        "Sprinkles": 25,
        "Candy": 25,
        "Chocolate": 25,
    }
    recipe = find_recipe(ingredients, initial_quantities, verbose=True)
    recipe = five_hundred_calories(recipe, verbose=True)
    # recipe = find_recipe(recipe, verbose=True, kcal=500, initial_recipe=recipe)
    return recipe.value1(), recipe.delta_c()


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
