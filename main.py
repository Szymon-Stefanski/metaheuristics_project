

def goal(arrays, target, limit):
    for i in range(len(arrays)):
        if arrays[i].get("weight") == limit:
            target.append(arrays[i])
            arrays.remove(arrays[i])
            target.sort(key=lambda x: x["price"], reverse=True)
        elif arrays[i].get("weight") < limit:
            for j in range(len(arrays)):
                while (arrays[j].get("weight") + arrays[i].get("weight")) <= limit:
                    if (arrays[j].get("name") not in arrays[i].get("name")) and (arrays[i].get("name") not in arrays[j].get("name")):
                        arrays.append({"name" : arrays[j].get("name") + " " + arrays[i].get("name"),
                                      "price" : arrays[j].get("price") + arrays[i].get("price"),
                                      "weight" : arrays[j].get("weight") + arrays[i].get("weight")})
                    break

    arrays.sort(key=lambda x: x["price"], reverse=True)

    for n in range(len(arrays) - 1, -1, -1):
        if arrays[n].get("weight") != limit:
            del arrays[n]
        else:
            if arrays[n].get("name") in arrays[n].get("name"):
                target.append({"name": arrays[n].get("name"),
                               "price": arrays[n].get("price"),
                               "weight": arrays[n].get("weight")})

    target.sort(key=lambda x: x["price"], reverse=True)
    return target


def nearest_neighbour(arr):
    return [arr[i].get("name") + "," + arr[i + 1].get("name") for i in range(len(arr) - 1)]


def random_solution(arr):
    return 0


goods = [{ "name" : "guitar", "price" : 500, "weight" : 4},
         { "name" : "violin", "price" : 900, "weight" : 2},
         { "name" : "monitor", "price" : 1000, "weight" : 3},
         { "name" : "laptop", "price" : 1500, "weight" : 4},
         { "name" : "watch", "price" : 700, "weight" : 1},
         { "name" : "phone", "price" : 600, "weight" : 1},
         ]


knapsack = []

print(goal(goods, knapsack,3))
#print(nearest_neighbour(goods))
