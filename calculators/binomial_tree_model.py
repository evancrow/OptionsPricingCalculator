import copy
import math
from calculators.calculator import Calculator

class BinomialTreeModel(Calculator):
    # MARK: init
    def __init__(
            self,
            initial_price,
            strike_price,
            time_to_expiration,
            risk_free_rate,
            volatility,
            number_of_steps):
        super().__init__()

        self._initial_price = initial_price
        self._strike_price = strike_price
        self._time_to_expiration = time_to_expiration
        self._risk_free_rate = risk_free_rate
        self._volatility = volatility
        self._number_of_steps = number_of_steps
        self._time_step = time_to_expiration / number_of_steps
        self._tree = None

    # MARK: Public Calculate Methods
    def calculate_call(self):
        self.__build_tree_if_needed()
        option_prices = self.__calculate_option_prices(False, True)
        return option_prices[0][0]

    def calculate_put(self):
        self.__build_tree_if_needed()
        option_prices = self.__calculate_option_prices(True, True)
        return option_prices[0][0]

    # MARK: Private Calculate Methods
    def __calculate_option_prices(self, is_put, is_american):
        tree_copy = copy.deepcopy(self._tree)
        risk_neutral_probability = self.__calculate_risk_neutral_probability()

        for step_index in range(len(tree_copy) - 1, -1, -1):
            for node_index in range(len(tree_copy[step_index])):
                if step_index == len(tree_copy) - 1:
                    payoff = self._strike_price - tree_copy[step_index][node_index] if is_put else tree_copy[step_index][node_index] - self._strike_price
                    tree_copy[step_index][node_index] = max(payoff, 0)
                else:
                    exponential_rate = math.pow(math.e, -self._risk_free_rate * self._time_step)
                    up_node_value = risk_neutral_probability * tree_copy[step_index + 1][node_index]
                    down_node_value = (1 - risk_neutral_probability) * tree_copy[step_index + 1][node_index + 1]
                    continuation_value = exponential_rate * (up_node_value + down_node_value)

                    if is_american:
                        # For American options, include the possibility of early exercise.
                        immediate_exercise = self._strike_price - tree_copy[step_index][node_index] if is_put else tree_copy[step_index][node_index] - self._strike_price
                        tree_copy[step_index][node_index] = max(continuation_value, immediate_exercise, 0)
                    else:
                        # For European options, use only the continuation value.
                        tree_copy[step_index][node_index] = continuation_value

        return tree_copy

    # MARK: Up & Down Factor
    def __calculate_up_factor(self):
        return math.pow(math.e, self._volatility * math.sqrt(self._time_step))

    def __calculate_down_factor(self):
        return 1 / self.__calculate_up_factor()

    # MARK: Risk Neutral Probability
    def __calculate_risk_neutral_probability(self):
        up_factor = self.__calculate_up_factor()
        down_factor = self.__calculate_down_factor()

        return (math.pow(math.e, self._risk_free_rate * self._time_step) - down_factor) / (up_factor - down_factor)

    # MARK: Tree Building
    def __build_tree_if_needed(self):
        if self._tree is not None:
            # No need to rebuild the tree.
            return

        nodes = [[self._initial_price]]
        up_factor = self.__calculate_up_factor()
        down_factor = self.__calculate_down_factor()

        # There aren't any extra nodes to calculate, return early.
        if self._number_of_steps < 1:
            return nodes

        # For each node, apply the up and down factor.
        for node_index in range(1, self._number_of_steps + 1):
            temporary = []

            for index in range(0, len(nodes[node_index - 1])):
                # This is the node we are branching from.
                previous_node_price = nodes[node_index - 1][index]

                # Only apply the up factor to the first branch, as it will be the same as the
                # down factor for the following nodes.
                if index == 0:
                    temporary.append(previous_node_price * up_factor)

                temporary.append(previous_node_price * down_factor)

            nodes.append(temporary)

        self._tree = nodes
