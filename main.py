import random
import csv
import math


items = [{"name" : "guitar", "price" : 500, "weight" : 3},
         {"name" : "laptop", "price" : 1000, "weight" : 2},
         {"name" : "phone", "price" : 500, "weight" : 1},
         {"name" : "tablet", "price" : 1000, "weight" : 1},
         {"name" : "tv", "price" : 3000, "weight" : 5}]

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

    permuts = array.copy()
    for i in range(len(permuts)-1):
        if permuts[i].get("weight") == limit:
            knapsack.append(permuts[i])
            permuts.remove(permuts[i])
            knapsack.sort(key=lambda x: x["price"], reverse=True)

        elif permuts[i].get("weight") < limit:
            for j in range(len(permuts)):
                while (permuts[j].get("weight") + permuts[i].get("weight")) <= limit:
                    if permuts[i].get("name") not in permuts[j].get("name"):
                        permuts.append({"name" : permuts[i].get("name") + " " + permuts[j].get("name"),
                                      "price" : permuts[i].get("price") + permuts[j].get("price"),
                                      "weight" : permuts[i].get("weight") + permuts[j].get("weight")})
                    break

    permuts.sort(key=lambda x: x["price"], reverse=True)

    for n in range(len(permuts) - 1, -1, -1):
        permuts[n]['name'] = " ".join(sorted(permuts[n]['name'].split()))
        if permuts[n].get("weight") != limit:
            del permuts[n]
        else:
            knapsack.append(permuts[n])

    knapsack = [dict(t) for t in {tuple(d.items()) for d in knapsack}]
    knapsack.sort(key=lambda x: x["price"], reverse=True)


    for m in range(len(knapsack) - 1, -1, -1):
        if knapsack[m].get("price") < knapsack[0].get("price"):
            del knapsack[m]

    print(f"\nKnapsack best possible items configuration with weight limit = {limit} :")
    return knapsack


# Nearest neighbour function
def nearest_neighbour(array=None):
    if array is None:
        array = no_items(array)

    neighbours = []

    for i in range(len(array)):
        neighbour = array.copy()
        neighbour[i], neighbour[(i+1) % len(array)] = neighbour[(i+1) % len(array)], neighbour[i]
        neighbours.append(neighbour)

    return neighbours


# Random solution function
def random_solution(array, limit):
    if not array:
        no_items(array)

    print("\nRandom solution for weight limit =", limit)

    total_weight = 0
    total_price = 0
    selected_names = []

    current = array.copy()
    random.shuffle(current)


    for item in current:
        if total_weight + item["weight"] <= limit:
            total_weight += item["weight"]
            total_price += item["price"]
            selected_names.append(item["name"])

    knapsack = {
        "name": " ".join(sorted(selected_names)),
        "price": total_price,
        "weight": total_weight
    }

    return knapsack


# Hill climbing solution
def hill_climbing(array, iterations, limit):
    current = random_solution(array, limit)
    best = current

    for _ in range(iterations):
        neighbours = nearest_neighbour(array)

        improved = False
        for neighbour in neighbours:
            total_weight = 0
            total_price = 0
            selected_names = []

            for item in neighbour:
                if total_weight + item["weight"] <= limit:
                    total_weight += item["weight"]
                    total_price += item["price"]
                    selected_names.append(item["name"])

            neighbour_solution = {
                "name": " ".join(sorted(selected_names)),
                "price": total_price,
                "weight": total_weight
            }

            if neighbour_solution["price"] > best["price"]:
                best = neighbour_solution
                improved = True

        if not improved:
            break

    print(f"\nHill climbing result for weight limit = {limit}:")
    return best



# Simulated annealing solution
def simulated_annealing(array, limit, initial_temp=1000, cooling_rate=0.95, min_temp=1):
    if not array:
        array = no_items(array)

    current = random_solution(array, limit)
    best = current
    temperature = initial_temp

    while temperature > min_temp:
        neighbour_items = nearest_neighbour(array)
        next_candidate = random.choice(neighbour_items)

        total_weight = 0
        total_price = 0
        selected_names = []

        for item in next_candidate:
            if total_weight + item["weight"] <= limit:
                total_weight += item["weight"]
                total_price += item["price"]
                selected_names.append(item["name"])

        candidate_solution = {
            "name": " ".join(sorted(selected_names)),
            "price": total_price,
            "weight": total_weight
        }

        delta = candidate_solution["price"] - current["price"]

        if delta > 0 or random.random() < math.exp(delta / temperature):
            current = candidate_solution

        if current["price"] > best["price"]:
            best = current

        temperature *= cooling_rate

    print(f"\nSimulated Annealing result for weight limit = {limit}:")
    return best


# Tabu Search algorithm
def tabu_search(array, limit, iterations=100, tabu_size=5):
    if not array:
        array = no_items(array)

    current = random_solution(array, limit)
    best = current
    tabu_list = []
    history = [current]

    for _ in range(iterations):
        neighbours = nearest_neighbour(array)
        candidates = []

        for neighbour in neighbours:
            total_weight = 0
            total_price = 0
            selected_names = []

            for item in neighbour:
                if total_weight + item["weight"] <= limit:
                    total_weight += item["weight"]
                    total_price += item["price"]
                    selected_names.append(item["name"])

            candidate_solution = {
                "name": " ".join(sorted(selected_names)),
                "price": total_price,
                "weight": total_weight
            }

            if candidate_solution["name"] not in tabu_list:
                candidates.append(candidate_solution)

        if not candidates:
            if history:
                current = history.pop()
                continue
            else:
                break

        next_solution = max(candidates, key=lambda x: x["price"])

        tabu_list.append(next_solution["name"])
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        history.append(current)
        current = next_solution

        if current["price"] > best["price"]:
            best = current

    print(f"\nTabu Search result for weight limit = {limit}, tabu size = {tabu_size}:")
    return best


print(nearest_neighbour(items))
print(goal(items, weight))
print(random_solution(items, 5))
print(hill_climbing(items, 10, 5))
print(simulated_annealing(items, 5))
print(tabu_search(items, 5, iterations=50, tabu_size=5))
