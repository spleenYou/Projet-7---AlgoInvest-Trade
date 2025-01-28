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
            if cost >= 1:
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


def somme(item, tab):
    return float(sum(x[item] for x in tab if x["name"] is not None))


def sac_a_dos(MAX_EXPENSE, actions, list_actions):
    n = len(actions)
    if n == 0:
        return list_actions
    liste1 = list_actions.copy()
    liste1.append(actions.pop())
    profit_with_x = somme("profit", liste1)
    profit = somme("profit", list_actions)
    if profit_with_x > profit:
        cost = somme("cost", liste1)
        if cost <= MAX_EXPENSE:
            list_actions = liste1.copy()
    return sac_a_dos(MAX_EXPENSE, actions, list_actions)


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
    actions = sorted(actions, key=lambda x: x["profit"]/x["cost"])
    list0 = [{"name": None, "cost": 0, "profit": 0}]
    list1 = [{"name": None, "cost": 1, "profit": 0}]
    while list0 != list1:
        list0 = list1.copy()
        list1 = sac_a_dos(MAX_EXPENSE, actions.copy(), list0)
    return list1


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
    print(f"le cout total est de {cost:.2f}€ "
          f"pour un profit de {profit-cost:.2f}€ "
          f"soit {((profit/cost) - 1) * 100:.2f}%")
