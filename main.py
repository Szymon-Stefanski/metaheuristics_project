import random


class Knapsack():
    def __init__(self, arrays=None):
        if arrays is None:
            self.arrays = []
        else:
            self.arrays = arrays

        self.bag = []

        if len(self.arrays) < 1:
            option = None
            while option != 3:
                option = input("\nChoose an option: :"
                               "\n1. Add item."
                               "\n2. Show items."
                               "\n3. Complete task.\n")
                if option == "1":
                    name = input("Insert item's name:")
                    price = input("Insert item's price:")
                    weight = input("Insert item's weight:")
                    self.arrays.append({"name": name, "price": int(price), "weight": int(weight)})
                elif option == "2":
                    if len(self.arrays) > 0:
                        for item in self.arrays:
                            print(item)
                    else:
                        print("There is no items!")
                elif option == "3":
                    break
                else:
                    print("Invalid option! Please try again!")
                    continue

    def goal(self, limit):
        permuts = self.arrays.copy()
        for i in range(len(permuts)):
            if permuts[i].get("weight") == limit:
                self.bag.append(permuts[i])
                permuts.remove(permuts[i])
                self.bag.sort(key=lambda x: x["price"], reverse=True)

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
                self.bag.append(permuts[n])

        target = [dict(t) for t in {tuple(d.items()) for d in self.bag}]
        target.sort(key=lambda x: x["price"], reverse=True)


        for m in range(len(target) - 1, -1, -1):
            if target[m].get("price") < target[0].get("price"):
                del target[m]

        print("\nKnapsack possible items: ")
        return print(target)


    def nearest_neighbour(self):
        print("\nNearest neighbours of items in goods:")
        return [self.arrays[i].get("name") + "," + self.arrays[i + 1].get("name") for i in range(len(self.arrays) - 1)]


    def random_solution(self):
        knapsack_random = []
        new_array = self.arrays.copy()
        for i in range(len(new_array)):
            new_array[i].update({"price" : int(random.random()*100)})
            new_array[i].update({"weight" : int(random.random()*100)})
        result = self.arrays.goal(new_array, knapsack_random, int(random.random() * 100))
        print("Random solution:")
        return result


knapsack = Knapsack()
knapsack.goal(2)
