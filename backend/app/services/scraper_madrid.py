import requests
from bs4 import BeautifulSoup as bs
import random
import time
import pandas as pd 
import numpy as np 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc 
from bs4 import BeautifulSoup as bs
import time 
import re
import unicodedata



# -----------------
# FUNCIÓN PARA ELIMINAR TILDES Y CARACTERES ESPECIALES
# -----------------
def quitar_tildes_y_caracteres(texto):
    """
    Elimina tildes y signos de puntuación, y separa palabras pegadas por mayúsculas.
    """
    try:
        # Reemplaza signos de puntuación por espacio
        texto = re.sub(r'[^\w\s]', ' ', texto)
        # Elimina tildes
        texto_normalizado = unicodedata.normalize('NFKD', texto)
        texto_sin_tildes = texto_normalizado.encode('ascii', 'ignore').decode('utf-8')
        # Separa palabras pegadas por mayúsculas (ejemplo: visitoMadrides -> visito Madrides)
        texto_separado = re.sub(r'(?<=[a-z])([A-Z])', r' \1', texto_sin_tildes)
        # Elimina cualquier carácter especial restante
        texto_limpio = re.sub(r'[^\w\s]', '', texto_separado)
        # Reemplaza múltiples espacios por uno solo y elimina espacios al inicio/final
        texto_limpio = re.sub(r'\s+', ' ', texto_limpio).strip()
        return texto_limpio
    except (TypeError, UnicodeEncodeError):
        return texto
# Crea una instancia del navegador (undetected_chromedriver)
browser = uc.Chrome()
url = "https://beaviajera.com/25-curiosidades-de-madrid-que-te-gustaran/"

try:
    browser.get(url)

    # Espera explícita para el botón de aceptar cookies
    try:
        # Usa el selector correcto para el botón de cookies
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="cookie_action_close_header"] '))
        ).click()
        print("Boton de cookies clickeado exitosamente.")
        time.sleep(2)
        #//*[@id="cookie_action_close_header"] 
        
        
    except:
        print("No se encontro el botón de cookies o no se pudo hacer clic. El script continuará.")
    
    # Obtiene el contenido de la página después de interactuar con las cookies
    html = browser.page_source
    soup = bs(html, 'lxml')

    # -----------------
    # SCRAPING DE DATOS 
    # -----------------
    
    # 1. Extrae el título del artículo
    # El selector correcto para el título es `h1` con la clase `entry-title`
    try:
        titulo = soup.find('h1', class_='entry-title').text
        print(f"Título: {titulo}")
    except AttributeError:
        print("Error: No se pudo encontrar el título. El selector 'h1.entry-title' puede ser incorrecto.")
        titulo = None
        
    # 2. Extrae las curiosidades de Madrid
    # Las curiosidades están dentro de etiquetas `p` y `li` en un div con la clase `entry-content`
    curiosidades = []
    content_div = soup.find('div', class_='entry-content')
    if content_div:
        # Busca todas las etiquetas de párrafo y lista
        for element in content_div.find_all(['p', 'li']):
            text = element.get_text(strip=True)
            # Aplica la función para quitar tildes y caracteres especiales
            clean_text = quitar_tildes_y_caracteres(text)
            # Reemplaza múltiples espacios en blanco por uno solo
            #clean_text = re.sub(r'\s+', ' ', clean_text).strip()
            if clean_text and len(clean_text) > 20 and "fuente" not in clean_text.lower():
                curiosidades.append(clean_text)


    # Guarda las curiosidades en un archivo .txt
    def guardar_en_txt(lista, nombre_archivo):
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            for i, fact in enumerate(lista, 1):
                f.write(f"{i}.{fact}\n")

    if curiosidades:
        print("\n--- Curiosidades Extraídas ---")
        for i, fact in enumerate(curiosidades, 1):
            print(f"{i}.{fact}\n")
        # Guarda automáticamente en curiosidades_madrid.txt
        guardar_en_txt(curiosidades, "curiosidades_madrid.txt")
        print("\nCuriosidades guardadas en curiosidades_madrid.txt")
    else:
        print("\nNo se encontraron curiosidades.")
        
finally:
    # Cierra el navegador al final del script
    browser.quit()
