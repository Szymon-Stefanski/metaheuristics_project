def brute_force(array, limit):
    knapsack = []

    best_value = 0
    best_weight = 0

    for r in range(1, len(array) + 1):
        for combination in itertools.combinations(array, r):
            value, weight = evaluate_solution(combination, limit)
            if value > best_value:
                best_value = value
                best_weight = weight
                knapsack = combination

    print(f"\nBrute-force limit = {limit}, weight = {best_weight}, value = {best_value}:")
    return knapsack
    