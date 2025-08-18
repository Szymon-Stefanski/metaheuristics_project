def simulated_annealing(array, limit, initial_temp, cooling_rate, min_temp):
    current_solution = random_solution(array, limit)
    best_solution = current_solution[:]
    best_score, best_weight = evaluate_solution(best_solution, limit)

    temperature = initial_temp

    while temperature > min_temp:
        neighbours = generate_neighbours(array)
        neighbour = random.choice(neighbours)

        candidate = []
        total_weight = 0
        for item in neighbour:
            if total_weight + item["weight"] <= limit:
                candidate.append(item)
                total_weight += item["weight"]

        candidate_score, _ = evaluate_solution(candidate, limit)
        current_score, _ = evaluate_solution(current_solution, limit)

        delta = candidate_score - current_score

        if delta > 0 or random.random() < math.exp(delta / temperature):
            current_solution = candidate

        best_score_now, best_weight_now = evaluate_solution(current_solution, limit)
        if best_score_now > best_score:
            best_solution = current_solution
            best_score = best_score_now
            best_weight = best_weight_now

        temperature *= cooling_rate

    print(f"\nSimulated annealing limit = {limit}, weight = {best_weight}, value = {best_score}:")
    return best_solution
