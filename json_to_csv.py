import json
import csv

# Lee los datos del archivo JSON
with open('suemzit_resultados.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


# Define los nombres de las columnas
fieldnames = ['seccion', 'año', 'periodo', 'url']

# Escribe los datos en un archivo CSV
with open('suemzit_resultados.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        writer.writerow(row)

print('Archivo suemzit_resultados.csv generado correctamente.')
