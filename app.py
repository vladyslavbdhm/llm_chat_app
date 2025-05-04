import streamlit as st
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# Leer la clave desde Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Configuración de la página
st.set_page_config(page_title="Chat con LLM", page_icon="🤖")
st.title("🤖 Chat con LLM (GPT-3.5 vía OpenAI)")

# Entrada del usuario
user_input = st.text_input("Escribe tu pregunta:")

if user_input:
    # Crear el modelo con LangChain
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0
    )

    # Mensajes del chat (incluye system prompt)
    messages = [
        SystemMessage(content="Eres un asistente útil que responde preguntas de forma clara, concisa y en español."),
        HumanMessage(content=user_input)
    ]

    with st.spinner("Pensando..."):
        response = llm(messages)
        st.success(response.content)
