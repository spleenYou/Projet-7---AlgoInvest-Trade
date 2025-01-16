import csv
from itertools import combinations
import time


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


def calculate_percent(combination):
    return sum(round((action["profit"]/action["cost"]) - 1, 2) * 100 for action in combination)


def calculate_cost(combination):
    return sum(action["cost"] for action in combination)


def calculate_profit(combination):
    return sum(action["cost"] * (1 + (action["profit"] / 100)) for action in combination)


def calcul_limit(actions, MAX_EXPENSE):
    total = 0
    loop = 0
    while total <= MAX_EXPENSE:
        total += actions[loop]["cost"]
        loop += 1
    return loop - 1


def bruteforce(actions, MAX_EXPENSE):
    actions = sorted(actions, key=lambda x: x["profit"]/x["cost"])
    limit = calcul_limit(actions, MAX_EXPENSE)
    bestProfit = 0
    bestCombination = ()
    for combination in combinations(actions, limit):
        cost = calculate_cost(combination)
        if cost <= MAX_EXPENSE:
            profitCost = calculate_profit(combination)
            profit = profitCost - cost
            if profit > bestProfit:
                bestProfit = profit
                bestCombination = combination
    return bestCombination


if __name__ == "__main__":
    MAX_EXPENSE = 500
    start = time.time()
    actions = readFile()
    best = bruteforce(actions, MAX_EXPENSE)
    print(f"Temps d'éxecution : {round(time.time() - start, 2)}")
    cost = calculate_cost(best)
    profit = calculate_profit(best)
    # for action in best:
    #     print(f"{action['name']} pour un prix de {action['cost']}€ avec un profit de {action['profit']}%")
    print(f"le cout total est de {cost}€ "
          f"pour un profit de {round(profit, 2)}€ "
          f"soit {round((profit/cost) - 1, 2) * 100}% "
          f"soit {round(profit - cost, 2)}€")