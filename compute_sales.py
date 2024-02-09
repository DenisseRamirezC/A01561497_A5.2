"""
compute_sales.py

This script calculates the total cost of sales recorded in the second json file
for each product according to the unit price established in the catalog of the
first json file. The results are printed on a screen and on a file named
SalesResults.txt.

DENISSE MARIA RAMIREZ COLMENERO
A01561497
"""
import os
import json
import time      # Obtain the time elapsed for the execution and calculations.
from tabulate import tabulate


NEW_FILE_NAME = "SalesResults.txt"


def calculate_total_cost(folders):
    """
    This function calculates the total cost of sales for each product
    by traversing through each folder and file.
    :param file_path: Path to the file
    """
    try:
        total_cost = 0

        for folder in folders:
            files = os.listdir(folder)  # Obtain list of files in each folder

            # Create lists only with files in the original list that end with..
            product_files = [file for file in files
                             if file.endswith("ProductList.json")]
            sales_files = [file for file in files
                           if file.endswith("Sales.json")]

            product_prices = {}

            # Create dictionary where key = title of product, and value = price
            for json_file in product_files:
                with open(os.path.join(folder, json_file), "r",
                          encoding="utf-8") as f:

                    data_list = json.load(f)
                    for data in data_list:
                        product_prices[data["title"]] = data["price"]

            # Obtain the cost with product_prices dictionary and sales file
            for json_file in sales_files:
                with open(os.path.join(folder, json_file), "r",
                          encoding="utf-8") as f:

                    data_list = json.load(f)
                    for sales in data_list:
                        product = sales["Product"]
                        quantity = sales["Quantity"]
                        # Look up the price of the product in dictionary
                        total_cost += quantity * (product_prices
                                                  .get(product, 0))

        return total_cost

    except FileNotFoundError as e:
        print(f"File not found: {folders} ({e})")
    except IOError as e:
        print(f"IOError: {e}")
    return []


def main():
    """
    This function prints the results of the total costs of the three folders
    in a table in addition to the execution time of the program. These results
    are also printed in a new .txt file.
    """
    start_time = time.time()
    # Get the directory of the current file in which the script is located
    directory = os.path.dirname(os.path.abspath(__file__))

    # Build full path to the file directory relative to the script location
    tc1 = [os.path.join(directory, 'TC1')]
    tc2 = [os.path.join(directory, 'TC2')]
    tc3 = [os.path.join(directory, 'TC3')]

    total_cost1 = calculate_total_cost(tc1)
    total_cost2 = calculate_total_cost(tc2)
    total_cost3 = calculate_total_cost(tc3)

    end_time = time.time()
    execution_time = end_time - start_time

    table = [
        ["TC1", total_cost1],
        ["TC2", total_cost2],
        ["TC3", total_cost3]
    ]
    headers = ["FOLDER", "TOTAL COST"]

    print(tabulate(table, headers, tablefmt="pretty"))
    print("Execution time", execution_time)

    # Results printed on a fule named SalesResults.txt
    output_file = os.path.join(directory, NEW_FILE_NAME)
    with open(output_file, "w", encoding="utf-8") as new_file:
        new_file.write(tabulate(table, headers, tablefmt="plain"))
        new_file.write(f"\n\nExecution Time: {execution_time} seconds")


if __name__ == "__main__":
    main()
