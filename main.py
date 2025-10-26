import csv
import argparse

from brute_force import brute_force
from genetic_algorithm import genetic_algorithm
from hill_climbing_deterministic import hill_climbing_deterministic
from hill_climbing_stochastic import hill_climbing_stochastic
from simulated_annealing import simulated_annealing
from tabu_search import tabu_search
from utils import generate_neighbours, random_solution


def read_items(file):
    reader = csv.DictReader(file)
    return [{"name": r["name"], "weight": int(r["weight"]), "price": int(r["price"])} for r in reader]


def main():
    parser = argparse.ArgumentParser(description="Knapsack optimization algorithms")

    parser.add_argument("--alg", type=str, required=True, choices=[
        "generate_neighbours", "random_solution", "brute_force",
        "hill_climbing_deterministic", "hill_climbing_stochastic",
        "simulated_annealing", "tabu_search", "genetic_algorithm"
    ], help="Choose an algorithm")

    parser.add_argument("--filename", type=str, required=True, help="Load a CSV file with items")
    parser.add_argument("--limit", type=int, required=True, help="Weight limit")
    parser.add_argument("--iterations", type=int, default=100)

    parser.add_argument("--tabu_size", type=int, default=10)
    parser.add_argument("--rollback", action="store_true")

    parser.add_argument("--temp", type=float, default=100.0)
    parser.add_argument("--cooling", type=float, default=0.95)
    parser.add_argument("--min_temp", type=float, default=0.01)

    parser.add_argument("--population_size", type=int, default=20)
    parser.add_argument("--generations", type=int, default=100)
    parser.add_argument("--elitism", action="store_true")

    args = parser.parse_args()

    if args.filename == "test":
        items = [
            {"name": "Laptop", "weight": 3, "price": 4000},
            {"name": "Smartphone", "weight": 1, "price": 2500},
            {"name": "Headphones", "weight": 1, "price": 800},
            {"name": "Camera", "weight": 2, "price": 3200},
        ]
    else:
        with open(args.filename, newline='') as f:
            items = read_items(f)

    if args.alg == "generate_neighbours":
        result = generate_neighbours(items)
    elif args.alg == "random_solution":
        result = random_solution(items, args.limit)
    elif args.alg == "brute_force":
        result = brute_force(items, args.limit)
    elif args.alg == "hill_climbing_deterministic":
        result = hill_climbing_deterministic(items, args.iterations, args.limit)
    elif args.alg == "hill_climbing_stochastic":
        result = hill_climbing_stochastic(items, args.iterations, args.limit)
    elif args.alg == "simulated_annealing":
        result = simulated_annealing(items, args.limit, args.temp, args.cooling, args.min_temp)
    elif args.alg == "tabu_search":
        result = tabu_search(items, args.limit, args.iterations, args.tabu_size, args.rollback)
    elif args.alg == "genetic_algorithm":
        result = genetic_algorithm(items, args.limit, args.population_size, args.generations, args.elitism)
    else:
        parser.error(f"Unknown algorithm: {args.alg}")

    print(f"Result: {result}")


if __name__ == "__main__":
    main()
