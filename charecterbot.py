import streamlit as st
import ollama

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Any Character AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 🧪 AI Controls")

    temperature = st.slider(
        "Creativity (Temperature)",
        0.0, 1.5, 0.7, 0.1
    )
    st.markdown(f"**Current value:** `{temperature}`")

    st.divider()
    exit_clicked = st.button("🚪 Exit Character", use_container_width=True)

# ---------- GLOBAL CSS ----------
st.markdown("""
<style>
header, footer { display: none !important; }

html, body, .stApp {
    margin: 0;
    padding: 0;
    height: 100%;
    background: linear-gradient(-45deg,#7b2ff7,#5f2cfa,#4a00e0,#8e2de2);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
    overflow-x: hidden;
}

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.block-container {
    max-width: 820px;
    margin: 0 auto;
    padding: 2rem 1.8rem 8rem;
}

/* TITLE */
h1 {
    text-align: center;
    font-size: 2.4rem;
    margin-bottom: 1rem;
    text-shadow: 0 0 18px rgba(180,140,255,0.9);
}

/* CHARACTER BANNER */
.character-box {
    background: linear-gradient(135deg,#3b82f6,#8b5cf6);
    padding: 12px;
    border-radius: 18px;
    text-align: center;
    font-weight: 600;
    box-shadow: 0 0 28px rgba(130,120,255,0.8);
    margin-bottom: 18px;
}

/* CHAT */
.chat-wrapper {
    display: flex;
    flex-direction: column;
    gap: 14px;
    padding-bottom: 80px;
}

.msg-row {
    display: flex;
    align-items: flex-end;
    gap: 10px;
}

.avatar {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    background: rgba(255,255,255,0.3);
}

.bubble {
    padding: 10px 14px;
    border-radius: 14px;
    font-size: 14.5px;
    line-height: 1.45;
    max-width: 65%;
    word-wrap: break-word;
}

/* USER */
.user-row { justify-content: flex-end; }
.user-bubble {
    background: linear-gradient(135deg,#22d3ee,#3b82f6);
    color: #001b33;
}

/* BOT */
.bot-row { justify-content: flex-start; }
.bot-bubble {
    background: rgba(255,255,255,0.45);
    color: #111;
    backdrop-filter: blur(10px);
}

/* CHAT INPUT */
[data-testid="stChatInput"] {
    position: fixed;
    bottom: 14px;
    left: 50%;
    transform: translateX(-50%);
    width: min(820px, 95%);
    background: rgba(0,0,0,0.55);
    backdrop-filter: blur(12px);
    border-radius: 18px;
    padding: 6px 10px;
    border: 1px solid rgba(255,255,255,0.25);
    z-index: 999;
}

textarea, input {
    background: transparent !important;
    color: white !important;
    border: none !important;
    font-size: 14.5px !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("✨ Any Character AI ✨")

# ---------- SESSION STATE ----------
if "character_memory" not in st.session_state:
    st.session_state.character_memory = {}

if "current_character" not in st.session_state:
    st.session_state.current_character = None

# ---------- EXIT ----------
if exit_clicked:
    st.session_state.current_character = None
    st.rerun()

# ---------- OLLAMA ----------
def chat_with_ollama(messages):
    res = ollama.chat(
        model="gemma3:4b",
        messages=messages,
        options={"temperature": temperature}
    )
    return res["message"]["content"]

# ---------- MAIN ----------
if st.session_state.current_character is None:
    st.markdown("<div class='character-box'>🎭 SUMMON A CHARACTER 🎭</div>", unsafe_allow_html=True)
    character = st.chat_input("Type a character name and press Enter")

    if character:
        st.session_state.current_character = character
        st.session_state.character_memory.setdefault(
            character,
            [{"role":"system","content":f"You are roleplaying as {character}. Stay fully in character."}]
        )
        st.rerun()

else:
    character = st.session_state.current_character
    messages = st.session_state.character_memory[character]

    st.markdown(f"<div class='character-box'>⚡ {character} MODE ⚡</div>", unsafe_allow_html=True)
    st.markdown("<div class='chat-wrapper'>", unsafe_allow_html=True)

    for m in messages:
        if m["role"] == "user":
            st.markdown(f"""
            <div class="msg-row user-row">
                <div class="bubble user-bubble">{m['content']}</div>
                <div class="avatar">🧑</div>
            </div>
            """, unsafe_allow_html=True)

        elif m["role"] == "assistant":
            st.markdown(f"""
            <div class="msg-row bot-row">
                <div class="avatar">🤖</div>
                <div class="bubble bot-bubble">{m['content']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    user_input = st.chat_input("💬 Talk…")

    if user_input:
        messages.append({"role":"user","content":user_input})
        reply = chat_with_ollama(messages)
        messages.append({"role":"assistant","content":reply})
        st.rerun()
