import streamlit as st
import time
from langchain_community.chat_message_histories import ChatMessageHistory
from src.chat import call_llm, gpt_llm_model, claude_llm_model
from src.prompt import get_general_promt

st.set_page_config(page_title="Chatbot Interface", page_icon="😊")
with open('src/static/styles.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

if 'chat_history_gpt' not in st.session_state:
    st.session_state.chat_history_gpt = ChatMessageHistory()
if 'chat_history_claude' not in st.session_state:
    st.session_state.chat_history_claude = ChatMessageHistory()
if 'debate_topic' not in st.session_state:
    st.session_state.debate_topic = None
if 'gpt_llm_model' not in st.session_state:
    st.session_state.gpt_llm_model = gpt_llm_model
if 'claude_llm_model' not in st.session_state:
    st.session_state.claude_llm_model = gpt_llm_model
if 'systeme_prompt' not in st.session_state:
    st.session_state.systeme_prompt = get_general_promt()


# Header section with profile picture
col1, col2, col3 = st.columns([1, 5, 1])
with col1:
    st.image("src/static/claude.png", width=100)
with col2:
    st.markdown("<div class='header'>CLAUDE vs GPT </div>", unsafe_allow_html=True)
with col3:
    st.image("src/static/gpt.png", width=100)

# Function to display chat messages
def display_message(message, is_user=True):
    if is_user:
        chat_container.markdown(f"<div class='chat-bubble user'>{message}</div>", unsafe_allow_html=True)
    else:
        chat_container.markdown(f"<div class='chat-bubble bot'>{message}</div>", unsafe_allow_html=True)

# User input form for debate topic
debate_topic_input = st.text_input("Entrez le sujet de débat:", key="debate_topic_input")

if st.button("Commencer la conversation"):
    
    debate_topic = debate_topic_input.strip()
    if debate_topic:
        st.markdown(f"<h4 style='text-align: center;'>Sujet de débat : {debate_topic}</h4>", unsafe_allow_html=True)
        time.sleep(1)
        # Clear previous chat history
        st.session_state.chat_history = []
        st.session_state.debate_topic = debate_topic

        # Container for the chat messages
        chat_container = st.container()
        chat_container.markdown('<div class="chat-container">', unsafe_allow_html=True)

        st.session_state.chat_history_gpt.add_user_message(st.session_state.debate_topic) 

        start_time = time.time()
        num_messages = 0 
        while True:
            # Calculate elapsed time
            elapsed_time = time.time() - start_time
            if elapsed_time >= 300:  # 300 seconds = 5 minutes
                break  # End the conversation if 5 minutes have passed
            
            if num_messages > 0 :
                st.session_state.chat_history_gpt.add_user_message(chatbot2_message)

            chatbot1_message = call_llm(st.session_state.gpt_llm_model, st.session_state.systeme_prompt , st.session_state.chat_history_gpt)
            st.session_state.chat_history_gpt.add_ai_message(chatbot1_message)
            
            chatbot1_message_display = (
                                f"<div >"
                                f"<strong>GPT</strong><br>{chatbot1_message}"
                                "</div>"
                                )
            display_message(chatbot1_message_display, True)


            st.session_state.chat_history_claude.add_user_message(chatbot1_message)
            chatbot2_message = call_llm(st.session_state.claude_llm_model, st.session_state.systeme_prompt , st.session_state.chat_history_claude)
            st.session_state.chat_history_claude.add_ai_message(chatbot2_message) 
            time.sleep(5)  

            chatbot2_message_dispalay = (
                                f"<div >"
                                f"<strong>CLAUDE</strong><br>{chatbot2_message}"
                                "</div>"
                                )
            display_message(chatbot2_message_dispalay, False)
            
            time.sleep(5)  
            
            num_messages += 1
            
