import random


def goal(arrays, target, limit):
    permuts = arrays.copy()
    for i in range(len(permuts)):
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

    print("\nKnapsack possible items: ")
    return target


def nearest_neighbour(arr):
    print("\nNearest neighbours of items in goods:")
    return [arr[i].get("name") + "," + arr[i + 1].get("name") for i in range(len(arr) - 1)]


def random_solution(array):
    knapsack_random = []
    new_array = array.copy()
    for i in range(len(new_array)):
        new_array[i].update({"price" : int(random.random()*100)})
        new_array[i].update({"weight" : int(random.random()*100)})
    result = goal(new_array, knapsack_random, int(random.random() * 100))
    print("Random solution:")
    return result


goods = [{ "name" : "guitar", "price" : 500, "weight" : 4},
         { "name" : "violin", "price" : 900, "weight" : 2},
         { "name" : "monitor", "price" : 1000, "weight" : 3},
         { "name" : "laptop", "price" : 1500, "weight" : 4},
         { "name" : "watch", "price" : 700, "weight" : 1},
         { "name" : "phone", "price" : 600, "weight" : 1},
         ]


knapsack = []


print(nearest_neighbour(goods))
print(goal(goods, knapsack,3))
print(random_solution(goods))
