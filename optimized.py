import csv
import time
import psutil
import os
from rich.table import Table
from rich.console import Console


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
                    "profit": float(data[2].replace("%", ""))
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


def clear_screen():
    "Clean the console for all os"
    command = "clear"
    if os.name in ("nt", "dos"):
        command = "cls"
    os.system(command)


def show_information(filename, actions, best_combination):
    console = Console()
    costs = cal_cost(best_combination)
    profits = cal_profit(best_combination)

    table = Table(title=f"Fichier : {filename}.csv", show_lines=True)
    table.add_column("Nom de l'action", justify="center")
    table.add_column("Prix", justify="center")
    table.add_column("Profit", justify="center")
    table.add_column("Ratio", justify="center")

    for action in best_combination:
        if action["name"] != "":
            cost = action['cost']
            profit = cost * (1 + (action['profit'])/100)
            table.add_row(action['name'],
                          f"{cost}€",
                          f"{profit - cost:.2f}€",
                          f"{action['profit']:.2f}%")

    table.add_row("[bold]Total",
                  f"[bold]{costs:.2f}€",
                  f"[bold]{profits - costs:.2f}€",
                  f"[bold]{((profits/costs) - 1) * 100:.2f}%")

    console.print(table)


def cal_profit(tab):
    if isinstance(tab, int):
        return 0
    return float(sum(action["cost"] * (1 + action["profit"]/100) for action in tab))


def cal_cost(tab):
    return float(sum(x["cost"] for x in tab))


def sac_a_dos(MAX_EXPENSE, actions, list_actions):
    n = len(actions)
    if n == 0:
        return list_actions
    new_action = actions.pop()
    if new_action not in list_actions:
        liste1 = list_actions.copy()
        liste1.append(new_action)
        profit_with_x = cal_profit(liste1)
        profit = cal_profit(list_actions)
        if profit_with_x > profit:
            cost = cal_cost(liste1)
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
    actions = sorted(actions, key=lambda x: cal_profit([x])/x["cost"])
    list0 = []
    list1 = [{"name": "", "cost": 0, "profit": 0}]
    while list0 != list1:
        list0 = list1.copy()
        list1 = sac_a_dos(MAX_EXPENSE, actions.copy(), list0)
    return list1


if __name__ == "__main__":
    # Spending limit
    MAX_EXPENSE = 500
    filenames = ["dataset0", "dataset1", "dataset2"]
    stop = False
    while not stop:
        choice = input("Quel jeu de valeurs souhaitez-vous tester ? (0 ou 1 ou 2) (stop pour arrêter) ")
        clear_screen()
        if choice in ["0", "1", "2"]:
            filename = filenames[int(choice)]
            # Read the file
            actions = readFile(filename)
            # Find the best combination
            best_combination = optimized(MAX_EXPENSE, actions)
            # Show information on screen
            show_information(filename, actions, best_combination)
        elif choice == "stop":
            stop = True
