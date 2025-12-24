import requests
from bs4 import BeautifulSoup
import csv

def extraer_datos_tienda(url):
    # 1. Configurar headers para parecer un navegador real y evitar bloqueos
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # 2. Hacer la petición a la web
        respuesta = requests.get(url, headers=headers)
        respuesta.raise_for_status() # Verifica si la descarga fue exitosa
        
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        
        # 3. Buscar los productos (ajusta los selectores según la web que elijas)
        productos = []
        # Ejemplo: buscamos elementos <div class="product">
        items = soup.find_all('div', class_='product-pod') 

        for item in items:
            nombre = item.find('h3').text.strip()
            precio = item.find('p', class_='price_color').text.strip()
            
            productos.append({
                'Nombre': nombre,
                'Precio': precio
            })
        
        return productos

    except Exception as e:
        print(f"Error al extraer: {e}")
        return []

def guardar_en_csv(datos, nombre_archivo):
    if not datos:
        print("No hay datos para guardar.")
        return

    llaves = datos[0].keys()
    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo:
        dict_writer = csv.DictWriter(archivo, fieldnames=llaves)
        dict_writer.writeheader()
        dict_writer.writerows(datos)
    print(f"Datos guardados exitosamente en {nombre_archivo}")

# --- EJECUCIÓN ---
url_objetivo = "http://books.toscrape.com/" # Web de práctica legal para scraping
datos_extraidos = extraer_datos_tienda(url_objetivo)
guardar_en_csv(datos_extraidos, 'mis_productos.csv')