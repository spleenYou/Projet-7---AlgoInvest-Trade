import csv

actions = []
max_expense = 500


def readFile():
    with open("Liste actions.csv") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=",")
        for data in csv_data:
            try:
                int(data[1])
                actions.append({
                    "name": data[0],
                    "cost": int(data[1]),
                    "profit": int(data[2].replace("%", ""))
                })
            except ValueError:
                None
#    return csv_data


if __name__ == "__main__":
    readFile()
    print(actions)
