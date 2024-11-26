import requests
from bs4 import BeautifulSoup
import json

url = "https://www.uade.edu.ar/facultad-de-ingenieria-y-ciencias-exactas/licenciatura-en-gestion-de-tecnologia-de-la-informacion/plan-de-estudios/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

with open('found_urls.json', 'r') as f:
    found_urls = json.load(f)

for url in found_urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extract the name of the career
    career_name = soup.find('h1').get_text()
    print(career_name)
    data = {}
    data["Carrera"] = career_name
    data["Años"] = []

    titles = soup.find_all('h2')
    for title in titles:
        title_text = title.get_text()
        if title_text == "":
            break

        year_data = {"Año": title_text, "Cuatrimestres": []}
        
        next_sibling = title.find_next_sibling()
        if next_sibling:
            cuatrimestres = next_sibling.find_all('h5')
            for cuatrimestre in cuatrimestres:
                cuatrimestre_text = cuatrimestre.get_text()
                cuatrimestre_data = {"Cuatrimestre": cuatrimestre_text, "Materias": []}
                
                next_sibling = cuatrimestre.find_next_sibling()
                if next_sibling:
                    materias = next_sibling.find_all('span')
                    for materia in materias:
                        materia_text = materia.get_text()
                        cuatrimestre_data["Materias"].append(materia_text)
                
                year_data["Cuatrimestres"].append(cuatrimestre_data)
        
        data["Años"].append(year_data)
    
    # depurar los nombres de las carreras
    career_name = career_name.replace(' ', '_').replace('/', '_').replace(':', '').replace(',', '').replace(';', '').replace('?', '').replace('¿', '').replace('¡', '')

    with open(f'./planes/{career_name}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
