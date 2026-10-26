import csv
import os

def get_all_from_csv(filename: str) -> list:
    """Lee todos los registros de un archivo CSV y los devuelve como lista de diccionarios."""
    if not os.path.exists(filename):
        return []
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        # Limpiamos posibles espacios en blanco en las llaves o valores
        cleaned_rows = []
        for row in reader:
            if row:
                cleaned_row = {k.strip(): v.strip() for k, v in row.items() if k}
                cleaned_rows.append(cleaned_row)
        return cleaned_rows

def save_to_csv(filename: str, data: dict):
    """Guarda un nuevo diccionario en el archivo CSV, agregando cabecera si el archivo está vacío."""
    file_exists = os.path.exists(filename) and os.path.getsize(filename) > 0
    fieldnames = list(data.keys())

    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        # Convertimos todos los valores a string para evitar conflictos en CSV
        string_data = {k: str(v) for k, v in data.items()}
        writer.writerow(string_data)

def update_csv_file(filename: str, data_list: list, fieldnames: list):
    """Reescribe completamente el archivo CSV (usado para borrados lógicos o actualizaciones)."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for data in data_list:
            if data:
                string_data = {k: str(v) for k, v in data.items() if k in fieldnames}
                writer.writerow(string_data)