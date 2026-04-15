🛡️ Fintech Sentiment & Risk Monitor - fintech-sentiment-risk-monitor

<p align="center">
<img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white" alt="PostgreSQL">
<img src="https://img.shields.io/badge/HuggingFace-FFD21E?style=flat&logo=huggingface&logoColor=black" alt="HuggingFace">
<img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white" alt="Docker">
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white" alt="Streamlit">
</p>

Este repositorio contiene un Pipeline de Datos End-to-End diseñado para el monitoreo de la salud reputacional y riesgo de mercado en instituciones financieras. El sistema automatiza la recolección de noticias, aplica inteligencia artificial para el análisis de sentimiento especializado y dispara alertas automáticas ante crisis potenciales.
🎯 Objetivos del Análisis

El sistema se centra en responder preguntas críticas para el sector Fintech:

    ¿Cuál es el sentimiento actual del mercado respecto a bancos y cajas populares?

    ¿Existen picos de negatividad que sugieran una crisis reputacional inminente?

    ¿Cómo correlaciona el sentimiento del público con la fluctuación de indicadores reales?

    ¿Cómo automatizar el monitoreo proactivo sin intervención humana constante?

📊 Proceso de Análisis e Ingeniería

El proyecto sigue una arquitectura de datos robusta dividida en etapas:

    Ingesta y Web Scraping (ETL): * Extracción automatizada de portales financieros (Yahoo Finance) usando BeautifulSoup.

        Persistencia en PostgreSQL con validación de duplicados (Idempotencia).

    Transformación y Limpieza (Data Cleaning): * Normalización de texto (remoción de URLs, menciones y caracteres especiales).

        Estandarización de formatos para optimizar la inferencia del modelo NLP.

    Procesamiento de Lenguaje Natural (NLP): * Implementación del modelo FinBERT (Hugging Face) optimizado para terminología financiera.

        Clasificación de artículos en categorías: Positivo, Negativo y Neutral.

    Visualización y Alertas: * Dashboard interactivo en Streamlit con métricas de riesgo en tiempo real.

        Microservicio de notificaciones vía Telegram para alertas críticas.

🛠️ Stack Tecnológico

    Lenguaje: Python 3.10+

    Base de Datos: PostgreSQL (Dockerizada)

    Modelado AI: FinBERT (Transformers/PyTorch)

    Dashboard: Streamlit y Plotly

🚀 Cómo Empezar

Para desplegar este monitor en tu entorno local, sigue estos pasos:

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

❓ Preguntas Frecuentes (FAQ)

    ¿Por qué usar FinBERT en lugar de modelos genéricos?
    FinBERT entiende el contexto financiero. Por ejemplo, reconoce que un "recorte de tasas" tiene implicaciones distintas a un recorte en otros contextos, ofreciendo una precisión mucho mayor en el análisis de riesgo.

    ¿Cómo se garantiza la integridad de los datos?
    Utilizamos restricciones de unicidad en PostgreSQL. El sistema está diseñado para ignorar noticias previamente procesadas mediante la cláusula ON CONFLICT, evitando la redundancia y el ruido estadístico.

    ¿Cómo funciona el sistema de alertas?
    El RiskDetector calcula el ratio de negatividad cada hora. Si el volumen de sentimiento negativo supera el umbral configurado (ej. 60%), se envía automáticamente un reporte detallado al administrador vía Telegram.

👨‍💻 Autor

Desarrollado por Francisco González.

    LinkedIn: linkedin.com/in/francisco-gonzalez

    GitHub: @FranciscoGG09