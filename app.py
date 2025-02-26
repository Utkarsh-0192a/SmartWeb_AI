import streamlit as st
from main import websearch
import ollama
from config import logger  # Use shared logger

st.title("question answering system")
st.write("Please enter your question below and the system will generate an answer for you.")

web_search = st.toggle("Enable Web Search", value=False)
searcher = websearch()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

ask_way = """
    You must follow these rules strictly:

    1. If the user message is a question and you have verifiable knowledge, answer concisely.
    2. If the question requires real-time data, external sources, predictions, or is beyond your knowledge, respond with only "false". Do not provide any explanation or additional text.
    3. If the user message is not a question, respond normally.

    Respond strictly according to these rules.

    User message:{}
"""



if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        modified_prompt = prompt

        if web_search:
            try:
                with st.spinner("Searching web for information..."):
                    modified_prompt = searcher.get_prompt(prompt)
                    logger.info("Modified prompt after web search generated.")
            except Exception as e:
                st.error(f"Error during web search: {e}")
                logger.error(f"Web search failed: {e}")
        else:
            modified_prompt = ask_way.format(prompt)
                
        full_response = ""
        message_placeholder = st.empty()
        with st.spinner("Generating response..."):
            for chunk in ollama.chat(
                model="llama3.2",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages[:-1] + [{"role": "user", "content": modified_prompt}]
                ],
                stream=True,
            ):
                full_response += chunk['message']['content']
                message_placeholder.markdown(full_response + "▌")
        
        # Check if the model's response indicates it doesn't have the knowledge
        if full_response.strip().lower() == "false" and not web_search:
            try:
                with st.spinner("Searching web for information..."):
                    modified_prompt = searcher.get_prompt(prompt)
                    logger.info("Modified prompt after web search generated.")
                    full_response = ""
                    for chunk in ollama.chat(
                        model="llama3.2",
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages[:-1] + [{"role": "user", "content": modified_prompt}]
                        ],
                        stream=True,
                    ):
                        full_response += chunk['message']['content']
                        message_placeholder.markdown(full_response + "▌")
            except Exception as e:
                st.error(f"Error during web search: {e}")
                logger.error(f"Web search failed: {e}")

        message_placeholder.markdown(full_response)
        logger.info("Response generated and displayed.")

    st.session_state.messages.append({"role": "assistant", "content": full_response})


