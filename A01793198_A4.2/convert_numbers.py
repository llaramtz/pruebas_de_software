"""
Este módulo realiza la conversión de números de un archivo de texto a sus representaciones
binarias y hexadecimales. Los resultados se imprimen en pantalla y se guardan en un archivo.
"""

import sys
import time


def to_binary(number):
    """
    Convierte un número entero a su representación binaria sin utilizar funciones incorporadas.
    Incluye soporte para números negativos utilizando complemento a dos.
    """
    if number == 0:
        return '0'

    is_negative = number < 0
    if is_negative:
        number = -number

    binary = ''
    while number > 0:
        binary = str(number % 2) + binary
        number = number // 2

    if is_negative:
        bits = len(binary)  # Determina la longitud necesaria para representar el número
        binary = ''.join('1' if b == '0' else '0' for b in binary)  # Complemento a uno
        binary = bin(int(binary, 2) + 1)[2:]  # Complemento a dos
        binary = binary.zfill(bits)

    return binary


def to_hexadecimal(number):
    """
    Convierte un número entero a su representación hexadecimal sin utilizar funciones incorporadas.
    Incluye soporte para números negativos utilizando complemento a dos.
    """
    if number == 0:
        return '0'

    is_negative = number < 0
    if is_negative:
        number = -number

    hex_map = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
               8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
    hexadecimal = ''
    while number > 0:
        hexadecimal = hex_map[number % 16] + hexadecimal
        number = number // 16

    if is_negative:
        bits = len(hexadecimal) * 4  # Determina la longitud necesaria en bits
        hexadecimal = ''.join(hex_map[(15 - int(h, 16)) % 16] for h in hexadecimal)
        hexadecimal = hex(int(hexadecimal, 16) + 1)[2:].upper()  # Complemento a dos
        hexadecimal = hexadecimal.zfill(bits // 4)

    return hexadecimal


def convert_numbers(filename):
    """
    Lee números de un archivo, los convierte a representaciones binarias y hexadecimales,
    e imprime los resultados en pantalla y los guarda en un archivo.
    Maneja valores no numéricos adecuadamente.
    """
    start_time = time.time()
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            numbers = []
            for line in file:
                try:
                    number = int(line.strip())
                    numbers.append(number)
                except ValueError:
                    print(f"Invalid data found and skipped: {line.strip()}")

        with open(filename+'.P2.Results.txt', 'w', encoding='utf-8') as file:
            for number in numbers:
                binary = to_binary(number)
                hexadecimal = to_hexadecimal(number)
                result = f"{number} -> Binary: {binary}, Hexadecimal: {hexadecimal}"
                print(result)
                file.write(result + "\n")

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
