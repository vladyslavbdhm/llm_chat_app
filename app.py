import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# Leer clave API
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Configurar página
st.set_page_config(page_title="Analizador de Datos con LLM", page_icon="📊")
st.title("📊 Interpretador y Explorador de Datos con LLM")

st.markdown("""
Subí un archivo `.csv` con datos de negocio o resultados analíticos. El asistente realizará un análisis exploratorio (EDA) y, si lo deseás, una interpretación con inteligencia artificial.
""")

# Inicializar historial
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Botón para limpiar historial
if st.button("🧽 Borrar conversación"):
    st.session_state.chat_history = []

# Subida de archivo
uploaded_file = st.file_uploader("📎 Subí un archivo CSV", type="csv")

# Si se sube un archivo
if uploaded_file:
    df_raw = pd.read_csv(uploaded_file)

    st.subheader("📄 Vista previa del archivo")
    st.dataframe(df_raw.head(10))

    # Filtrar filas sin nulos y limitar a 100
    df_clean = df_raw.dropna().copy()
    if len(df_clean) > 100:
        df_clean = df_clean.head(100)

    st.success(f"✅ Usando {len(df_clean)} filas sin valores nulos para el análisis automático.")

    st.markdown("---")

    # Sección de EDA
    st.subheader("🔍 Exploración de Datos (EDA)")

    st.write("**📐 Dimensiones del archivo:**")
    st.write(f"{df_raw.shape[0]} filas × {df_raw.shape[1]} columnas")

    st.write("**📋 Columnas:**")
    st.write(df_raw.columns.tolist())

    st.write("**🕳️ Valores nulos por columna:**")
    st.write(df_raw.isnull().sum())

    st.write("**📊 Estadísticas numéricas:**")
    st.write(df_raw.describe())

    # Histograma
    st.subheader("📈 Distribuciones de columnas numéricas")
    numeric_cols = df_clean.select_dtypes(include="number").columns.tolist()

    if numeric_cols:
        for col in numeric_cols:
            fig, ax = plt.subplots()
            df_clean[col].hist(bins=20, ax=ax)
            ax.set_title(f"Distribución de {col}")
            st.pyplot(fig)
    else:
        st.info("No se encontraron columnas numéricas para graficar.")

    st.markdown("---")

    # Entrada de texto opcional
    user_input = st.text_area("✏️ Comentarios o preguntas adicionales (opcional):", key="input_area")

    # Botón para interpretar
    if st.button("🤖 Interpretar con LLM"):
        if not df_clean.empty:
            # Convertir a texto
            csv_text = df_clean.to_csv(index=False)

            # Armar input
            full_input = f"""Datos del archivo (primeras {len(df_clean)} filas sin nulos):\n{csv_text}"""
            if user_input.strip():
                full_input += f"\n\nComentarios adicionales:\n{user_input.strip()}"

            llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

            messages = [
                SystemMessage(content="""
Eres un experto en análisis de datos. Recibirás datos tabulados o métricas de negocio.
Tu tarea es:
- Detectar patrones o irregularidades
- Explicar tendencias
- Sugerir hipótesis o conclusiones
Responde en español, de forma clara y estructurada.
"""),
                HumanMessage(content=full_input)
            ]

            with st.spinner("Analizando con LLM..."):
                response = llm(messages)
                st.session_state.chat_history.append((full_input, response.content))
        else:
            st.warning("No hay suficientes datos sin nulos para enviar al modelo.")

# Mostrar historial
if st.session_state.chat_history:
    st.divider()
    st.subheader("🗂 Historial de Interpretaciones")

    for idx, (q, a) in enumerate(reversed(st.session_state.chat_history), 1):
        st.markdown(f"**🔎 Consulta {idx}:**")
        st.write("📝 **Entrada enviada:**")
        st.code(q[:1500] + "\n... (truncado)" if len(q) > 1500 else q, language="markdown")

        st.markdown("💬 **Respuesta:**")
        st.markdown(a)
        st.markdown("---")
