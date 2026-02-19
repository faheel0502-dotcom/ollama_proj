import streamlit as st
import ollama
import time

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Thinking Jargon Bot",
    page_icon="🧠",
    layout="centered"
)

# ---------- UI ----------
st.title("🧠 Thinking Jargon Bot")
st.caption("Simulated reasoning • Jargon output • 4-word answers")

# ---------- SESSION STATE ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- SYSTEM PROMPT ----------
SYSTEM_PROMPT = """
You are an AI assistant.

Rules you MUST follow:
- Use technical jargon.
- After internal reasoning, provide ONLY the final answer.
- Final answer MUST be exactly 4 words.
- Do NOT explain.
- Do NOT add punctuation.
- No emojis.
"""

# Initialize system message once
if not st.session_state.messages:
    st.session_state.messages.append(
        {"role": "system", "content": SYSTEM_PROMPT}
    )

# ---------- OLLAMA CALL ----------
def get_response(messages):
    response = ollama.chat(
        model="gemma3:4b",
        messages=messages,
        options={"temperature": 0.9}
    )
    return response["message"]["content"]

# ---------- CHAT HISTORY ----------
for msg in st.session_state.messages:
    if msg["role"] in ("user", "assistant"):
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# ---------- INPUT ----------
user_input = st.chat_input("Ask something complex...")

if user_input:
    # Save user input
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("assistant"):
        # ---- THINKING PHASE ----
        thinking = st.empty()
        thinking.write("🧠 Thinking...")
        time.sleep(1.2)

        thinking.write("🧠 Analyzing context vectors...")
        time.sleep(1.0)

        thinking.write("🧠 Compressing reasoning state...")
        time.sleep(0.8)

        # ---- MODEL RESPONSE ----
        raw_reply = get_response(st.session_state.messages)

        # ---- ENFORCE 4 WORDS ----
        words = raw_reply.strip().split()
        final_reply = " ".join(words[:4])

        thinking.write("🧠 Finalizing output...")
        time.sleep(0.5)

        thinking.empty()
        st.write(final_reply)

    # Save assistant reply
    st.session_state.messages.append(
        {"role": "assistant", "content": final_reply}
    )
