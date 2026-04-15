import requests
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime

# Configuración de la conexión a tu Postgres Local
DB_CONFIG = {
    "host": "localhost",
    "database": "fintech_monitor",
    "user": "postgres",  # Cambia por tu usuario si es distinto
    "password": "Andrei01" 
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def scrape_finance_news():
    url = "https://finance.yahoo.com/news/"
    # El User-Agent evita que el servidor bloquee la petición por parecer un bot básico
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    print(f"[{datetime.now()}] Iniciando scraping en {url}...")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Lanza error si la página no carga
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # En Yahoo Finance, las noticias suelen estar en etiquetas <h3> dentro de ciertos contenedores
        articles = soup.find_all('div', {'class': 'Py(14px)'}) # Este selector puede variar ligeramente
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        new_count = 0
        for item in articles:
            title_tag = item.find('h3')
            link_tag = item.find('a')
            desc_tag = item.find('p')
            
            if title_tag and link_tag:
                title = title_tag.text.strip()
                link = "https://finance.yahoo.com" + link_tag['href'] if not link_tag['href'].startswith('http') else link_tag['href']
                content = desc_tag.text.strip() if desc_tag else "Sin descripción disponible"
                
                # Insertar solo si la URL no existe (evita duplicados)
                try:
                    cur.execute(
                        "INSERT INTO financial_articles (source, title, url, content) VALUES (%s, %s, %s, %s) ON CONFLICT (url) DO NOTHING",
                        ('Yahoo Finance', title, link, content)
                    )
                    if cur.rowcount > 0:
                        new_count += 1
                except Exception as e:
                    print(f"Error al insertar: {e}")
                    conn.rollback()

        conn.commit()
        cur.close()
        conn.close()
        print(f"[{datetime.now()}] Proceso terminado. Se agregaron {new_count} noticias nuevas.")

    except Exception as e:
        print(f"Error en el scraper: {e}")

if __name__ == "__main__":
    scrape_finance_news()