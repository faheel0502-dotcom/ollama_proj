import streamlit as st
import ollama

st.title("chatbot Faheel")

st.session_state.messages =[] #message saving system
user_input = st.text_input("You:")

if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})

    response = ollama.chat(
         model = "gemma3:4b",
         messages = st.session_state.messages
    )

    reply = response["message"]["content"]
    st.session_state.messages.append({"role":"assistant","content":reply})

    st.write("Bot: ",reply)