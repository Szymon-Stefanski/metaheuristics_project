
goods = [{ "name" : "guitar", "price" : 500, "weight" : 4},
         { "name" : "violin", "price" : 900, "weight" : 2},
         { "name" : "monitor", "price" : 1000, "weight" : 3},
         { "name" : "laptop", "price" : 1500, "weight" : 4},
         { "name" : "watch", "price" : 700, "weight" : 1},
         { "name" : "phone", "price" : 600, "weight" : 1},
         ]

knapsack = []


def goal(arrays, limit):
    for array in arrays:
        if array.get("weight") == limit:
            knapsack.append(array)
        else:
            for i in range(len(goods)):
                for j in range(len(goods)):
                    if i != j:
                        if goods[i].get("weight") + goods[j].get("weight") <= limit:
                            knapsack.append({"name" : goods[i].get("name") + " " + goods[j].get("name"),
                                             "price" : goods[i].get("price") + goods[j].get("price"),
                                             "weight" : goods[i].get("weight") + goods[j].get("weight")})

    knapsack.sort(key=lambda x: x["price"], reverse=True)

    return knapsack


def nearest_neighbour(arr):
    return [arr[i].get("name") + "," + arr[i + 1].get("name") for i in range(len(arr) - 1)]


def random_solution(arr):
    return 0


print(goal(goods,4))
print(nearest_neighbour(goods))
