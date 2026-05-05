import math


def calculate_poisson(actual_goals, expected_goals):
    """
    Calculates the probability of a team scoring actual_goals
    based on how many their average goals are expected_goals.
    """
    numerator = (expected_goals ** actual_goals) * math.exp(-expected_goals)
    denominator = math.factorial(actual_goals)
    return (numerator / denominator)

prob = calculate_poisson(2,1.5)
print(prob)