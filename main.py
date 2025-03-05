

def goal(arrays, target, limit):
    for i in range(len(arrays)):
        arrays[i]['name'] = " ".join(sorted(arrays[i]['name'].split()))

        if arrays[i].get("weight") == limit:
            target.append(arrays[i])
            arrays.remove(arrays[i])
            target.sort(key=lambda x: x["price"], reverse=True)

        elif arrays[i].get("weight") < limit:
            for j in range(len(arrays)):
                while (arrays[j].get("weight") + arrays[i].get("weight")) <= limit:
                    if arrays[i].get("name") not in arrays[j].get("name"):
                        arrays.append({"name" : arrays[i].get("name") + " " + arrays[j].get("name"),
                                      "price" : arrays[i].get("price") + arrays[j].get("price"),
                                      "weight" : arrays[i].get("weight") + arrays[j].get("weight")})
                    break

    arrays.sort(key=lambda x: x["price"], reverse=True)

    for n in range(len(arrays) - 1, -1, -1):
        arrays[n]['name'] = " ".join(sorted(arrays[n]['name'].split()))
        if arrays[n].get("weight") != limit:
            del arrays[n]
        else:
            target.append(arrays[n])

    target = [dict(t) for t in {tuple(d.items()) for d in target}]
    target.sort(key=lambda x: x["price"], reverse=True)


    for m in range(len(target) - 1, -1, -1):
        if target[m].get("price") < target[0].get("price"):
            del target[m]

    print("\nKnapsack possible items: ")
    return target


def nearest_neighbour(arr):
    print("\nNearest neighbour:")
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


print(nearest_neighbour(goods))
print(goal(goods, knapsack,3))
