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
            cost = float(data[1]) * 100
            if cost > 0:
                tab.append({
                    "name": data[0],
                    "cost": int(cost),
                    "profit": (cost * (1 + float(data[2].replace("%", ""))/100) - cost)/100
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

    # actions = list(action for action in actions if action["profit"] > 0)
    # Dispatch actions's dict in list
    costs = list(action["cost"] for action in actions)
    profits = list(action["profit"] for action in actions)
    names = list(action["name"] for action in actions)
    # Find the number of actions
    n = len(costs)
    MAX_EXPENSE = MAX_EXPENSE * 100
    # Create a table in two dimensions : MAX_EXPENSE by number of actions
    profits_items = [[0 for _ in range(MAX_EXPENSE + 1)] for _ in range(2)]

    # Create a similar table but for action's name
    selected_items = [[[] for _ in range(MAX_EXPENSE + 1)] for _ in range(2)]

    # Fill tables
    for i in range(1, n + 1):
        for j in range(1, MAX_EXPENSE + 1):
            # If cost can be included
            if costs[i-1] <= j:
                # Get profit more profit in the previous dimension
                new_profit = profits[i-1] + profits_items[0][j-costs[i-1]]
                # Get the previous profit
                previous_profit = profits_items[0][j]

                # Maximise profit and keep names
                if new_profit > previous_profit:
                    profits_items[1][j] = new_profit
                    selected_items[1][j] = selected_items[0][j-costs[i-1]] + [names[i-1]]
                else:
                    profits_items[1][j] = previous_profit
                    selected_items[1][j] = selected_items[0][j]
            else:
                # If cost cannot be included
                profits_items[1][j] = profits_items[0][j]
                selected_items[1][j] = selected_items[0][j]
        # Copy row 1 in row 0 for noth tables
        profits_items[0] = profits_items[1].copy()
        selected_items[0] = selected_items[1].copy()
    # Return the best combination (last case)
    return selected_items[1][MAX_EXPENSE]


if __name__ == "__main__":
    # Spending limit
    MAX_EXPENSE = 500
    # Read the file
    actions = readFile("dataset2")
    # Find the best combination
    best_combination = optimized(MAX_EXPENSE, actions)
    # Show actions details
    cost = 0
    profit = 0
    for action in actions:
        if action["name"] in best_combination:
            cost += action["cost"] / 100
            profit += action["profit"]
            print(f"{action['name']} pour un prix de {action['cost'] / 100}€ avec un profit de {action['profit']:.2f}%")
    # Show the total
    print(f"le cout total est de {cost}€ "
          f"pour un profit de {profit:.2f}€ "
          f"soit {(profit/cost) * 100:.2f}%")
