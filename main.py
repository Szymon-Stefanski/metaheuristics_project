
goods = [{ "name" : "guitar", "price" : 500, "weight" : 4},
         { "name" : "violin", "price" : 900, "weight" : 2},
         { "name" : "monitor", "price" : 1000, "weight" : 3},
         { "name" : "laptop", "price" : 1500, "weight" : 4},
         { "name" : "watch", "price" : 700, "weight" : 1},
         { "name" : "phone", "price" : 600, "weight" : 1},
         ]


knapsack = []

permutations = []

def goal(arr, limit):
        for i in range(len(arr)):
            if arr[i].get("weight") == limit:
                permutations.append({"name": arr[i].get("name"),
                                 "price": arr[i].get("price"),
                                 "weight": arr[i].get("weight")})
            for j in range(len(arr)):
                if (arr[i].get("name") != arr[j].get("name")) and (arr[i].get("weight") + arr[j].get("weight")) <= limit:
                    permutations.append({"name": arr[i].get("name") + arr[j].get("name"),
                                    "price" : arr[i].get("price") + arr[j].get("price"),
                                    "weight" : arr[i].get("weight") + arr[j].get("weight")})

        for i in range(len(permutations)):
            if permutations[i].get("weight") < limit:
                knapsack.append({"name": permutations[i].get("name"),
                                 "price": permutations[i].get("price"),
                                 "weight": permutations[i].get("weight")})

        return knapsack


def nearest_neighbour(arr):
    return [arr[i].get("name") + "," + arr[i + 1].get("name") for i in range(len(arr) - 1)]



def random_solution(arr):
    return 0


print(goal(goods,5))
#print(nearest_neighbour(goods))

