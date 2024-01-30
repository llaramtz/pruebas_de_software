"""
Este módulo realiza el cálculo de estadísticas descriptivas (media, mediana, moda,
desviación estándar y varianza) para un conjunto de datos numéricos proporcionados en un archivo.
"""

import sys
import time

def calculate_mean(numbers):
    """Calcula y retorna la media de una lista de números."""
    return sum(numbers) / len(numbers) if numbers else 0

def calculate_median(numbers):
    """Calcula y retorna la mediana de una lista de números."""
    numbers.sort()
    num_items = len(numbers)
    mid_index = num_items // 2
    if num_items % 2 == 0:
        median = (numbers[mid_index] + numbers[~mid_index]) / 2
    else:
        median = numbers[mid_index]
    return median

def calculate_mode(numbers):
    """Calcula y retorna la moda de una lista de números."""
    frequency = {}
    for num in numbers:
        frequency[num] = frequency.get(num, 0) + 1
    max_freq = max(frequency.values())
    mode = [key for key, value in frequency.items() if value == max_freq]
    return mode[0] if len(mode) == 1 else mode

def calculate_variance(numbers):
    """Calcula y retorna la varianza de una lista de números."""
    mean = calculate_mean(numbers)
    return sum((x - mean) ** 2 for x in numbers) / len(numbers) if numbers else 0

def calculate_stdev(numbers):
    """Calcula y retorna la desviación estándar de una lista de números."""
    return calculate_variance(numbers) ** 0.5

def compute_statistics(filename):
    """
    Calcula y muestra las estadísticas descriptivas de los números en el archivo dado.
    Los resultados se escriben en un archivo y se muestran en pantalla.
    """
    start_time = time.time()
    numbers = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    number = float(line.strip())
                    numbers.append(number)
                except ValueError as val_error:
                    print(f"Invalid data found and skipped: {line.strip()} - Error: {val_error}")

        results = (f"Mean: {calculate_mean(numbers)}\n"
                   f"Median: {calculate_median(numbers)}\n"
                   f"Mode: {calculate_mode(numbers)}\n"
                   f"Variance: {calculate_variance(numbers)}\n"
                   f"Standard Deviation: {calculate_stdev(numbers)}")
        print(results)

        with open('StatisticsResults.txt', 'w', encoding='utf-8') as file:
            file.write(results)

    except FileNotFoundError as fnf_error:
        print(f"File not found: {filename} - Error: {fnf_error}")
    finally:
        elapsed_time = time.time() - start_time
        print(f"Execution Time: {elapsed_time} seconds")
        with open('StatisticsResults.txt', 'a', encoding='utf-8') as file:
            file.write(f"\nExecution Time: {elapsed_time} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python compute_statistics.py <filename>")
    else:
        compute_statistics(sys.argv[1])
