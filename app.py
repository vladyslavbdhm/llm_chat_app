import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from io import StringIO

# Configuración
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
st.set_page_config(page_title="Analizador de Datos con LLM", page_icon="📊")
st.title("📊 Interpretador y Explorador de Datos con LLM")

st.markdown("""
Subí un `.csv` o ingresá texto. Podés generar insights automáticos del dataset, y luego hacer preguntas o repreguntas sobre los datos.
""")

# Inicializar estados
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "df_clean" not in st.session_state:
    st.session_state.df_clean = None

if "csv_text" not in st.session_state:
    st.session_state.csv_text = ""

# Borrar conversación
if st.button("🧽 Borrar conversación"):
    st.session_state.chat_history = []

# Subida de archivo
uploaded_file = st.file_uploader("📎 Subí un archivo CSV", type="csv")
if uploaded_file:
    df_raw = pd.read_csv(uploaded_file)
    df_clean = df_raw.dropna()
    if len(df_clean) > 100:
        df_clean = df_clean.head(100)

    st.session_state.df_clean = df_clean
    st.session_state.csv_text = df_clean.to_csv(index=False)

    st.success(f"✅ Se usarán {len(df_clean)} filas sin nulos para el análisis.")
    st.subheader("📄 Vista previa del archivo")
    st.dataframe(df_clean.head(10))

# Entrada de texto manual
user_question = st.text_area("💬 Escribí tu pregunta o consulta (puede usar contexto anterior):", key="input_area", height=150)

# Botón: Generar insights generales del CSV
if st.button("🧠 Generar insights con LLM"):
    if st.session_state.csv_text:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

        messages = [
            SystemMessage(content="""
Eres un experto en análisis de datos. Recibirás una tabla de datos (máximo 100 filas sin nulos).
Tu tarea es:
- Detectar patrones o tendencias
- Señalar anomalías
- Explicar posibles causas
- Sugerir conclusiones generales

Responde en español, de forma clara, breve y estructurada.
"""),
            HumanMessage(content=f"Datos del archivo:\n{st.session_state.csv_text}")
        ]

        with st.spinner("🧠 Analizando datos..."):
            response = llm(messages)
            st.session_state.chat_history.append(("(INSIGHTS GENERALES)", response.content))
    else:
        st.warning("Por favor, subí un archivo válido antes de generar insights.")

# Botón: Preguntar o repreguntar (chat continuo)
if st.button("💬 Preguntar"):
    if user_question.strip():
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

        messages = [
            SystemMessage(content="""
Eres un experto en análisis de datos. Vas a recibir una pregunta relacionada con un análisis anterior. Respondé en español, de forma concisa y estructurada.
""")
        ]

        for user_msg, ai_msg in st.session_state.chat_history:
            messages.append(HumanMessage(content=user_msg))
            messages.append(HumanMessage(content=ai_msg))

        messages.append(HumanMessage(content=user_question.strip()))

        with st.spinner("✍️ Procesando pregunta..."):
            response = llm(messages)
            st.session_state.chat_history.append((user_question.strip(), response.content))
    else:
        st.warning("Por favor, escribí una pregunta antes de enviar.")

# Botón: Métricas básicas (EDA)
if st.button("📊 Ver métricas básicas") and st.session_state.df_clean is not None:
    df_clean = st.session_state.df_clean

    st.subheader("📋 Resumen general")

    total_rows = df_clean.shape[0]
    total_cols = df_clean.shape[1]
    total_cells = total_rows * total_cols
    total_nulls = df_clean.isnull().sum().sum()
    percent_nulls = (total_nulls / total_cells) * 100
    num_cols = df_clean.select_dtypes(include="number").columns.tolist()
    cat_cols = df_clean.select_dtypes(include=["object", "category"]).columns.tolist()

    summary_data = {
        "Total filas": [total_rows],
        "Total columnas": [total_cols],
        "Total nulos": [total_nulls],
        "Porcentaje nulos": [f"{percent_nulls:.2f}%"],
        "Columnas numéricas": [len(num_cols)],
        "Columnas categóricas": [len(cat_cols)],
        "Promedio global (num)": [df_clean[num_cols].mean().mean() if num_cols else "N/A"]
    }

    st.dataframe(pd.DataFrame(summary_data))

    # Mostrar df.info() como tabla
    st.subheader("📐 Estructura del DataFrame")
    df_info = pd.DataFrame({
        "Columna": df_clean.columns,
        "Non-Nulls": df_clean.notnull().sum().values,
        "Dtype": df_clean.dtypes.astype(str).values
    })
    st.dataframe(df_info)

    # Nulos por columna
    st.subheader("🕳️ Valores nulos por columna")
    st.dataframe(df_clean.isnull().sum().to_frame("Nulos"))

    # Estadísticas numéricas
    st.subheader("📈 Estadísticas numéricas")
    st.dataframe(df_clean.describe().T)


# Botón: Mostrar gráficos
if st.button("📈 Mostrar gráficos") and st.session_state.df_clean is not None:
    st.subheader("📊 Gráficos de columnas numéricas")
    numeric_cols = st.session_state.df_clean.select_dtypes(include="number").columns.tolist()

    if numeric_cols:
        for col in numeric_cols:
            fig, ax = plt.subplots()
            st.session_state.df_clean[col].hist(bins=20, ax=ax)
            ax.set_title(f"Distribución de {col}")
            st.pyplot(fig)
    else:
        st.info("No hay columnas numéricas para graficar.")


# Mostrar historial de conversación
if st.session_state.chat_history:
    st.divider()
    st.subheader("🗂 Historial de Conversación")

    for idx, (q, a) in enumerate(reversed(st.session_state.chat_history), 1):
        st.markdown(f"**🔎 Entrada {idx}:**")
        st.markdown("📝 **Consulta o datos:**")
        st.code(q[:1500] + "\n... (truncado)" if len(q) > 1500 else q)
        st.markdown("💬 **Respuesta del modelo:**")
        st.markdown(a)
        st.markdown("---")
