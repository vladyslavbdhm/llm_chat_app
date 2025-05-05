import streamlit as st
import os
import pandas as pd
from io import StringIO
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# Configurar API y página
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
st.set_page_config(page_title="Analizador de Datos con LLM", page_icon="📊")
st.title("📊 Interpretador y Explorador de Datos con LLM")

st.markdown("""
Subí un archivo `.csv` **o** pegá métricas directamente. Se realizará un análisis exploratorio (EDA) y una interpretación automática con IA.
""")

# Inicializar historial si no existe
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Botón para limpiar historial
if st.button("🧽 Borrar conversación"):
    st.session_state.chat_history = []

# Entrada manual
user_text = st.text_area("✏️ Pegá aquí tus métricas o KPIs (opcional):", key="input_area", height=150)

# Subida de archivo
uploaded_file = st.file_uploader("📎 O subí un archivo CSV", type="csv")

# Variables de control
csv_text = ""
eda_text = ""

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file)

    # Limpiar nulos y limitar filas
    df_clean = df_raw.dropna()
    if len(df_clean) > 100:
        df_clean = df_clean.head(100)

    st.success(f"✅ Se usaron {len(df_clean)} filas sin nulos para análisis automático.")
    st.subheader("📄 Vista previa")
    st.dataframe(df_clean.head(10))

    # EDA básico
    buffer = StringIO()
    df_info = df_raw.info(buf=buffer)
    info_str = buffer.getvalue()

    eda_text += "📋 **Info del DataFrame:**\n```text\n" + info_str + "```\n"
    eda_text += "\n📊 **Valores nulos por columna:**\n"
    eda_text += df_raw.isnull().sum().to_string() + "\n"
    eda_text += "\n📈 **Resumen estadístico:**\n"
    eda_text += df_raw.describe().T.to_string()

    st.subheader("🧠 Análisis exploratorio (EDA)")
    st.markdown(f"```text\n{info_str}```")
    st.write("**Nulos por columna:**")
    st.dataframe(df_raw.isnull().sum().to_frame("Nulos"))
    st.write("**Estadísticas:**")
    st.dataframe(df_raw.describe().T)

    # Preparar texto para el LLM
    csv_text = df_clean.to_csv(index=False)

# Interpretación automática (si hay input o CSV válido)
if user_text.strip() or csv_text:
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    full_input = ""

    if csv_text:
        full_input += f"Datos tabulados:\n{csv_text}\n"

    if user_text.strip():
        full_input += f"Texto adicional:\n{user_text.strip()}\n"

    messages = [
        SystemMessage(content="""
Eres un experto en análisis de datos. Recibirás métricas, texto descriptivo o una tabla de datos.
Tu tarea es:
- Detectar patrones o tendencias
- Señalar anomalías
- Explicar posibles causas
- Sugerir conclusiones

Responde en español, de forma clara y estructurada.
"""),
        HumanMessage(content=full_input)
    ]

    with st.spinner("🤖 Analizando con IA..."):
        response = llm(messages)
        st.session_state.chat_history.append((full_input, response.content))

# Mostrar historial
if st.session_state.chat_history:
    st.divider()
    st.subheader("🗂 Historial de interpretaciones")
    for idx, (q, a) in enumerate(reversed(st.session_state.chat_history), 1):
        st.markdown(f"**🔎 Consulta {idx}:**")
        st.markdown("📝 **Entrada:**")
        st.code(q[:1500] + "\n... (truncado)" if len(q) > 1500 else q)
        st.markdown("💬 **Respuesta:**")
        st.markdown(a)
        st.markdown("---")
