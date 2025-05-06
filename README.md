# Knapsack Problem 🎒

The Knapsack Problem is a classic combinatorial optimization problem.
It models a situation where you must choose a subset of items to maximize the total value without exceeding a weight limit.

This project focuses on solving the classic **Knapsack Problem** using various metaheuristic and custom approaches.  
It serves both as a learning exercise in optimization algorithms and as a practical comparison of different solution strategies.

## ✨ Implemented Methods:

- **Custom Algorithm**  
  A handcrafted algorithm based on greedy strategies.
  

- **Random Solution**  
  Generates random feasible solutions to serve as a baseline for comparison.


- **Brute-force Search**  
  Exhaustively checks all possible item combinations to find the optimal solution.  
  Guarantees the best result, but becomes computationally infeasible for larger item sets due to exponential time complexity.
  

- **Hill Climbing**  
  Starts from an initial solution and iteratively makes small improvements to reach a local optimum.
  

- **Simulated Annealing**

  A probabilistic metaheuristic that explores the solution space by occasionally accepting worse solutions, 
  allowing it to escape local optima. Gradually reduces its acceptance rate by lowering a "temperature" 
  parameter over time.


- **Tabu Search**  
  A local search metaheuristic that uses memory structures to avoid revisiting recent solutions (tabu list).  
  It explores neighboring solutions while keeping track of recently visited states to escape local optima.  
  Optionally supports backtracking to the last promising solution if no valid neighbors are found.

## 🧠 Project Focus

- Experiment with different metaheuristic optimization techniques
- Understand trade-offs between exploration and exploitation
- Analyze performance and solution quality across multiple approaches
