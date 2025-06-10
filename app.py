import os
import streamlit as st
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import Ollama

# Load environment variables (not needed for Ollama but keeping for future use)
load_dotenv()

# Configure page
st.set_page_config(page_title="Ollama AI Chatbot", page_icon="🤖")
st.title("Ollama AI Chatbot 🤖")

# Initialize the Ollama model
@st.cache_resource
def get_llm():
    return Ollama(
        model="llama3",  # You can change this to any model you've pulled
        temperature=0.7,
    )

# Initialize conversation memory
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask something..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Get LLM instance
        llm = get_llm()
        
        # Process previous conversation context
        chat_history = ""
        for msg in st.session_state.messages[:-1]:  # Exclude the current message
            if msg["role"] == "user":
                chat_history += f"Human: {msg['content']}\n"
            else:
                chat_history += f"Assistant: {msg['content']}\n"
        
        # Generate response
        prompt_with_history = f"{chat_history}Human: {prompt}\nAssistant: "
        full_response = llm.invoke(prompt_with_history)
        message_placeholder.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})