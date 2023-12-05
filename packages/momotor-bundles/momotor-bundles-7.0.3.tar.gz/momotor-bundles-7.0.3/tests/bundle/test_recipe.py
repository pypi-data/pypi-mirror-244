from pathlib import Path

from momotor.bundles.recipe import RecipeBundle


# def test_recipe_get_steps():
#     path = Path(__file__).parent / 'files' / 'full-recipe'
#
#     recipe_bundle = RecipeBundle.from_file(path)
#
#     tree = list(recipe_bundle.steps().items())
#
#     assert [
#         ('step-1', 2, []),
#         ('step-2', 1, ['step-1']),
#         ('step-3', 2, ['step-1', 'step-2']),
#         ('step-4', 3, ['step-1']),
#         ('step-5', 0, ['step-3']),
#     ] == tree


# def test_recipe_get_test_products():
#     path = Path(__file__).parent / 'files' / 'full-recipe'
#
#     recipe_bundle = RecipeBundle.from_file(path)
#     recipe_reader = RecipeReader(recipe_bundle)
#
#     products = list(recipe_reader.get_tests())
#
#     assert [] == products
