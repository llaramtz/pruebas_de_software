"""
Este módulo cuenta la frecuencia de cada palabra en un archivo de texto. Las palabras se
consideran distintas sin importar su capitalización. Los resultados se imprimen en pantalla
y se guardan en un archivo.
"""

import sys
import time

def count_words(filename):
    """
    Lee un archivo de texto, cuenta la frecuencia de cada palabra y guarda los resultados
    en un archivo. Las palabras inválidas se omiten y se informa en la consola.
    """
    start_time = time.time()
    word_count = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                words = line.strip().split()
                for word in words:
                    if word.isalpha():
                        word = word.lower()
                        word_count[word] = word_count.get(word, 0) + 1
                    else:
                        print(f"Invalid data found and skipped: {word}")

        with open(filename+'.P3.Results.txt', 'w', encoding='utf-8') as file:
            for word, count in word_count.items():
                result = f"{word}: {count}"
                print(result)
                file.write(result + "\n")

    except FileNotFoundError as file_not_found_error:
        print(f"File not found: {filename} - Error: {file_not_found_error}")
    finally:
        elapsed_time = time.time() - start_time
        print(f"Execution Time: {elapsed_time} seconds")
        with open(filename+'.P3.Results.txt', 'a', encoding='utf-8') as file:
            file.write(f"\nExecution Time: {elapsed_time} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python word_count.py <filename>")
    else:
        count_words(sys.argv[1])
