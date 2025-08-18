def hill_climbing_deterministic(array, iterations, limit):
    knapsack = random_solution(array, limit)
    best_score, best_weight = evaluate_solution(knapsack, limit)

    for _ in range(iterations):
        neighbours = generate_neighbours(array)
        improved = False

        for neighbour in neighbours:
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
                improved = True

        if not improved:
            break

    print(f"\nHill climbing (deterministic) limit = {limit}, weight = {best_weight}, value = {best_score}:")
    return knapsack
