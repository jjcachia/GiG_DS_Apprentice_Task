import os
import streamlit as st
import uuid

from src.user import User
from src.chatbot import ChatbotV1
from src.chat import Chat

# Set the data directory
data_dir = os.path.abspath("data")

# Initialize session state
if "user" not in st.session_state:
    st.session_state.user = None

if "chats" not in st.session_state:
    st.session_state.chats = {}  # chat_id → Chat object

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

# Initialise by asking for a username
if st.session_state.user is None:
    username = st.text_input("Enter your name to start:", key="username")
    if username:
        st.session_state.user = User(username=username)
        chat_id = str(uuid.uuid4())
        st.session_state.chats[chat_id] = Chat(user=st.session_state.user, chatbot=ChatbotV1(data_dir))
        st.session_state.current_chat_id = chat_id
        st.rerun()  # Rerun to update the UI after setting the user

# Once user is set, show chat UI
if st.session_state.user:

    # Select current chat
    current_chat = st.session_state.chats[st.session_state.current_chat_id]

    # Main Chat UI
    st.subheader(f"GiG's Knowledge Base Chatbot V0.1 - Chat {list(st.session_state.chats).index(st.session_state.current_chat_id) + 1}")
    st.markdown("---")

    # Display chat prompt
    user_question = st.chat_input("Ask a question:")
    if user_question:
        answer = current_chat.ask(user_question)

    # Display chat history
    for message in current_chat.get_chat_history():
        st.write(f"**{message['speaker']}:** {message['text']}")
    
    # Display Bar UI
    # New Chat Button
    if st.sidebar.button("New Chat", use_container_width=True):
        chat_id = str(uuid.uuid4())
        st.session_state.chats[chat_id] = Chat(user=st.session_state.user, chatbot=ChatbotV1(data_dir))
        st.session_state.current_chat_id = chat_id
        st.rerun()  # Rerun to update the UI with the new chat

    st.sidebar.markdown("---")

    # Navigation through existing chats
    for chat_id in st.session_state.chats:
        if st.sidebar.button(f"Chat {list(st.session_state.chats).index(chat_id) + 1}", key=chat_id, use_container_width=True):
            st.session_state.current_chat_id = chat_id
            st.rerun()  # Rerun to update the UI with the selected chat

    
