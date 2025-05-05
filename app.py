import streamlit as st
import os
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# Leer clave API
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Configuración general
st.set_page_config(page_title="Analizador de Datos con LLM", page_icon="📊")
st.title("📊 Interpretador de Resultados de Datos con LLM")

st.markdown("""
Este asistente te ayuda a **interpretar resultados de análisis de datos**.
Pegá métricas, KPIs, estadísticas o subí un archivo `.csv` con datos, y recibirás una explicación clara en lenguaje natural.
""")

# Mostrar ejemplo dentro de un expander
with st.expander("📌 Ver ejemplo de entrada"):
    st.markdown("""
    ```
    Promedio de ventas: 1245 €
    Desviación estándar: 232 €
    Ventas de abril: 1020 € (-15% respecto a marzo)
    Top productos: A (1520 €), B (1340 €), C (900 €)
    ```
    """)

# Inicializar historial si no existe
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Botón para limpiar conversación
if st.button("🧽 Borrar conversación"):
    st.session_state.chat_history = []

# Carga de archivo CSV
uploaded_file = st.file_uploader("📎 O subir un archivo CSV con métricas", type="csv")
csv_text = ""

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Vista previa del archivo:")
    st.dataframe(df)

    # Extraer primeras filas como markdown
    csv_text = df.head(5).to_markdown(index=False)

    st.markdown("🧾 Fragmento de datos extraído para el modelo:")
    st.code(csv_text, language="markdown")

# Entrada de texto manual
user_input = st.text_area(
    "✏️ También podés escribir o pegar resultados directamente:",
    key="input_area",
    height=150
)

# Botón para interpretar
if st.button("Interpretar"):
    if user_input.strip() or csv_text:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

        # Prompt de sistema
        messages = [SystemMessage(content="""
Eres un experto en análisis de datos. Recibirás resultados estadísticos, métricas de negocio o resúmenes de dashboards.
Tu tarea es explicar en lenguaje claro y breve:
1. Qué indican los datos.
2. Si hay algo inusual.
3. Cualquier conclusión que se pueda sacar.

Responde en español, de forma ordenada y usando bullets o subtítulos si es posible.
""")]

        # Historial previo (para contexto)
        for user_msg, ai_msg in st.session_state.chat_history:
            messages.append(HumanMessage(content=user_msg))
            messages.append(HumanMessage(content=ai_msg))

        # Construir input combinado (csv + texto manual)
        combined_input = ""
        if csv_text:
            combined_input += f"Datos del archivo:\n{csv_text}\n\n"
        if user_input.strip():
            combined_input += f"Comentarios adicionales:\n{user_input.strip()}"

        messages.append(HumanMessage(content=combined_input))

        with st.spinner("Analizando..."):
            response = llm(messages)
            st.session_state.chat_history.append((combined_input, response.content))
    else:
        st.warning("Por favor, escribí algo o subí un archivo antes de interpretar.")

# Mostrar historial
# Mostrar historial
if st.session_state.chat_history:
    st.divider()
    st.subheader("🗂 Historial de Interpretaciones")

    for idx, (q, a) in enumerate(reversed(st.session_state.chat_history), 1):
        st.markdown(f"**🔎 Consulta {idx}:**")
        st.write("📝 **Entrada:**")
        st.code(q, language="markdown")

        st.markdown("💬 **Respuesta:**")
        st.markdown(a)
        st.markdown("---")

