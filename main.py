import random
import csv
import math
import itertools


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


# Function to create array or import from data file function
def no_items(array):
    if array is None:
        array = []

    while True:
        option = input("\nChoose an option:"
                       "\n0. Import data from a file (.csv)"
                       "\n1. Add item."
                       "\n2. Show items."
                       "\n3. Complete task.\n")

        match option:
            case "0":
                bag = []
                path = input("\nEnter path to file: ")
                try:
                    with open(path, "r") as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            bag.append({
                                "name": row["name"],
                                "price": int(row["price"]),
                                "weight": int(row["weight"]),
                            })
                    array.extend(bag)
                    print("Items successfully imported.")
                except FileNotFoundError:
                    print("File not found! Please try again.")

            case "1":
                name = input("Insert item's name: ")
                price = input("Insert item's price: ")
                weight = input("Insert item's weight: ")
                array.append({"name": name, "price": int(price), "weight": int(weight)})

            case "2":
                if array:
                    print("\nCurrent items:")
                    for item in array:
                        print(item)
                else:
                    print("There are no items!")

            case "3":
                print("Finished item input.")
                return array

            case _:
                print("Invalid option! Please try again.")

    return array


# Knapsack problem solution function
def goal(array=None, limit=None):
    knapsack = []

    if limit is None or limit < 0:
        limit = int(input("Please enter weight limit: "))

    if array is None:
        return []

    permuts = array.copy()
    candidates = []

    for r in range(1, len(permuts) + 1):
        for combo in itertools.combinations(permuts, r):
            total_weight = sum(item["weight"] for item in combo)
            total_price = sum(item["price"] for item in combo)
            if total_weight <= limit:
                candidates.append({
                    "items": list(combo),
                    "total_price": total_price,
                    "total_weight": total_weight
                })

    if candidates:
        best_price = max(c["total_price"] for c in candidates)
        best_combinations = [c for c in candidates if c["total_price"] == best_price]

        knapsack = best_combinations[0]["items"]

    print(f"\nKnapsack best possible items configuration with weight limit = {limit}:")
    return knapsack


# Nearest neighbour function
def nearest_neighbour(array=None):
    if array is None:
        array = no_items(array)

    if len(array) < 2:
        return []

    neighbours = []

    for i in range(len(array)):
        neighbour = array.copy()
        j = (i + 1) % len(array)
        neighbour[i], neighbour[j] = neighbour[j], neighbour[i]
        neighbours.append(neighbour)

    print("\nNearest neighbours:")

    return neighbours


# Random solution function
def random_solution(array, limit):
    knapsack = []

    if limit < 0:
        limit = input("Please enter weight limit")

    if not array:
        array = no_items(array)

    total_weight = 0
    total_price = 0

    current = array.copy()
    random.shuffle(current)

    for item in current:
        if total_weight + item["weight"] <= limit:
            total_weight += item["weight"]
            total_price += item["price"]
            knapsack.append(item)

    print(f"\nRandom solution result for weight limit = {limit}:")

    return knapsack


# Brute force algorithm
def brute_force(array, limit):
    knapsack = []

    if limit < 0:
        limit = input("Please enter weight limit")

    if not array:
        array = no_items(array)

    best_value = 0

    for r in range(1, len(array) + 1):
        for combination in itertools.combinations(array, r):
            total_weight = sum(item["weight"] for item in combination)
            total_price = sum(item["price"] for item in combination)

            if total_weight <= limit and total_price > best_value:
                best_value = total_price
                knapsack = combination

    print(f"\nBrute-force result for weight limit = {limit}:")

    return knapsack


# Hill climbing solution
def hill_climbing_deterministic(array, iterations, limit):
    knapsack = []

    if limit < 0:
        limit = input("Please enter weight limit")

    if not array:
        array = no_items(array)

    current_items = random_solution(array, limit)
    knapsack = current_items

    def total_price_weight(items):
        total_weight = sum(item["weight"] for item in items)
        total_price = sum(item["price"] for item in items)
        return total_price, total_weight

    best_price, _ = total_price_weight(knapsack)

    for _ in range(iterations):
        neighbours = nearest_neighbour(array)

        improved = False
        for neighbour in neighbours:
            total_weight = 0
            total_price = 0
            selected = []

            for item in neighbour:
                if total_weight + item["weight"] <= limit:
                    total_weight += item["weight"]
                    total_price += item["price"]
                    selected.append(item)

            if total_price > best_price:
                knapsack = selected
                best_price = total_price
                improved = True

        if not improved:
            break

    print(f"\nHill climbing (deterministic) result for weight limit = {limit}:")

    return knapsack



def hill_climbing_stochastic(array, iterations, limit):
    knapsack = []

    if limit < 0:
        limit = int(input("Please enter weight limit: "))

    if not array:
        array = no_items(array)

    knapsack = random_solution(array, limit)

    def evaluate(solution):
        total_weight = sum(item["weight"] for item in solution)
        total_price = sum(item["price"] for item in solution)
        return total_price, total_weight

    best_price, _ = evaluate(knapsack)

    for _ in range(iterations):
        neighbours = nearest_neighbour(array)
        neighbour = random.choice(neighbours)

        selected = []
        weight = 0
        price = 0
        for item in neighbour:
            if weight + item["weight"] <= limit:
                weight += item["weight"]
                price += item["price"]
                selected.append(item)

        if price > best_price:
            knapsack = selected
            best_price = price

    print(f"Hill climbing (stochastic) result for limit = {limit}")
    return knapsack


# Simulated annealing solution
def simulated_annealing(array, limit, initial_temp=1000, cooling_rate=0.95, min_temp=1):
    knapsack = []

    if limit < 0:
        limit = input("Please enter weight limit")

    if not array:
        array = no_items(array)

    current_items = random_solution(array, limit)
    knapsack = current_items
    temperature = initial_temp

    def total_price(items):
        return sum(item["price"] for item in items)

    while temperature > min_temp:
        neighbours = nearest_neighbour(array)
        next_candidate = random.choice(neighbours)

        candidate = []
        w = 0
        for item in next_candidate:
            if w + item["weight"] <= limit:
                w += item["weight"]
                candidate.append(item)

        delta = total_price(candidate) - total_price(current_items)

        if delta > 0 or random.random() < math.exp(delta / temperature):
            current_items = candidate

        if total_price(current_items) > total_price(knapsack):
            knapsack = current_items

        temperature *= cooling_rate

    print(f"\nSimulated annealing result for weight limit = {limit}:")

    return knapsack



# Tabu Search algorithm
def tabu_search(array, limit, iterations=100, tabu_size=5, lp=False):
    knapsack = []

    if limit is None or limit < 0:
        limit = int(input("Please enter weight limit"))

    if not array:
        return []

    current_items = random_solution(array, limit)
    knapsack = current_items
    tabu_list = []
    history = [current_items]

    def get_name_tuple(items):
        return tuple(sorted(item["name"] for item in items))

    def total_price(items):
        return sum(item["price"] for item in items)

    for _ in range(iterations):
        neighbours = nearest_neighbour(array)
        candidates = []

        for neighbour in neighbours:
            candidate = []
            w = 0
            for item in neighbour:
                if w + item["weight"] <= limit:
                    w += item["weight"]
                    candidate.append(item)

            name_tuple = get_name_tuple(candidate)
            if name_tuple not in tabu_list:
                candidates.append((candidate, name_tuple))

        if not candidates:
            if lp and history:
                rollback_found = False
                while history:
                    previous = history.pop()
                    temp_neighbours = nearest_neighbour(previous)
                    for temp in temp_neighbours:
                        temp_candidate = []
                        w = 0
                        for item in temp:
                            if w + item["weight"] <= limit:
                                w += item["weight"]
                                temp_candidate.append(item)

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
            next_items, next_name_tuple = max(candidates, key=lambda x: total_price(x[0]))

            tabu_list.append(next_name_tuple)
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)

            history.append(current_items)
            current_items = next_items

            if total_price(current_items) > total_price(knapsack):
                knapsack = current_items

    print(f"\nTabu Search result for weight limit = {limit}, tabu size = {tabu_size}, rollback enabled = {lp}:")
    return knapsack


def fitness(individual, limit):
    weight = sum(item["weight"] for item in individual)
    value = sum(item["price"] for item in individual)
    return value if weight <= limit else 0

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
    point = random.randint(1, min(len(parent1), len(parent2)) - 1)
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


def genetic_algorithm(array, limit, population_size=20, generations=100, elitism=True):
    population = [generate_individual(array[:], limit) for _ in range(population_size)]
    best = max(population, key=lambda ind: fitness(ind, limit))
    stagnation = 0

    for gen in range(generations):
        new_population = []

        if elitism:
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

        current_best = max(population, key=lambda ind: fitness(ind, limit))

        if fitness(current_best, limit) > fitness(best, limit):
            best = current_best
            stagnation = 0
        else:
            stagnation += 1
            if stagnation >= 10:
                break

        if fitness(best, limit) == sum(item["price"] for item in array):
            break

    print(f"\nGenetic algorithm result for weight limit = {limit}:")
    return best


print(goal(items, weight))
#print(nearest_neighbour(items))
#print(random_solution(items, 5))
#print(brute_force(items, 5))
#print(hill_climbing_deterministic(items, 10, 5))
#print(hill_climbing_stochastic(items, 10, 5))
#print(simulated_annealing(items, 5))
#print(tabu_search(items, 5, iterations=50, tabu_size=5))
