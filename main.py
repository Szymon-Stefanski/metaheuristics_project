import random
import csv


goods = [{"name" : "guitar", "price" : 500, "weight" : 3},
         {"name" : "laptop", "price" : 1000, "weight" : 2},
         {"name" : "phone", "price" : 500, "weight" : 1},
         {"name" : "tablet", "price" : 1000, "weight" : 1},
         {"name" : "tv", "price" : 3000, "weight" : 5}]

weight = 4

def no_items(array):
    if array is None:
        option = None
        while option != 3:
            option = input("\nChoose an option: :"
                           "\n0. Import data from a file (.csv)"
                           "\n1. Add item."
                           "\n2. Show items."
                           "\n3. Complete task.\n")

            match option:
                case 0:
                    bag = []
                    path = input("\nEnter path to file: ")
                    with open(path, "r") as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            bag.append({
                                "name": row["name"],
                                "price": int(row["price"]),
                                "weight": int(row["weight"]),
                            })
                    arrays = bag.copy()

                case 1:
                    name = input("Insert item's name:")
                    price = input("Insert item's price:")
                    weight = input("Insert item's weight:")
                    arrays.append({"name": name, "price": int(price), "weight": int(weight)})

                case 2:
                    if len(arrays) > 0:
                        for item in arrays:
                            print(item)
                    else:
                        print("There is no items!")

                case 3:
                    break

                case _:
                    print("Invalid option! Please try again!")
                    continue
        return array


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


def nearest_neighbour(array=None):
    if array is None:
        no_items(array)

    neighbours = []

    for i in range(len(array)):
        neighbour = array.copy()
        neighbour[(i+1) % len(array)],neighbour[i] = array[i],array[(i+1) % len(array)]
        neighbours.append(neighbour)

    return neighbours



def random_solution(array, limit):
    if array is None:
        raise ValueError("Item list cannot be None")

    print("\n")

    knapsack = []
    total_weight = 0

    current = array.copy()
    random.shuffle(current)

    for item in current:
        knapsack.append({"name" : item["name"], "price" : item["price"], "weight" : item["weight"]})
        total_weight += item["weight"]

        if total_weight >= limit:
            break

    print(f"Random solution for weight limit = {limit}:")

    return knapsack



# In progress
"""
def hill_climbing(array, iterations):
    current = random_solution(array)
    neighbours = nearest_neighbour(array)
    best_neighbour = neighbours[0]

    print("\nHill climbing algorithm result:")
    return best_neighbour

"""


print(nearest_neighbour(goods))
print(goal(goods, weight))
print(random_solution(goods, 4))
#print(hill_climbing(goods, 3))
