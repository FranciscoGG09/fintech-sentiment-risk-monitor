import torch
from transformers import BertTokenizer, BertForSequenceClassification
from sqlalchemy import create_engine, text
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

class SentimentAnalyzer:
    def __init__(self):
        # Cargamos el modelo especializado en finanzas
        self.model_name = "ProsusAI/finbert"
        self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
        self.model = BertForSequenceClassification.from_pretrained(self.model_name)
        
        # La URL de SQLAlchemy debe llevar la contraseña así:
        self.db_url = os.getenv("DB_URL", "postgresql://postgres:admin123@localhost:5432/fintech_monitor")
        self.engine = create_engine(self.db_url)

    def analyze_pending_articles(self):
        # 1. Traer solo artículos que no han sido procesados
        query = "SELECT id, content FROM financial_articles WHERE sentiment_label IS NULL LIMIT 50"
        df = pd.read_sql(query, self.engine)

        if df.empty:
            print("No hay artículos nuevos para analizar.")
            return

        print(f"Procesando {len(df)} artículos con FinBERT...")

        results = []
        for index, row in df.iterrows():
            # Tokenización del texto
            inputs = self.tokenizer(row['content'], return_tensors="pt", padding=True, truncation=True, max_length=512)
            
            # Inferencia del modelo
            with torch.no_grad():
                outputs = self.model(**inputs)
                # Aplicamos Softmax para obtener probabilidades
                probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
                
            # Obtener la clase con mayor probabilidad
            # FinBERT labels: 0 -> Positive, 1 -> Negative, 2 -> Neutral
            labels = ["Positive", "Negative", "Neutral"]
            max_index = torch.argmax(probs).item()
            sentiment = labels[max_index]
            score = probs[0][max_index].item()

            # Guardar actualización en la DB
            self.update_db(row['id'], sentiment, score)
        
        print("Análisis de sentimiento completado.")

    def update_db(self, article_id, label, score):
        query = text("""
            UPDATE financial_articles 
            SET sentiment_label = :label, 
                sentiment_score = :score 
            WHERE id = :id
        """)
        
        with self.engine.connect() as conn:
            conn.execute(query, {
                "label": label,
                "score": float(score),
                "id": int(article_id)
            })
            conn.commit() # Muy importante para que los cambios se guarden

if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    analyzer.analyze_pending_articles()