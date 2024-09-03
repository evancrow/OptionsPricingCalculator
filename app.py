from helpers.inputs import integer_input, float_input, string_input, options_input
from calculators.binomial_tree_model import BinomialTreeModel

model = BinomialTreeModel(229, 230, 21/361, 0.0438, 0.226, 100)
print(model.calculate_call())
print(model.calculate_put())