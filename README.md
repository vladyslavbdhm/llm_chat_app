# 📊 Interpretador de Resultados de Análisis de Datos con LLM

Esta aplicación web utiliza un modelo de lenguaje (LLM) para interpretar métricas, estadísticas y resultados de dashboards, y explicarlos en lenguaje natural. Está pensada para ayudar a analistas, equipos de negocio y estudiantes a entender mejor sus datos.

---

## 🎯 ¿Qué hace esta app?

- 📥 Permite subir archivos `.csv` o ingresar texto manual
- 🤖 Genera automáticamente **insights generales** con IA (modelo GPT)
- 💬 Permite hacer **preguntas consecutivas** sobre los datos (mantiene historial)
- 📊 Muestra un **resumen exploratorio** (EDA) del dataset
- 📈 Permite generar **gráficos automáticos** para columnas numéricas

---


## 🧠 Tecnología utilizada

- [Streamlit](https://streamlit.io/) – interfaz web interactiva
- [Pandas](https://pandas.pydata.org/) – carga y análisis de datos
- [Matplotlib](https://matplotlib.org/) – generación de gráficos
- [LangChain](https://www.langchain.com/) – estructura conversacional con LLM
- [OpenAI](https://openai.com/) – modelo **GPT-3.5-turbo** para insights y preguntas

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
