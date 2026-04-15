# main.py
from src.ingestion.scraper import scrape_finance_news
from src.models.sentiment_analyzer import SentimentAnalyzer
from src.alerts.telegram_notifier import TelegramAlertSystem

def run_pipeline():
    print("--- 1. Iniciando Ingesta de Datos ---")
    scrape_finance_news()
    
    print("\n--- 2. Analizando Sentimiento con FinBERT ---")
    analyzer = SentimentAnalyzer()
    analyzer.analyze_pending_articles()
    
    print("\n--- 3. Verificando Alertas de Riesgo ---")
    notifier = TelegramAlertSystem()
    notifier.check_and_notify()

if __name__ == "__main__":
    run_pipeline()