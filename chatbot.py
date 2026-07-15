import streamlit as st

from config import DEFAULT_CHAT_MODEL
from ollama_client import OllamaError, chat, list_models

st.set_page_config(
    page_title="AI Chatbot",
    page_icon=" ",
    layout="centered",
)

st.title("AI Chatbot")
st.caption("Powered by Ollama")

st.sidebar.title("Settings")

try:
    available_models = list_models()
except OllamaError as exc:
    st.error(str(exc))
    st.stop()

if not available_models:
    st.error("No Ollama models found. Install one with `ollama pull llama3.2` or `ollama pull gemma3`.")
    st.stop()

default_model_index = (
    available_models.index(DEFAULT_CHAT_MODEL)
    if DEFAULT_CHAT_MODEL in available_models
    else 0
)

model_name = st.sidebar.selectbox(
    "Select Model",
    available_models,
    index=default_model_index,
)

temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=2.0,
    value=0.7,
    step=0.1,
)

max_tokens = st.sidebar.slider(
    "Maximum Output Tokens",
    min_value=100,
    max_value=2048,
    value=512,
    step=100,
)

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask anything...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        answer = chat(
            st.session_state.messages,
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except OllamaError as exc:
        st.error(str(exc))
        st.stop()

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

chat_text = ""

for message in st.session_state.messages:
    chat_text += f"{message['role'].upper()}:\n{message['content']}\n\n"

st.sidebar.download_button(
    label="Download Chat",
    data=chat_text,
    file_name="chat_history.txt",
    mime="text/plain",
)
