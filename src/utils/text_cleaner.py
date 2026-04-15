import re
import unicodedata

def clean_financial_text(text):
    if not text:
        return ""

    # 1. Convertir a minúsculas
    text = text.lower()

    # 2. Eliminar acentos y caracteres especiales (Normalización)
    # Esto convierte 'acción' en 'accion' para evitar problemas de encoding
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    # 3. Eliminar URLs (a veces vienen en el contenido)
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

    # 4. Eliminar menciones (@user) y hashtags (#fintech)
    text = re.sub(r'@\w+|#\w+', '', text)

    # 5. Eliminar caracteres no deseados (quedarse solo con letras, números y signos de puntuación básicos)
    # Mantenemos los números porque en finanzas (tasas de interés, precios) son vitales.
    text = re.sub(r'[^a-z0-9\s.,!?]', '', text)

    # 6. Eliminar espacios en blanco extra
    text = re.sub(r'\s+', ' ', text).strip()

    return text