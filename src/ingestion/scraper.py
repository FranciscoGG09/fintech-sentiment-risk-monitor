import requests
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime
import sys
import os

# Añadimos el path para poder importar nuestra función de limpieza
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.utils.text_cleaner import clean_financial_text

# Configuración de la conexión
DB_CONFIG = {
    "host": "localhost",
    "database": "fintech_monitor",
    "user": "postgres",
    "password": "TU_PASSWORD_AQUI" # ¡No olvides poner tu password!
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def scrape_finance_news():
    url = "https://finance.yahoo.com/news/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    print(f"[{datetime.now()}] Iniciando scraping en {url}...")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Yahoo Finance usa estas clases para sus contenedores de noticias
        articles = soup.find_all('div', {'class': 'Py(14px)'}) 
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        new_count = 0
        for item in articles:
            title_tag = item.find('h3')
            link_tag = item.find('a')
            desc_tag = item.find('p')
            
            if title_tag and link_tag:
                raw_title = title_tag.text.strip()
                raw_link = link_tag['href']
                link = "https://finance.yahoo.com" + raw_link if not raw_link.startswith('http') else raw_link
                raw_content = desc_tag.text.strip() if desc_tag else "Sin descripción disponible"
                
                # --- TRANSFORMACIÓN (Limpieza) ---
                clean_title = clean_financial_text(raw_title)
                clean_content = clean_financial_text(raw_content)
                
                # --- CARGA (Inserción Única) ---
                try:
                    cur.execute(
                        """INSERT INTO financial_articles 
                           (source, title, url, content) 
                           VALUES (%s, %s, %s, %s) 
                           ON CONFLICT (url) DO NOTHING""",
                        ('Yahoo Finance', clean_title, link, clean_content)
                    )
                    
                    if cur.rowcount > 0:
                        new_count += 1
                except Exception as e:
                    print(f"Error al insertar noticia: {e}")
                    conn.rollback()

        conn.commit()
        cur.close()
        conn.close()
        print(f"[{datetime.now()}] Proceso terminado. Se agregaron {new_count} noticias nuevas limpias.")

    except Exception as e:
        print(f"Error crítico en el scraper: {e}")

if __name__ == "__main__":
    scrape_finance_news()