import csv
import time
import psutil
import os


def readFile(filename):
    """
    Read the csv file with all actions

    Args:
        filename (str): Name of the csv file
    Returns:
        tab (list) : List of all actions
    """
    tab = []
    with open(f"data/{filename}.csv") as csv_file:
        # Skip the first line (name of the column)
        next(csv_file)
        # Read the rest of the csv_file delimit by ','
        csv_data = csv.reader(csv_file, delimiter=",")
        # Create a list of dicts
        for data in csv_data:
            cost = float(data[1])
            if cost > 0:
                tab.append({
                    "name": data[0],
                    "cost": cost,
                    "profit": cost * (1 + float(data[2].replace("%", ""))/100)
                })
    return tab


def execution_information(func):
    "Decorative function for obtaining information about execution"
    def wrapper(*args, **kwargs):
        # Get the process pid
        process = psutil.Process(os.getpid())

        # Get the USS memory before the function
        memory_before = process.memory_full_info().uss

        # Get the time before the function
        start_time = time.time()

        result = func(*args, **kwargs)

        # Get the time after the function
        stop_time = time.time()

        # Get the USS memory after the function
        memory_after = process.memory_full_info().uss

        # Convert the execution time in ms
        print(f"Temps d'éxecution : {(stop_time - start_time) * 1000:.2f}ms")

        # Convert the use memory in KB
        memory_usage_mb = (memory_after - memory_before) / 1024
        print(f"Utilisation de la mémoire : {memory_usage_mb:.2f} KB")
        return result
    return wrapper


def somme(item, tab, x=None):
    if x is None:
        x = {item: 0}
    return float(sum(x[item] for x in tab) + x[item])


def sac_a_dos(poids_max, tab, result):
    if len(tab) == 0:
        return result
    x = tab.pop()
    n = len(tab)
    rent1 = somme("profit", result[0][n + 1], x)
    rent2 = somme("profit", result[1][n + 1])
    if rent1 > rent2:
        poids1 = somme("cost", result[0][n + 1], x)
        if poids1 <= poids_max:
            result[1][n] = result[0][n + 1].copy()
            result[1][n].append(x)
        else:
            result[1][n] = result[1][n + 1].copy()
    else:
        result[1][n] = result[1][n + 1]
    return sac_a_dos(poids_max, tab, result)


@execution_information
def optimized(MAX_EXPENSE, actions):
    """
    Find the best combination with a solution based on knapsack solution

    Args:
        actions (list): list of all actions
        MAX_EXPENSE (int): Maximum amount to spend

    Returns:
        best_combination (tuple): combination with the best profit
    """
    # Find the number of actions
    n = len(actions)
    actions = sorted(actions, key=lambda x: x["cost"]/x["profit"], reverse=True)
    tab = [[[{"name": None, "cost": 0, "profit": 0}]] * (n + 1)] * 2
    for i in range(0, n):
        tab[0] = tab[1].copy()
        tab = sac_a_dos(MAX_EXPENSE, actions.copy(), tab)
    return tab[1][0]


if __name__ == "__main__":
    # Spending limit
    MAX_EXPENSE = 500
    # Read the file
    tab_actions = readFile("dataset2")
    # Find the best combination
    best_combination = optimized(MAX_EXPENSE, tab_actions)
    # Show actions details
    for action in best_combination:
        if action["name"] is not None:
            print(f"{action['name']} pour un prix de {action['cost']}€ avec un profit de {action['profit']:.2f}€")
    # Show the total
    cost = somme("cost", best_combination)
    profit = somme("profit", best_combination)
    print(f"le cout total est de {cost}€ "
          f"pour un profit de {profit-cost:.2f}€ "
          f"soit {((profit/cost) - 1) * 100:.2f}%")
