from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Inicializa el navegador Chrome
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Ejecuta en modo sin interfaz gráfica
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Abre la página
url = "https://suemzit.site123.me/"
driver.get(url)

time.sleep(10)  # Espera a que cargue el contenido dinámico


from bs4 import BeautifulSoup
import json

# Extrae el HTML
html = driver.page_source
driver.quit()

# Parsea el HTML
soup = BeautifulSoup(html, 'html.parser')

data = []


# Busca todas las secciones principales por h2 (título de sección)
for section in soup.find_all('section'):
	h2 = section.find('h2')
	if not h2:
		continue
	section_title = h2.get_text(strip=True)
	# Busca listas de años y trimestres/meses con PDFs
	for ul in section.find_all('ul'):
		for li in ul.find_all('li', recursive=False):
			li_text = li.get_text(separator=' ', strip=True)
			# Detecta año en el texto (ej: "Año: 2015")
			if 'Año:' in li_text:
				year = li_text.split('Año:')[1].split()[0]
				# Busca sub-lista de periodos
				for subli in li.find_all('li'):
					periodo = subli.get_text(strip=True)
					link = subli.find('a')
					if link and link['href'].endswith('.pdf'):
						data.append({
							'seccion': section_title,
							'año': year,
							'periodo': periodo,
							'url': link['href']
						})
			else:
				# Busca año y periodo en el texto si están juntos (ej: "2015Julio")
				link = li.find('a')
				if link and link['href'].endswith('.pdf'):
					# Intenta extraer año (4 dígitos) y el resto como periodo
					import re
					match = re.match(r'(20\d{2})(.*)', li_text)
					if match:
						year = match.group(1)
						periodo = match.group(2).strip()
					else:
						year = ''
						periodo = li_text
					data.append({
						'seccion': section_title,
						'año': year,
						'periodo': periodo,
						'url': link['href']
					})

# Guarda los resultados en un archivo JSON
with open('suemzit_resultados.json', 'w', encoding='utf-8') as f:
	json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Se extrajeron {len(data)} archivos PDF. Resultados guardados en suemzit_resultados.json")
