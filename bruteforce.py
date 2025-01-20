import csv
from itertools import combinations
import time
import os
import psutil


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
                "value_after": int(data[1]) * (1 + int(data[2].replace("%", "")) / 100)
            })
    return tab


def sum_total_cost(combination):
    return sum(action["cost"] for action in combination)


def sum_total_value_after_2_year(combination):
    return sum(action["value_after"] for action in combination)


def bruteforce(actions, MAX_EXPENSE):
    tabLen = len(actions)
    best_profit = 0
    best_combination = ()
    for r in range(1, tabLen):
        for combination in combinations(actions, r):
            cost = sum_total_cost(combination)
            if cost <= MAX_EXPENSE:
                value = sum_total_value_after_2_year(combination)
                profit = value - cost
                if profit > best_profit:
                    best_profit = profit
                    best_combination = combination
    return best_combination


if __name__ == "__main__":
    MAX_EXPENSE = 500
    start = time.time()
    actions = readFile()
    best = bruteforce(actions, MAX_EXPENSE)
    print(f"Temps d'éxecution : {round(time.time() - start, 2)}")
    cost = sum_total_cost(best)
    profit = sum_total_value_after_2_year(best)
    # for action in best:
    #     print(f"{action['name']} pour un prix de {action['cost']}€ avec un profit de {action['value_after']}%")
    print(f"le cout total est de {cost}€ "
          f"pour un profit de {profit:.2f}€ "
          f"soit {(profit/cost) * 100:.2f}%")
    # Obtenir le processus actuel
    process = psutil.Process(os.getpid())
    # Obtenir l'utilisation de la mémoire en octets
    memory_usage = process.memory_info().rss
    # Convertir en mégaoctets pour une lecture plus facile
    memory_usage_mb = memory_usage / 1024 / 1024
    print(f"Utilisation de la mémoire : {memory_usage_mb:.2f} MB")
