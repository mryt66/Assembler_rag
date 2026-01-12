import streamlit as st
import requests

# Configuration
API_URL = "http://localhost:8000/chat"

st.set_page_config(
    page_title="Assembler RAG Chatbot", page_icon="🤖", layout="centered"
)

st.title("🤖 Assembler RAG Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask about Assembler..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # Prepare payload
            # The API expects 'history' as a list of dicts with 'role' and 'content'/'message'
            # We exclude the current prompt from history sent to API if the API handles it separately as 'query'
            # But looking at api.py, it takes 'query' and 'history'.
            # Usually history should contain previous turns.

            history_payload = st.session_state.messages[
                :-1
            ]  # Exclude the just added user message

            payload = {"query": prompt, "history": history_payload}

            with st.spinner("Thinking..."):
                response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                data = response.json()
                answer = data.get("response", "No response received.")
                message_placeholder.markdown(answer)
                full_response = answer
            else:
                error_msg = f"Error {response.status_code}: {response.text}"
                message_placeholder.error(error_msg)
                full_response = error_msg

        except requests.exceptions.ConnectionError:
            error_msg = "❌ Could not connect to the API. Is 'api.py' running?"
            message_placeholder.error(error_msg)
            full_response = error_msg
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            message_placeholder.error(error_msg)
            full_response = error_msg

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

