import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from io import StringIO

# Configurar API y página
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
st.set_page_config(page_title="Analizador de Datos con LLM", page_icon="📊")
st.title("📊 Interpretador de Resultados con LLM")

st.markdown("""
Podés subir un archivo `.csv` o ingresar texto manualmente. El asistente analizará los datos, y podés obtener métricas y gráficos adicionales con los botones opcionales.
""")

# Inicializar historial si no existe
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Botón para limpiar conversación
if st.button("🧽 Borrar conversación"):
    st.session_state.chat_history = []

# Subida de CSV
uploaded_file = st.file_uploader("📎 Subí un archivo CSV", type="csv")

df_clean = None
csv_text = ""
if uploaded_file:
    df_raw = pd.read_csv(uploaded_file)
    df_clean = df_raw.dropna()
    if len(df_clean) > 100:
        df_clean = df_clean.head(100)
    csv_text = df_clean.to_csv(index=False)
    st.success(f"✅ Se usarán {len(df_clean)} filas sin nulos para el análisis.")

    st.subheader("📄 Vista previa del archivo")
    st.dataframe(df_clean.head(10))

# Entrada manual
user_input = st.text_area("✏️ Ingresá texto con métricas o KPIs (opcional):", key="input_area", height=150)

# Botón para interpretar
if st.button("🤖 Interpretar"):
    if user_input.strip() or csv_text:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

        messages = [SystemMessage(content="""
Eres un experto en análisis de datos. Recibirás métricas, texto descriptivo o una tabla de datos.
Tu tarea es:
- Detectar patrones o tendencias
- Señalar anomalías
- Explicar posibles causas
- Sugerir conclusiones

Responde en español, de forma clara y estructurada.
""")]

        # Agregar historial como contexto
        for user_msg, ai_msg in st.session_state.chat_history:
            messages.append(HumanMessage(content=user_msg))
            messages.append(HumanMessage(content=ai_msg))

        # Armar input combinado
        combined_input = ""
        if csv_text:
            combined_input += f"Datos del archivo:\n{csv_text}\n"
        if user_input.strip():
            combined_input += f"Texto adicional:\n{user_input.strip()}"

        messages.append(HumanMessage(content=combined_input))

        with st.spinner("Analizando..."):
            response = llm(messages)
            st.session_state.chat_history.append((combined_input, response.content))
    else:
        st.warning("Ingresá texto o subí un archivo para analizar.")

# Botón para mostrar métricas básicas (EDA)
if st.button("📊 Ver métricas básicas (EDA)") and df_clean is not None:
    st.subheader("📐 Info del DataFrame")
    buffer = StringIO()
    df_clean.info(buf=buffer)
    st.text(buffer.getvalue())

    st.subheader("🕳️ Valores nulos por columna")
    st.dataframe(df_clean.isnull().sum().to_frame("Nulos"))

    st.subheader("📈 Estadísticas numéricas")
    st.dataframe(df_clean.describe().T)

# Botón para mostrar gráficos
if st.button("📈 Mostrar gráficos") and df_clean is not None:
    st.subheader("📊 Gráficos de columnas numéricas")
    numeric_cols = df_clean.select_dtypes(include="number").columns.tolist()

    if numeric_cols:
        for col in numeric_cols:
            fig, ax = plt.subplots()
            df_clean[col].hist(bins=20, ax=ax)
            ax.set_title(f"Distribución de {col}")
            st.pyplot(fig)
    else:
        st.info("No hay columnas numéricas para graficar.")

# Mostrar historial completo (chat)
if st.session_state.chat_history:
    st.divider()
    st.subheader("🗂 Historial de Conversación")

    for idx, (q, a) in enumerate(reversed(st.session_state.chat_history), 1):
        st.markdown(f"**🔎 Consulta {idx}:**")
        st.markdown("📝 **Entrada:**")
        st.code(q[:1500] + "\n... (truncado)" if len(q) > 1500 else q)
        st.markdown("💬 **Respuesta:**")
        st.markdown(a)
        st.markdown("---")
