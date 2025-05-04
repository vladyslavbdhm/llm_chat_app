import streamlit as st
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# Leer la clave desde secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Página
st.set_page_config(page_title="Analizador de Datos con LLM", page_icon="📊")
st.title("📊 Interpretador de Resultados de Datos con LLM")

st.markdown("""
Este asistente te ayuda a **interpretar resultados de análisis de datos**.
Pegá métricas, KPIs, estadísticas o resúmenes de dashboards, y recibirás una explicación clara en lenguaje natural.
""")

# Inicializar historial si no existe
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Botón para limpiar conversación
if st.button("🧽 Borrar conversación"):
    st.session_state.chat_history = []

# Entrada del usuario
user_input = st.text_area("📥 Pegá aquí tus resultados de análisis o métricas:")

# Botón para interpretar
if st.button("Interpretar"):
    if user_input:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

        # Crear lista de mensajes desde el historial
        messages = [SystemMessage(content="""
Eres un experto en análisis de datos. Recibirás resultados estadísticos, métricas de negocio o resúmenes de dashboards.
Tu tarea es explicar en lenguaje claro y breve:
1. Qué indican los datos.
2. Si hay algo inusual.
3. Cualquier conclusión que se pueda sacar.

Responde en español, de forma ordenada y usando bullets o subtítulos si es posible.
""")]

        # Agregar historial como contexto
        for user_msg, ai_msg in st.session_state.chat_history:
            messages.append(HumanMessage(content=user_msg))
            messages.append(HumanMessage(content=ai_msg))  # opción simple si no usamos AIMessage

        # Mensaje actual del usuario
        messages.append(HumanMessage(content=user_input))

        with st.spinner("Analizando..."):
            response = llm(messages)
            st.session_state.chat_history.append((user_input, response.content))
    else:
        st.warning("Por favor, pegá algún contenido antes de interpretar.")

# Mostrar historial con formato visual
if st.session_state.chat_history:
    st.divider()
    st.subheader("🗂 Historial de Interpretaciones")
    for idx, (q, a) in enumerate(reversed(st.session_state.chat_history), 1):
        st.markdown(f"**🔎 Consulta {idx}:**")
        st.write(f"📝 **Entrada:**")
        st.code(q, language="markdown")

        # 🔍 Detección simple de términos críticos
        alert_words = ["descenso", "caída", "disminución", "alarma", "riesgo", "alerta", "bajo"]
        highlight = any(word in a.lower() for word in alert_words)

        st.markdown("💬 **Respuesta:**")
        if highlight:
            st.markdown(f"<div style='color: red'>{a}</div>", unsafe_allow_html=True)
        else:
            st.markdown(a)

        st.markdown("---")
