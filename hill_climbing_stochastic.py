def hill_climbing_stochastic(array, iterations, limit):
    knapsack = random_solution(array, limit)
    best_score, best_weight = evaluate_solution(knapsack, limit)

    for _ in range(iterations):
        neighbours = generate_neighbours(array)
        neighbour = random.choice(neighbours)

        candidate = []
        total_weight = 0

        for item in neighbour:
            if total_weight + item["weight"] <= limit:
                candidate.append(item)
                total_weight += item["weight"]

        score, _ = evaluate_solution(candidate, limit)

        if score > best_score:
            knapsack = candidate
            best_score = score
            best_weight = total_weight

    print(f"\nHill climbing (stochastic) limit = {limit}, weight = {best_weight}, value = {best_score}:")
    return knapsack
