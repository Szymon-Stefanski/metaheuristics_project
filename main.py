
goods = [{ "name" : "guitar", "price" : 500, "weight" : 4},
         { "name" : "violin", "price" : 900, "weight" : 1},
         { "name" : "monitor", "price" : 1000, "weight" : 3},
         { "name" : "laptop", "price" : 1500, "weight" : 4},
         { "name" : "watch", "price" : 700, "weight" : 1},
         { "name" : "phone", "price" : 600, "weight" : 2},
         ]

max = 4


def goal(arr, limit):
    for i in range(len(arr)-1):
        if arr[i].get("weight") <= limit:
            return [arr[i].get("price") + arr[i].get("weight") for i in range(len(arr)-1)]


def nearest_neighbour(arr):
    return [arr[i].get("name") + "," + arr[i + 1].get("name") for i in range(len(arr) - 1)]



def random_solution(arr):
    return 0



print(goal(goods,max))
print(nearest_neighbour(goods))

