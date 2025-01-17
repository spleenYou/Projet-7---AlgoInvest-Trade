import csv
from itertools import combinations
import time


def readFile():
    tab = []
    with open("data/Liste actions.csv") as csv_file:
        next(csv_file)
        csv_data = csv.reader(csv_file, delimiter=",")
        for data in csv_data:
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


def calcul_length_of_combination(actions, MAX_EXPENSE):
    total = 0
    nb_of_actions = 0
    while total <= MAX_EXPENSE:
        total += actions[nb_of_actions]["cost"]
        nb_of_actions += 1
    return nb_of_actions - 1


def optimzed(actions, MAX_EXPENSE):
    actions = sorted(actions, key=lambda x: x["profit"]/x["cost"])
    length_of_combination = calcul_length_of_combination(actions, MAX_EXPENSE)
    best_profit = 0
    best_combination = ()
    for combination in combinations(actions, length_of_combination):
        cost = sum_total_cost(combination)
        if cost <= MAX_EXPENSE:
            profit_cost = sum_total_profit(combination)
            profit = profit_cost - cost
            if profit > best_profit:
                best_profit = profit
                best_combination = combination
    return best_combination


if __name__ == "__main__":
    MAX_EXPENSE = 500
    start = time.time()
    actions = readFile()
    best = optimzed(actions, MAX_EXPENSE)
    print(f"Temps d'éxecution : {round(time.time() - start, 2)}")
    cost = sum_total_cost(best)
    profit = sum_total_profit(best)
    # for action in best:
    #     print(f"{action['name']} pour un prix de {action['cost']}€ avec un profit de {action['profit']}%")
    print(f"le cout total est de {cost}€ "
          f"pour un profit de {round(profit, 2)}€ "
          f"soit {round((profit/cost) - 1, 2) * 100}% "
          f"soit {round(profit - cost, 2)}€")
