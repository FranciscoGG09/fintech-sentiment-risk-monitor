import requests
import os
from dotenv import load_dotenv
from src.models.risk_detector import RiskDetector

# Cargamos variables de entorno para seguridad (No subir tokens a GitHub)
load_dotenv()

class TelegramAlertSystem:
    def __init__(self):
        self.token = "TU_TELEGRAM_TOKEN"
        self.chat_id = "TU_CHAT_ID"
        self.detector = RiskDetector()

    def send_alert(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            print("Alerta enviada con éxito a Telegram.")
        except Exception as e:
            print(f"Error enviando alerta: {e}")

    def check_and_notify(self):
        metrics = self.detector.calculate_risk_metrics()
        
        # Solo enviar alerta si el riesgo es Medio o Alto
        if metrics["risk_level"] in ["Medio", "Alto / Crisis Reputacional"]:
            alert_msg = (
                f"⚠️ *ALERTA DE RIESGO FINANCIERO* ⚠️\n\n"
                f"*Nivel:* {metrics['risk_level']}\n"
                f"*Ratio de Negatividad:* {metrics['negativity_ratio']}%\n"
                f"*Artículos analizados (24h):* {metrics['total_articles']}\n"
                f"*Fecha:* {metrics['timestamp']}\n\n"
                f"👉 Revisa el dashboard para más detalles."
            )
            self.send_alert(alert_msg)
        else:
            print("El nivel de riesgo es normal. No se enviaron alertas.")

if __name__ == "__main__":
    notifier = TelegramAlertSystem()
    notifier.check_and_notify()