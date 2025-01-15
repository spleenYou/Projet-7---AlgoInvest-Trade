import csv
from itertools import combinations

actions = []
MAX_EXPENSE = 500


def readFile():
    with open("data/Liste actions.csv") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=",")
        for data in csv_data:
            try:
                int(data[1])
                actions.append({
                    "name": data[0],
                    "cost": int(data[1]),
                    "profit": int(data[2].replace("%", ""))
                })
            except ValueError:
                None


def calculate_cost(combination):
    cost = 0
    for action in combination:
        cost = cost + action["cost"]
    return cost


def calculate_profit(combination):
    profit = 0
    for action in combination:
        profit = profit + (action["cost"] * (1 + (action["profit"] / 100)))
    return profit


def bruteforce():
    tabLen = len(actions)
    bestProfit = 0
    bestCombination = ()
    for r in range(tabLen - 1):
        for combination in combinations(actions, r):
            cost = calculate_cost(combination)
            profit = calculate_profit(combination)
            if cost <= MAX_EXPENSE and profit > bestProfit:
                bestProfit = profit
                bestCombination = combination
    return bestCombination


if __name__ == "__main__":
    readFile()
    best = bruteforce()
    cost = calculate_cost(best)
    profit = calculate_profit(best)
    print(f"le cout est de {cost}, le profit de {profit}")
    print(best)
