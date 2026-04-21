import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class RiskDetector:
    def __init__(self):
        self.db_url = os.getenv("DB_URL", "postgresql://postgres:admin123@localhost:5432/fintech_monitor")
        self.engine = create_engine(self.db_url)

    def calculate_risk_metrics(self):
        # 1. Obtener datos de las últimas 24 horas
        yesterday = datetime.now() - timedelta(days=1)
        query = f"""
            SELECT sentiment_label, sentiment_score, published_at 
            FROM financial_articles 
            WHERE published_at > '{yesterday}'
            AND sentiment_label IS NOT NULL
        """
        df = pd.read_sql(query, self.engine)

        if df.empty:
            return {"status": "No hay datos suficientes", "risk_level": "N/A"}

        # 2. Calcular KPIs de riesgo
        total = len(df)
        negatives = len(df[df['sentiment_label'] == 'Negative'])
        negativity_ratio = (negatives / total) * 100

        # 3. Lógica de Alerta
        # Si el 60% o más de las noticias son negativas, hay un riesgo alto.
        risk_level = "Bajo"
        if negativity_ratio > 40: risk_level = "Medio"
        if negativity_ratio > 60: risk_level = "Alto / Crisis Reputacional"

        return {
            "total_articles": total,
            "negativity_ratio": round(negativity_ratio, 2),
            "risk_level": risk_level,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

if __name__ == "__main__":
    detector = RiskDetector()
    print(detector.calculate_risk_metrics())