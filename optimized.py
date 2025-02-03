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

        # Convert the use memory in KB
        memory_usage_mb = (memory_after - memory_before) / 1024
        # Convert the execution time in ms
        exectution_time = (stop_time - start_time) * 1000

        # Table creation to shgow information
        console = Console()
        table = Table(title="Informations d'execution", show_lines=True)
        table.add_column("Temps (ms)", justify="center")
        table.add_column("Mémoire utilisée", justify="center")
        table.add_row(f"{exectution_time:.2f}ms", f"{memory_usage_mb:.2f} KB")
        console.print(table)
        return result
    return wrapper


def clear_screen():
    "Clean the console for all os"
    command = "clear"
    if os.name in ("nt", "dos"):
        command = "cls"
    os.system(command)


def show_information(filename, best_combination):
    """
    Displays the actions selected for purchase and the total

    Args:
        filename (str): Name of the file choosen
        best_combination (list): List of the best combination af actions
    """
    console = Console()

    # calculating total costs and profits
    costs = cal_total_cost(best_combination)
    profits = cal_total_profit(best_combination)

    # Table creation for the information
    table = Table(title=f"Fichier : {filename}.csv", show_lines=True)
    table.add_column("Nom de l'action", justify="center")
    table.add_column("Prix", justify="center")
    table.add_column("Profit", justify="center")
    table.add_column("Ratio", justify="center")

    for action in best_combination:
        if action["name"] != "":
            cost = action['cost']
            profit = cost * (action['profit'])/100
            table.add_row(action['name'],
                          f"{cost}€",
                          f"{profit:.2f}€",
                          f"{action['profit']:.2f}%")

    table.add_row("[bold]Total",
                  f"[bold]{costs:.2f}€",
                  f"[bold]{profits - costs:.2f}€",
                  f"[bold]{((profits/costs) - 1) * 100:.2f}%")

    # Display the table
    console.print(table)


def cal_total_profit(actions):
    """
    Calculating the total profit for a list of actions

    Args:
        actions (list): List of actions

    Returns:
        (float): Sum of profit
    """
    return float(sum(action["cost"] * (1 + action["profit"]/100) for action in actions))


def cal_total_cost(actions):
    """
    Calculating the total cost for a list of actions

    Args:
        actions (list): List of actions

    Returns:
        (float): Sum of cost
    """
    return float(sum(x["cost"] for x in actions))


def find_best_combination(MAX_EXPENSE, actions, last_list_actions_found):
    """
    Find the best combination in the list of actions until there is no actions to be added

    Args:
        MAX_EXPENSE (int): Spending limit
        actions (list): List of actions
        last_list_actions_found (list): Last list of actions found

    Returns:
        last_list_actions_found (list): Last list of actions found when no more action to add
    """
    n = len(actions)
    # If no actions to add, return the last list found
    if n == 0:
        return last_list_actions_found
    # Take the last action in the actions list
    new_action = actions.pop()
    # Reject action if already took
    if new_action not in last_list_actions_found:
        # Create the list of actions found more the action to be added
        list_actions_found = last_list_actions_found.copy()
        list_actions_found.append(new_action)
        # Calculating the profit with and without the action to be added
        profit_with_x = cal_total_profit(list_actions_found)
        profit = cal_total_profit(last_list_actions_found)
        # If the profit with the action to be added is greater than without it
        if profit_with_x > profit:
            cost = cal_total_cost(list_actions_found)
            # Check if the cost is less than MAX_EXPENSE
            if cost <= MAX_EXPENSE:
                last_list_actions_found = list_actions_found.copy()
    return find_best_combination(MAX_EXPENSE, actions, last_list_actions_found)


@execution_information
def optimized(MAX_EXPENSE, actions):
    """
    Find the best combination with a solution based on knapsack solution

    Args:
        MAX_EXPENSE (int): Maximum amount to spend
        actions (list): list of all actions

    Returns:
        best_combination (list): Combination of the best profit
    """
    # Sorts actions by rentability
    actions = sorted(actions, key=lambda x: cal_total_profit([x])/x["cost"])
    # last_combination = []
    best_combination = [{"name": "", "cost": 0, "profit": 0}]
    # search the best combination
    return find_best_combination(MAX_EXPENSE, actions.copy(), best_combination)


if __name__ == "__main__":
    # Spending limit
    MAX_EXPENSE = 500
    # list of filenames
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
            show_information(filename, best_combination)
        elif choice == "stop":
            stop = True
