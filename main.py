import csv
import random
import math
import itertools
import argparse


def read_items(file):
    objects = []
    reader = csv.DictReader(file)
    for row in reader:
        objects.append({
            "name": row["name"],
            "weight": int(row["weight"]),
            "price": int(row["price"])
        })
    return objects


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--alg", type=str, required=True, choices=[
        "generate_neighbours", "random_solution", "brute_force", "hill_climbing_deterministic",
        "hill_climbing_stochastic", "simulated_annealing", "tabu_search", "genetic_algorithm"
    ], help="Choose an algorithm")

    # General parameters
    parser.add_argument("--filename", type=str, required=True, help="Load a CSV file with items")
    parser.add_argument("--limit", type=int, required=True, help="Limit")
    parser.add_argument("--iterations", type=int, default=100)

    # Tabu search algorithm parameters
    parser.add_argument("--tabu_size", type=int, default=10)
    parser.add_argument("--rollback", action="store_true")

    # Simulated annealing algorithm parameters
    parser.add_argument("--temp", type=float, default=100.0)
    parser.add_argument("--cooling", type=float, default=0.95)
    parser.add_argument("--min_temp", type=float, default=0.01)

    # Genetic algorithm parameters
    parser.add_argument("--population_size", type=int, default=20)
    parser.add_argument("--generations", type=int, default=100)
    parser.add_argument("--elitism", action="store_true")

    args = parser.parse_args()
    with open(args.filename, newline='') as f:
        items = read_items(f)

    if args.alg == "generate_neighbours":
        result = generate_neighbours(items)
        print(f"{result}")
    elif args.alg == "random_solution":
        result = random_solution(items, args.limit)
        print(f"{result}")
    elif args.alg == "brute_force":
        result = brute_force(items, args.limit)
        print(f"{result}")
    elif args.alg == "hill_climbing_deterministic":
        result = hill_climbing_deterministic(items, args.iterations, args.limit)
        print(f"{result}")
    elif args.alg == "hill_stochastic":
        result = hill_climbing_stochastic(items, args.iterations, args.limit)
        print(f"{result}")
    elif args.alg == "simulated_annealing":
        result = simulated_annealing(items, args.limit, args.temp, args.cooling, args.min_temp)
        print(f"{result}")
    elif args.alg == "tabu_search":
        result = tabu_search(items, args.limit, args.iterations, args.tabu_size, args.rollback)
        print(f"{result}")
    elif args.alg == "genetic_algorithm":
        result = genetic_algorithm(
            items, args.limit, args.population_size, args.generations, args.elitism)
        print(f"{result}")
    else:
        print("Unknown algorithm")
        return

items = [
    {"name": "Laptop", "weight": 3, "price": 4000},
    {"name": "Smartphone", "weight": 1, "price": 2500},
    {"name": "Headphones", "weight": 1, "price": 800},
    {"name": "Camera", "weight": 2, "price": 3200},
    {"name": "Watch", "weight": 1, "price": 1500},
    {"name": "Tablet", "weight": 1, "price": 1800},
    {"name": "Bluetooth Speaker", "weight": 2, "price": 1200},
    {"name": "Portable Charger", "weight": 1, "price": 600},
    {"name": "Gaming Console", "weight": 3, "price": 3500},
    {"name": "E-reader", "weight": 1, "price": 1000},
    {"name": "External Hard Drive", "weight": 1, "price": 900},
    {"name": "Smart Glasses", "weight": 1, "price": 2200},
    {"name": "Fitness Tracker", "weight": 1, "price": 700},
    {"name": "Drone", "weight": 4, "price": 4500},
    {"name": "Wireless Mouse", "weight": 1, "price": 300},
    {"name": "Keyboard", "weight": 2, "price": 1100},
    {"name": "Microphone", "weight": 1, "price": 1300},
    {"name": "Action Camera", "weight": 1, "price": 2700},
    {"name": "VR Headset", "weight": 2, "price": 3800},
    {"name": "Smart Home Hub", "weight": 1, "price": 1600},
]

weight = 4

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

# Hill climbing algorithm deterministic version
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



# Hill climbing algorithm stochastic version
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


# Simulated annealing algorithm
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



# Tabu Search algorithm
def tabu_search(array, limit, iterations, tabu_size, lp=False):
    def get_name_tuple(items):
        return tuple(sorted(item["name"] for item in items))

    current_items = random_solution(array, limit)
    knapsack = current_items
    tabu_list = []
    history = [current_items]

    best_value, best_weight = evaluate_solution(knapsack, limit)

    for _ in range(iterations):
        neighbours = generate_neighbours(array)
        candidates = []

        for neighbour in neighbours:
            candidate = []
            total_weight = 0
            for item in neighbour:
                if total_weight + item["weight"] <= limit:
                    candidate.append(item)
                    total_weight += item["weight"]

            value, weight = evaluate_solution(candidate, limit)
            name_tuple = get_name_tuple(candidate)

            if name_tuple not in tabu_list:
                candidates.append((candidate, name_tuple, value, weight))

        if not candidates:
            if lp and history:
                rollback_found = False
                while history:
                    previous = history.pop()
                    temp_neighbours = generate_neighbours(previous)
                    for temp in temp_neighbours:
                        temp_candidate = []
                        temp_weight = 0
                        for item in temp:
                            if temp_weight + item["weight"] <= limit:
                                temp_candidate.append(item)
                                temp_weight += item["weight"]

                        temp_value, temp_weight = evaluate_solution(temp_candidate, limit)
                        temp_name_tuple = get_name_tuple(temp_candidate)
                        if temp_name_tuple not in tabu_list:
                            current_items = previous
                            rollback_found = True
                            break
                    if rollback_found:
                        break
                if not rollback_found:
                    break
            else:
                break
        else:
            next_items, next_name_tuple, next_value, next_weight = max(candidates, key=lambda x: x[2])

            tabu_list.append(next_name_tuple)
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)

            history.append(current_items)
            current_items = next_items

            if next_value > best_value:
                knapsack = next_items
                best_value = next_value
                best_weight = next_weight

    print(f"\nTabu Search limit = {limit}, weight = {best_weight}, value = {best_value}, iterations = {iterations}, tabu size = {tabu_size}, rollback enabled = {lp}:")
    return knapsack


# Genetic algorithm
def generate_individual(items, limit):
    random.shuffle(items)
    individual = []
    w = 0
    for item in items:
        if w + item["weight"] <= limit:
            individual.append(item)
            w += item["weight"]
    return individual

def crossover_one_point(parent1, parent2):
    min_length = min(len(parent1), len(parent2))
    if min_length < 2:
        return parent1[:] if random.random() < 0.5 else parent2[:]
    point = random.randint(1, min_length - 1)
    child = parent1[:point] + [item for item in parent2 if item not in parent1[:point]]
    return child

def crossover_uniform(parent1, parent2):
    child = []
    for i in range(max(len(parent1), len(parent2))):
        if i < len(parent1) and i < len(parent2):
            chosen = random.choice([parent1[i], parent2[i]])
        elif i < len(parent1):
            chosen = parent1[i]
        elif i < len(parent2):
            chosen = parent2[i]
        else:
            break
        if chosen not in child:
            child.append(chosen)
    return child

def mutate_swap(individual):
    if len(individual) < 2:
        return individual
    i, j = random.sample(range(len(individual)), 2)
    individual[i], individual[j] = individual[j], individual[i]
    return individual

def mutate_remove_add(individual, all_items, limit):
    if individual:
        individual.pop(random.randrange(len(individual)))
    items_pool = [item for item in all_items if item not in individual]
    random.shuffle(items_pool)
    total_w = sum(i["weight"] for i in individual)
    for item in items_pool:
        if total_w + item["weight"] <= limit:
            individual.append(item)
            total_w += item["weight"]
    return individual

def genetic_algorithm(array, limit, population_size, generations, elitism=True):
    population = [generate_individual(array[:], limit) for _ in range(population_size)]
    best = max(population, key=lambda ind: evaluate_solution(ind, limit))
    stagnation = 0

    for gen in range(generations):
        new_population = []

        if elitism == True:
            new_population.append(best)

        while len(new_population) < population_size:
            parents = random.sample(population, 2)

            if random.random() < 0.5:
                child = crossover_one_point(parents[0], parents[1])
            else:
                child = crossover_uniform(parents[0], parents[1])

            if random.random() < 0.5:
                child = mutate_swap(child)
            else:
                child = mutate_remove_add(child, array, limit)

            total_w = sum(item["weight"] for item in child)
            while total_w > limit:
                item = random.choice(child)
                child.remove(item)
                total_w -= item["weight"]

            new_population.append(child)

        population = new_population

        current_best = max(population, key=lambda ind: evaluate_solution(ind, limit))

        if evaluate_solution(current_best, limit) > evaluate_solution(best, limit):
            best = current_best
            stagnation = 0
        else:
            stagnation += 1
            if stagnation >= 10:
                break

        if evaluate_solution(best, limit) == sum(item["price"] for item in array):
            break

        items_price, _ = evaluate_solution(best, limit)

    print(f"\nGenetic algorithm limit = {limit}, weight = {weight}, value = {items_price}, "
          f"population size = {population_size}, generations = {generations}, elitism = {elitism}:")
    return best


if __name__ == "__main__":
    main()

#print(generate_neighbours(items))
#print(random_solution(items, weight))
#print(brute_force(items, weight))
#print(hill_climbing_deterministic(items, 20, weight))
#print(hill_climbing_stochastic(items, 20, weight))
#print(simulated_annealing(items, weight, 1000, 0.95, 1))
#print(tabu_search(items, weight, 50, 5))
#print(genetic_algorithm(items, weight, 20, 100, True))
