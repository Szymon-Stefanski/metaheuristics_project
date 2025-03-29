import random
import csv
from random import randint


goods = [{"name" : "guitar", "price" : 500, "weight" : 3},
         {"name" : "laptop", "price" : 1000, "weight" : 2},
         {"name" : "phone", "price" : 500, "weight" : 1},
         {"name" : "tablet", "price" : 1000, "weight" : 1}]

knapsack = []
weight = 4

def goal(arrays=None, target=None, limit=None):
    if len(arrays) < 1:
        option=None
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
                    arrays.append({"name" : name, "price" : int(price), "weight" : int(weight)})

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

    permuts = arrays.copy()
    for i in range(len(permuts)-1):
        if permuts[i].get("weight") == limit:
            target.append(permuts[i])
            permuts.remove(permuts[i])
            target.sort(key=lambda x: x["price"], reverse=True)

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
            target.append(permuts[n])

    target = [dict(t) for t in {tuple(d.items()) for d in target}]
    target.sort(key=lambda x: x["price"], reverse=True)


    for m in range(len(target) - 1, -1, -1):
        if target[m].get("price") < target[0].get("price"):
            del target[m]

    print(f"\nKnapsack best possible items configuration with weight limit = {limit} :")
    return target


def nearest_neighbour(arr):
    print("\nItems:")
    print(arr)
    print("\nNearest neighbours of items in goods:")
    return [arr[i].get("name") + "," + arr[i + 1].get("name") for i in range(len(arr) - 1)]


def random_solution(array):
    knapsack_random = []
    new_array = array.copy()
    for i in range(len(new_array)):
        max_weight = randint(1,5)
        new_array[i].update({"price" : round(int(random.randint(100,10000)),-2)})
        new_array[i].update({"weight" : int(random.randint(1,max_weight))})
    result = goal(new_array, knapsack_random, int(random.randint(1,6)))
    print("Random items - random prices and weights: ")
    print(new_array)
    print("Random solution:")
    return result


#Create table with dictionaries for example: x = [{"name":"laptop", "price":3000, "weight":2},
#                                                 {"name":"phone", "price":1500, "weight":1}]
#Create knapsack table - knapsack = []
#
#Set limit for example: weight = 5

print(nearest_neighbour(goods))
print(goal(goods, knapsack, weight))
print(random_solution(goods))
