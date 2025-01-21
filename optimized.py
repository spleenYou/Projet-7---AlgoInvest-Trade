import csv
import time
import psutil
import os


def readFile():
    tab = []
    with open("data/Liste actions.csv") as csv_file:
        next(csv_file)
        csv_data = csv.reader(csv_file, delimiter=",")
        for data in csv_data:
            tab.append({
                "name": data[0],
                "cost": int(data[1]),
                "profit": int(data[1]) * (1 + int(data[2].replace("%", ""))/100) - int(data[1])
            })
    return tab


# decorator function
def profile(func):
    def wrapper(*args, **kwargs):
        process = psutil.Process(os.getpid())
        mem_before = process.memory_full_info().rss
        result = func(*args, **kwargs)
        mem_after = process.memory_full_info().rss
        print(f"consumed memory 1: {(mem_after - mem_before)/1024/1024}")
        return result
    return wrapper


@profile
def knapSack(MAX_EXPENSE, actions):
    # Création des tableaux de valeurs
    costs = list(action["cost"] for action in actions)
    profits = list(action["profit"] for action in actions)
    names = list(action["name"] for action in actions)

    n = len(costs)
    # Création de la table pour stocker les profits maximaux
    table = [[0 for _ in range(MAX_EXPENSE + 1)] for _ in range(n + 1)]

    # Création d'une table pour suivre les éléments sélectionnés
    selected_items = [[[] for _ in range(MAX_EXPENSE + 1)] for _ in range(n + 1)]

    # Remplissage de la table
    for i in range(1, n + 1):
        for j in range(1, MAX_EXPENSE + 1):
            if costs[i-1] <= j:
                # Calcul du profit si on inclut l'élément actuel
                new_profit = profits[i-1] + table[i-1][j-costs[i-1]]
                old_profit = table[i-1][j]

                # Maximiser le profit et enregistrer les noms correspondants
                if new_profit > old_profit:
                    table[i][j] = new_profit
                    selected_items[i][j] = selected_items[i-1][j-costs[i-1]] + [names[i-1]]
                else:
                    table[i][j] = old_profit
                    selected_items[i][j] = selected_items[i-1][j]
            else:
                # Si l'élément ne peut pas être inclus
                table[i][j] = table[i-1][j]
                selected_items[i][j] = selected_items[i-1][j]
    # Les éléments sélectionnés sont dans selected_items[n][MAX_EXPENSE]
    items_selected = selected_items[n][MAX_EXPENSE]

    return items_selected


if __name__ == "__main__":
    # Obtenir le processus actuel
    process = psutil.Process(os.getpid())
    # Obtenir la ram avant le programme
    memory_before = process.memory_info().rss
    # Dépense maximum pour le client
    MAX_EXPENSE = 500
    # Récupération de l'heure au démarrage
    start_time = time.time()
    # Lecture du fichier
    actions = readFile()
    # Recherche de la liste la plus rentable
    items_selected = knapSack(MAX_EXPENSE, actions)
    # Ecriture du temps d'éxecution
    print(f"Temps d'éxecution : {round(time.time() - start_time, 6)}sec")
    # Calcul du cout total
    cost = sum(action["cost"] for action in actions if action["name"] in items_selected)
    # Calcul du profit
    profit = sum(action["profit"] for action in actions if action["name"] in items_selected)
    # Ecriture de la finalité
    print(f"le cout total est de {cost}€ "
          f"pour un profit de {profit:.2f}€ "
          f"soit {(profit/cost) * 100:.2f}%")
    # Obtenir l'utilisation de la mémoire après
    memory_after = process.memory_info().rss
    # Convertir en mégaoctets pour une lecture plus facile
    memory_usage_mb = (memory_after - memory_before) / 1024 / 1024
    print(f"Utilisation de la mémoire : {memory_usage_mb:.2f} MB")
