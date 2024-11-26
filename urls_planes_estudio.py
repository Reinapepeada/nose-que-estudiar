import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import json

# Variable global para almacenar las URLs encontradas
found_urls = []
visited_urls = []
url = "https://www.uade.edu.ar/sitemap"

def scrape_page(urlActual, depth=0):
    global found_urls
    global visited_urls
    global url
    #  agregar la URL actual a la lista de URLs visitadas pero sin el https://www.uade.edu.ar
    visited_urls.append(urlActual.replace(url, ''))
    print(f"{'  ' * depth}Visiting: {visited_urls[-1]}")

    # Intentar realizar la solicitud
    try:
        response = requests.get(urlActual)
        if response.status_code != 200:
            print(f"{'  ' * depth}Error al acceder a {urlActual}, status: {response.status_code}")
            return []
        
        # Analizar el contenido de la página
        soup = BeautifulSoup(response.text, 'html.parser')

        # identifico el main
        main = soup.find('main')

        # Buscar todas las etiquetas <a> dentro del main
        links = main.find_all('a', href=True)

        # si no hay links o estan todos en la lista de visitados, cortar la recursión
        if not links or all([link['href'] in visited_urls for link in links]):
            return

        # Filtrar los enlaces que no contienen http o https
        # links = [link for link in links if not re.search(r'^https?://', link['href'])]

        # Filtrar las URLs que contienen mailto: o que terminan en extensiones de archivos  o que contienen ciertas palabras o que si empieza por http que sea de la misma pagina
        filtered_links = []
        for link in links:
            href = link['href']
            if re.search(r'^https?://', href):
                if re.search(r'^https?://www.uade.edu.ar', href) and not re.search(r'mailto:|\.pdf$|\.jpg$|\.png$|\.jpeg$|noticias|informacion|acerca-de-uade|sites|informacion-para|agenda|event-form|minors-en-uade-potencia-tu-carrera-elegi-tu-formacion|investigacion|whatsapp|youtube|instagram|facebook|twitter|linkedin|uade-|admisionesweb|admision', href):
                    filtered_links.append(link)
            else:
                if not re.search(r'mailto:|\.pdf$|\.jpg$|\.png$|\.jpeg$|noticias|informacion|acerca-de-uade|sites|informacion-para|agenda|event-form|minors-en-uade-potencia-tu-carrera-elegi-tu-formacion|investigacion|whatsapp|youtube|instagram|facebook|twitter|linkedin|uade-|admisionesweb|admision', href):
                    filtered_links.append(link)
        links = filtered_links
        # Mostrar todos los atributos href de las etiquetas <a> parseados
        print([link['href'] for link in links])

        # Filtrar las URLs que terminan en 'plan-de-estudios/'
        for link in links:
            href = link['href']
            if href in ['/', '#']:
                continue
            full_url = urljoin(urlActual, href)
            if re.search(r'plan-de-estudios/$', full_url):
                found_urls.append(full_url)
                print(f"{'  ' * depth}Found: {full_url}")
                return   # Condición de corte: se encontró una URL válida

        # Recursivamente buscar en los enlaces internos de la página
        for link in links:
            href = link['href']
            # print(f"{'  ' * depth}Checking: {href}")
            if href in ['/', '#'] or href in visited_urls:
                continue
            visited_urls.append(href)
            # print(f"{'  ' * depth}Visiting: {visited_urls}")
            full_url = urljoin(url, href)
            print(f"{'  ' * depth}Scraping: {full_url}")
            scrape_page(full_url, depth + 1)

    except requests.RequestException as e:
        print(f"{'  ' * depth}Error al acceder a {urlActual}: {e}")
        return []
    
    except Exception as e:  
        print(f"{'  ' * depth}Error inesperado: {e}")
        return []

# Uso
scrape_page(url)

# Escribir las URLs encontradas en un archivo JSON
with open('found_urls.json', 'w') as f:
    json.dump(found_urls, f, indent=4)

print("Found URLs ending with 'plan-de-estudios/':")
for url in found_urls:
    print(url)