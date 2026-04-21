import requests
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime
import sys
import os
import re
from dotenv import load_dotenv

# Configuración de la base de datos
# Asegúrate de usar la contraseña que configuramos en psql
DB_CONFIG = {
    "host": "localhost",
    "database": "fintech_monitor",
    "user": "postgres",
    "password": "admin123" 
}

def get_db_connection():
    """Establece conexión con PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)

def scrape_finance_news():
    url = "https://finance.yahoo.com/news/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"[{datetime.now()}] Iniciando scraping en {url}...")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Buscamos TODOS los enlaces que tengan un h3 dentro (estructura común de Yahoo)
        # O enlaces que tengan clases de titulares
        links = soup.find_all('a')
        
        new_count = 0
        conn = get_db_connection()
        cur = conn.cursor()

        for a in links:
            title = a.text.strip()
            link = a.get('href', '')

            # FILTROS CRÍTICOS:
            # 1. El título debe ser largo (más de 30 caracteres para que sea una noticia real)
            # 2. El link debe contener '/news/',='/m/' o '/article' (estructura actual de Yahoo)
            if len(title) > 30 and any(keyword in link for keyword in ['/news/', '/m/', '/article']):
                
                if not link.startswith('http'):
                    link = 'https://finance.yahoo.com' + link
                
                # Evitar duplicados en la misma ejecución
                query = """
                INSERT INTO financial_articles (source, title, url, content)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (url) DO NOTHING;
                """
                cur.execute(query, ('Yahoo Finance', title, link, title))
                
                if cur.rowcount > 0:
                    new_count += 1
                    print(f" -> Capturado: {title[:70]}...")

        conn.commit()
        cur.close()
        conn.close()
        
        print(f"[{datetime.now()}] Proceso terminado. Se agregaron {new_count} noticias reales.")
        return new_count

    except Exception as e:
        print(f"Error: {e}")
        return 0

if __name__ == "__main__":
    scrape_finance_news()