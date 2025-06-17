import random
import csv
import math
import itertools


items = [{"name" : "watch", "price" : 2000, "weight" : 1},
         {"name" : "laptop", "price" : 3000, "weight" : 2},
         {"name" : "phone", "price" : 1500, "weight" : 5},
         {"name" : "tablet", "price" : 1000, "weight" : 1},
         {"name" : "tv", "price" : 5000, "weight" : 5}]

weight = 5


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

    if limit < 0:
        limit = input("Please enter weight limit")

    if array is None:
        no_items(array)

    best_value = 0

    for r in range(1, len(array) + 1):
        for combo in itertools.combinations(array, r):
            total_weight = sum(array["weight"] for array in combo)
            total_price = sum(array["price"] for array in combo)

            if total_weight <= limit and total_price > best_value:
                best_value = total_price
                knapsack = combo

    print(f"\nMy solution result for weight limit = {limit}:")

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
def tabu_search(array, limit, iterations=100, tabu_size=5):
    knapsack = []

    if limit < 0:
        limit = input("Please enter weight limit")

    if not array:
        array = no_items(array)

    current_items = random_solution(array, limit)
    knapsack = current_items
    tabu_list = []
    history = [current_items]

    def get_name_tuple(items):
        return tuple(sorted(item["name"] for item in items))

    def total_price(items):
        return sum(item["price"] for item in items)

    def total_weight(items):
        return sum(item["weight"] for item in items)

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
            if history:
                current_items = history.pop()
                continue
            else:
                break

        next_items, next_name_tuple = max(candidates, key=lambda x: total_price(x[0]))

        tabu_list.append(next_name_tuple)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        history.append(current_items)
        current_items = next_items

        if total_price(current_items) > total_price(knapsack):
            knapsack = current_items

    print(f"\nTabu Search result for weight limit = {limit}, tabu size = {tabu_size}:")

    return knapsack




print(goal(items, weight))
print(nearest_neighbour(items))
print(random_solution(items, 5))
print(brute_force(items, 5))
print(hill_climbing_deterministic(items, 10, 5))
print(hill_climbing_stochastic(items, 10, 5))
#print(simulated_annealing(items, 5))
#print(tabu_search(items, 5, iterations=50, tabu_size=5))
