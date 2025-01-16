import csv
from itertools import combinations
import time

MAX_EXPENSE = 500


def readFile():
    tab = []
    with open("data/Liste actions.csv") as csv_file:
        next(csv_file)
        csv_data = csv.reader(csv_file, delimiter=",")
        for data in csv_data:
            int(data[1])
            tab.append({
                "name": data[0],
                "cost": int(data[1]),
                "profit": int(data[2].replace("%", ""))
            })
    return tab


def sum_total_cost(combination):
    return sum(action["cost"] for action in combination)


def sum_total_profit(combination):
    return sum(action["cost"] * (1 + (action["profit"] / 100)) for action in combination)


def bruteforce(actions):
    tabLen = len(actions)
    bestProfit = 0
    bestCombination = ()
    for r in range(1, tabLen):
        for combination in combinations(actions, r):
            cost = sum_total_cost(combination)
            if cost <= MAX_EXPENSE:
                profitCost = sum_total_profit(combination)
                profit = profitCost - cost
                if profit > bestProfit:
                    bestProfit = profit
                    bestCombination = combination
    return bestCombination


if __name__ == "__main__":
    actions = readFile()
    start = time.time()
    best = bruteforce(actions)
    print(f"Temps d'éxecution : {round(time.time() - start, 2)}")
    cost = sum_total_cost(best)
    profit = sum_total_profit(best)
    for action in best:
        print(f"{action['name']} pour un prix de {action['cost']}€ avec un profit de {action['profit']}%")
    print(f"le cout total est de {cost}€"
          f"pour un profit de {round(profit, 2)}€"
          f"soit {round((profit/cost) - 1, 2) * 100}%"
          f"soit {round(profit - cost, 2)}€")
