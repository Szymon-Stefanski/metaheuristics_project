import random
import csv


items = [{"name" : "guitar", "price" : 500, "weight" : 3},
         {"name" : "laptop", "price" : 1000, "weight" : 2},
         {"name" : "phone", "price" : 500, "weight" : 1},
         {"name" : "tablet", "price" : 1000, "weight" : 1},
         {"name" : "tv", "price" : 3000, "weight" : 5}]

weight = 5


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
        array = no_items(array)

    neighbours = array.copy()

    for i in range(len(array)):
        neighbour = array.copy()
        neighbour[(i+1) % len(array)],neighbour[i] = array[i],array[(i+1) % len(array)]
        neighbours.append(neighbour)

    return neighbours


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



# In progress
"""
def hill_climbing(array, iterations):
    current = random_solution(array)
    neighbours = nearest_neighbour(array)
    best_neighbour = neighbours[0]

    print("\nHill climbing algorithm result:")
    return best_neighbour

"""


print(nearest_neighbour(items))
print(goal(items, weight))
print(random_solution(items, 5))
#print(hill_climbing(items, 3))
