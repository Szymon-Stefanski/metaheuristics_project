# Knapsack Problem

The Knapsack Problem is a classic combinatorial optimization problem.
It models a situation where you must choose a subset of items to maximize the total value without exceeding a weight limit.

This project focuses on solving the classic **Knapsack Problem** using various metaheuristic and custom approaches.  
It serves both as a learning exercise in optimization algorithms and as a practical comparison of different solution strategies.

---

## Implemented Methods

- **Random Solution**  
  Generates random feasible solutions to serve as a baseline for comparison.


- **Brute-force Search**  
  Exhaustively checks all possible item combinations to find the optimal solution.  
  Guarantees the best result, but becomes computationally infeasible for larger item sets due to exponential time complexity.


- **Hill Climbing (Deterministic & Stochastic)**  
  Starts from an initial solution and iteratively makes small improvements to reach a local optimum.  
  The stochastic variant introduces randomness to escape shallow local optima.


- **Simulated Annealing**  
  A probabilistic metaheuristic that explores the solution space by occasionally accepting worse solutions.  
  Gradually reduces this acceptance probability using a cooling schedule based on temperature.


- **Tabu Search**  
  A local search algorithm that uses a tabu list (short-term memory) to prevent cycling and promote exploration.  
  Includes optional rollback to the last promising solution if stuck in a local minimum.


- **Genetic Algorithm**  
  A population-based metaheuristic inspired by biological evolution.  
  Applies crossover, mutation, and elitism over generations to evolve better solutions.

---

## Key Features

- **Multiple input modes**:  
  - CSV file using `--filename`  
  - Directly via Python list using `--list` (no file needed)

- **Goal function with penalty support**:  
  Automatically evaluates solution value and optionally penalizes overweight solutions using a configurable `--penalty_factor`.

- **Modular and extensible design**:  
  Each algorithm is implemented in its own function, making it easy to test, modify, or extend.

- **Command-line Interface (CLI)**:  
  Run any algorithm directly with custom parameters:
  
  ```bash
  python main.py --alg random_solution --filename objects.csv --limit 10
  python main.py --alg genetic_algorithm --list items --limit 15 --generations 100 --population_size 30 --elitism

