
goods = [{ "name" : "guitar", "price" : 500, "weight" : 4},
         { "name" : "violin", "price" : 900, "weight" : 1},
         { "name" : "monitor", "price" : 1000, "weight" : 3},
         { "name" : "laptop", "price" : 1500, "weight" : 4},
         { "name" : "watch", "price" : 700, "weight" : 1},
         { "name" : "phone", "price" : 600, "weight" : 2},
         ]

max = 4

permuts = []

knapsack = []

def goal(arr, limit):
    for i in range(len(arr)):
        for j in range(len(arr)-1):
            if (arr[i].get("name") != arr[j+1].get("name")) and (arr[i].get("weight") + arr[j+1].get("weight")) <= limit:
                permuts.append({"name":arr[i].get("name") + " , " + arr[j+1].get("name"),
                                "price":arr[i].get("price") + arr[j+1].get("price"),
                                "weight":arr[i].get("weight") + arr[j+1].get("weight")})

    return permuts


def nearest_neighbour(arr):
    return [arr[i].get("name") + "," + arr[i + 1].get("name") for i in range(len(arr) - 1)]



def random_solution(arr):
    return 0


print(goal(goods,max))
#print(nearest_neighbour(goods))

