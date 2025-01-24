import csv
from itertools import combinations
import time
import os
import psutil


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
            tab.append({
                "name": data[0],
                "cost": int(data[1]),
                "value_after": int(data[1]) * (1 + int(data[2].replace("%", "")) / 100)
            })
    return tab


def sum_total_cost(combination):
    "Return the sum of the cost of all actions in combination"
    return sum(action["cost"] for action in combination)


def sum_total_value_after_2_year(combination):
    "Return the sum of the value after 2 years of all actions in combination"
    return sum(action["value_after"] for action in combination)


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


@execution_information
def bruteforce(actions, MAX_EXPENSE):
    """
    Find the best combination in bruteforce way by check the profit makes for all combinations

    Args:
        actions (list): list of all actions
        MAX_EXPENSE (int): Maximum amount to spend

    Returns:
        best_combination (tuple): combination with the best profit
    """

    best_profit = 0
    best_combination = ()

    # Get the number of actions
    tabLen = len(actions)
    # Calculation of the profit for each combination of all length
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
    # Spending limit
    MAX_EXPENSE = 500
    # Read the file
    actions = readFile("Liste actions")
    # Find the best combination
    best_combination = bruteforce(actions, MAX_EXPENSE)
    # Cost calculation
    cost = sum_total_cost(best_combination)
    # Profit calculation
    profit = sum_total_value_after_2_year(best_combination)
    # Show all actions in best combination
    for action in best_combination:
        print(f"{action['name']} pour un prix de {action['cost']}€ avec un profit de {action['value_after']:.2f}%")
    # Show the total
    print(f"le cout total est de {cost}€ "
          f"pour un profit de {profit:.2f}€ "
          f"soit {((profit/cost - 1) * 100):.2f}%")
