import pandas as pd

# Lee el archivo CSV generado
csv_file = 'suemzit_resultados.csv'
df = pd.read_csv(csv_file)

# Mostrar resumen de los años disponibles
print('Años disponibles en el archivo:')
print(df['año'].unique())
