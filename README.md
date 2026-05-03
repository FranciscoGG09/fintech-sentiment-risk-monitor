# 🛡️ Fintech Sentiment & Risk Monitor

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/HuggingFace-FFD21E?style=flat&logo=huggingface&logoColor=black" alt="HuggingFace">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white" alt="Streamlit">
</p>

**Pipeline de datos end‑to‑end** para el monitoreo de la **salud reputacional** y el **riesgo de mercado** en instituciones financieras.  
Automatiza la recolección de noticias, aplica **IA especializada** en análisis de sentimiento financiero y dispara **alertas automáticas** ante posibles crisis.

---

## 🎯 Objetivos del Análisis

El sistema responde preguntas críticas para el sector **Fintech**:

- **¿Cuál es el sentimiento actual del mercado** respecto a bancos y cajas populares?
- **¿Existen picos de negatividad** que sugieran una crisis reputacional inminente?
- **¿Cómo correlaciona el sentimiento del público** con la fluctuación de indicadores reales?
- **¿Cómo automatizar el monitoreo proactivo** sin intervención humana constante?

---

## 📊 Proceso de Análisis e Ingeniería

Arquitectura robusta dividida en etapas:

### 1. Ingesta y Web Scraping (ETL)
- **Extracción** automatizada desde portales financieros (Yahoo Finance) usando `BeautifulSoup`.
- **Persistencia** en PostgreSQL con validación de duplicados (**idempotencia**).

### 2. Transformación y Limpieza (Data Cleaning)
- **Normalización de texto**: remoción de URLs, menciones y caracteres especiales.
- **Estandarización** de formatos para optimizar la inferencia del modelo NLP.

### 3. Procesamiento de Lenguaje Natural (NLP)
- Modelo **FinBERT** de Hugging Face, optimizado para terminología financiera.
- Clasificación de artículos en: **Positivo**, **Negativo** o **Neutral**.

### 4. Visualización y Alertas
- **Dashboard interactivo** en Streamlit con métricas de riesgo en tiempo real.
- **Microservicio de notificaciones** vía Telegram para alertas críticas.

---

## 🛠️ Stack Tecnológico

| Componente       | Tecnología                              |
|-----------------|-----------------------------------------|
| **Lenguaje**    | Python 3.10+                            |
| **Base de datos**| PostgreSQL (Dockerizada)                |
| **Modelado AI** | FinBERT (Transformers / PyTorch)        |
| **Dashboard**   | Streamlit + Plotly                      |

---

## 🚀 Cómo Empezar

Sigue estos pasos para desplegar el monitor en tu entorno local:
 Clonar el repositorio:
    Bash

    git clone https://github.com/FranciscoGG09/fintech-sentiment-risk-monitor.git
    cd fintech-sentiment-risk-monitor

    Configurar el entorno y dependencias:
    Bash

    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    pip install -r requirements.txt

    Configurar variables de entorno:

        Crea un archivo .env en la raíz con tus credenciales de Postgres y Tokens de Telegram.

    Ejecutar el Pipeline:
    Bash

    python main.py
    streamlit run src/dashboard/app.py
---

## ❓ Preguntas Frecuentes (FAQ)

    ¿Por qué usar FinBERT en lugar de modelos genéricos?
    FinBERT entiende el contexto financiero. Por ejemplo, reconoce que un "recorte de tasas" tiene implicaciones distintas a un recorte en otros contextos, ofreciendo una precisión mucho mayor en el análisis de riesgo.

    ¿Cómo se garantiza la integridad de los datos?
    Utilizamos restricciones de unicidad en PostgreSQL. El sistema está diseñado para ignorar noticias previamente procesadas mediante la cláusula ON CONFLICT, evitando la redundancia y el ruido estadístico.

    ¿Cómo funciona el sistema de alertas?
    El RiskDetector calcula el ratio de negatividad cada hora. Si el volumen de sentimiento negativo supera el umbral configurado (ej. 60%), se envía automáticamente un reporte detallado al administrador vía Telegram.
---

## 👨‍💻 Autor

Desarrollado por Francisco González.

    LinkedIn: linkedin.com/in/francisco-gonzalez

    GitHub: @FranciscoGG09
   
