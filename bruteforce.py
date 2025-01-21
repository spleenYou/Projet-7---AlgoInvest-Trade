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


# fonction de décoration
def execution_information(func):
    def wrapper(*args, **kwargs):
        # Récupére le pid du process en cours
        process = psutil.Process(os.getpid())

        memory_before = process.memory_full_info().rss

        # Récupération de l'heure au démarrage
        start_time = time.time()

        result = func(*args, **kwargs)

        # Récupération de l'heure d'arrêt
        stop_time = time.time()

        memory_after = process.memory_full_info().rss

        # Ecriture du temps d'éxecution en milliseconde
        print(f"Temps d'éxecution : {(stop_time - start_time) * 1000:.2f}ms")
        # Convertir en mégaoctets pour une lecture plus facile
        memory_usage_mb = (memory_after - memory_before) / 1024 / 1024
        print(f"Utilisation de la mémoire : {memory_usage_mb:.2f} MB")
        return result
    return wrapper


@execution_information
def bruteforce(actions, MAX_EXPENSE):
    best_profit = 0
    best_combination = ()

    # Calcul du nombre d'actions
    tabLen = len(actions)
    # Calcul du meilleur profit pour chaque combinaisons d'actions de l longueur
    for length in range(1, tabLen):
        for combination in combinations(actions, length):
            cost = sum_total_cost(combination)
            if cost <= MAX_EXPENSE:
                value = sum_total_value_after_2_year(combination)
                profit = value - cost
                if profit > best_profit:
                    best_profit = profit
                    best_combination = combination
    return best_combination


if __name__ == "__main__":
    # Dépense maximum pour le client
    MAX_EXPENSE = 500
    # Lecture du fichier
    actions = readFile()
    # Calcul de la meilleure combinaison
    best_combination = bruteforce(actions, MAX_EXPENSE)
    # Calcul du cout
    cost = sum_total_cost(best_combination)
    # Calcul du profit
    profit = sum_total_value_after_2_year(best_combination)
    # Affichage des actions à acheter
    for action in best_combination:
        print(f"{action['name']} pour un prix de {action['cost']}€ avec un profit de {action['value_after']:.2f}%")
    # Affichage du global
    print(f"le cout total est de {cost}€ "
          f"pour un profit de {profit:.2f}€ "
          f"soit {((profit/cost - 1) * 100):.2f}%")
