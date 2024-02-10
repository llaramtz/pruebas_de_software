"""
This module contains functions to compute and report total sales
from a given product catalog and sales record in JSON format.
"""

import json
import sys
import time


def load_json_data(file_path):
    """
    Load and return the JSON data from a given file path.
    Handles JSON decoding errors and file not found errors.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as error:
        print(f"Error decoding JSON from {file_path}: {error}")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    return None


def calculate_total_sales(product_list, sales):
    """
    Calculate and return the total sales for each product
    and the grand total of all sales.
    """
    if product_list is None or sales is None:
        return {}, 0
    total_sales = {}
    grand_total = 0
    for sale in sales:
        product_name = sale['Product']
        quantity = sale['Quantity']
        for product in product_list:
            if product['title'] == product_name:
                if product_name not in total_sales:
                    total_sales[product_name] = {'total_cost': 0,
                                                 'quantity': 0}
                total_cost = quantity * product['price']
                total_sales[product_name]['total_cost'] += total_cost
                total_sales[product_name]['quantity'] += quantity
                grand_total += total_cost
    return total_sales, grand_total


def write_results_to_file(results, grand_total, file_name="SalesResults.txt"):
    """
    Write the sales results and the grand total to a specified file.
    """
    with open(file_name, 'w', encoding='utf-8') as file:
        for product, details in results.items():
            file.write(f"{product}: Quantity Sold: {details['quantity']}, "
                       f"Total Sales: ${details['total_cost']:.2f}\n")
        file.write(f"\nGrand Total of All Sales: ${grand_total:.2f}\n")


def main(product_list_file, sales_file):
    """
    Main function to load the product list and sales data,
    compute the total sales, and write the results to a file.
    """
    start_time = time.time()
    product_list = load_json_data(product_list_file)
    sales = load_json_data(sales_file)

    if product_list is None or sales is None:
        print("Error in input files. Exiting...")
        sys.exit(1)

    total_sales, grand_total = calculate_total_sales(product_list, sales)

    for product, details in total_sales.items():
        print(f"{product}: Quantity Sold: {details['quantity']}, "
              f"Total Sales: ${details['total_cost']:.2f}")

    print(f"\nGrand Total of All Sales: ${grand_total:.2f}")
    write_results_to_file(total_sales, grand_total)

    elapsed_time = time.time() - start_time
    print(f"Execution and calculus time: {elapsed_time:.2f} seconds.")
    with open("SalesResults.txt", 'a', encoding='utf-8') as file:
        file.write(f"Execution and calculus time: "
                   f"{elapsed_time:.2f} seconds.\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python computeSales.py "
              "priceCatalogue.json salesRecord.json")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
