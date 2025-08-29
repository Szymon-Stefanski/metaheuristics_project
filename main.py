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
