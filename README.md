# 📊 Interpretador de Resultados de Análisis de Datos con LLM

Esta aplicación web utiliza un modelo de lenguaje (LLM) para interpretar métricas, estadísticas y resultados de dashboards, y explicarlos en lenguaje natural. Está pensada para ayudar a analistas, equipos de negocio y estudiantes a entender mejor sus datos.

---

## 🎯 Propósito

El modelo recibe como entrada texto con resultados de análisis (por ejemplo: KPIs, tablas de datos, indicadores estadísticos o resúmenes de Power BI / Google Sheets), y genera una interpretación en español:

- Explica qué indican los datos.
- Detecta anomalías o puntos llamativos.
- Presenta conclusiones clave en lenguaje claro.

---

## 🧠 Tecnología utilizada

- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- OpenAI API (`gpt-3.5-turbo`)

---

## ▶️ ¿Cómo usar esta aplicación?

### Opción 1: Desde la nube (recomendado)

La app está publicada en Streamlit Cloud y accesible desde:

👉 [https://llmchatapp-vladyslav-dodonov.streamlit.app/](https://llmchatapp-vladyslav-dodonov.streamlit.app/)

### Opción 2: Ejecutar localmente

1. Clonar el repositorio:

```bash
git clone https://github.com/tuusuario/llm_chat_app.git
cd llm_chat_app
