"""
Este módulo realiza la conversión de números de un archivo de texto a sus representaciones
binarias y hexadecimales. Los resultados se imprimen en pantalla y se guardan en un archivo.
"""

import sys
import time

def to_binary(number):
    """
    Convierte un número entero a su representación binaria sin utilizar funciones incorporadas.
    """
    binary = ''
    while number > 0:
        binary = str(number % 2) + binary
        number = number // 2
    return binary or '0'

def to_hexadecimal(number):
    """
    Convierte un número entero a su representación hexadecimal sin utilizar funciones incorporadas.
    """
    hex_map = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5',
               6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B',
               12: 'C', 13: 'D', 14: 'E', 15: 'F'}
    hexadecimal = ''
    while number > 0:
        hexadecimal = hex_map[number % 16] + hexadecimal
        number = number // 16
    return hexadecimal or '0'

def convert_numbers(filename):
    """
    Lee números de un archivo, los convierte a representaciones binarias y hexadecimales,
    e imprime los resultados en pantalla y los guarda en un archivo.
    """
    start_time = time.time()
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            numbers = [int(line.strip()) for line in file if line.strip().isdigit()]

        with open(filename+'.P2.Results.txt', 'w', encoding='utf-8') as file:
            for number in numbers:
                binary = to_binary(number)
                hexadecimal = to_hexadecimal(number)
                result = (f"{number} -> Binary: {binary}, "
                          f"Hexadecimal: {hexadecimal}")
                print(result)
                file.write(result + "\n")

    except ValueError as val_error:
        print(f"Invalid data found and skipped - Error: {val_error}")
    except FileNotFoundError as fnf_error:
        print(f"File not found: {filename} - Error: {fnf_error}")
    finally:
        elapsed_time = time.time() - start_time
        print(f"Execution Time: {elapsed_time} seconds")
        with open(filename+'.P2.Results.txt', 'a', encoding='utf-8') as file:
            file.write(f"\nExecution Time: {elapsed_time} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_numbers.py <filename>")
    else:
        convert_numbers(sys.argv[1])
