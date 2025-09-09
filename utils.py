# Goal function
def evaluate_solution(solution, limit):
    total_weight = sum(item["weight"] for item in solution)
    total_price = sum(item["price"] for item in solution)

    if total_weight > limit:
        return 0, total_weight
    return total_price, total_weight


# Generate neighbours function
def generate_neighbours(array):
    neighbours = []

    for i in range(len(array)):
        neighbour = array.copy()
        j = (i + 1) % len(array)
        neighbour[i], neighbour[j] = neighbour[j], neighbour[i]
        neighbours.append(neighbour)

    print("\nGenerate neighbours:")
    return neighbours


# Random solution function
def random_solution(array, limit):
    knapsack = []

    current = array.copy()
    random.shuffle(current)

    total_weight = 0

    for item in current:
        if total_weight + item["weight"] <= limit:
            knapsack.append(item)
            total_weight += item["weight"]

    value, weight = evaluate_solution(knapsack, limit)

    print(f"\nRandom solution limit = {limit}, weight = {weight}, value = {value}:")
    return knapsack
    