import streamlit as st
from groq import Groq

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="HarsH AI - Ollama ChatGPT Clone",
    page_icon="🤖",
    layout="centered"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
.block-container { max-width: 850px; padding-top: 2rem; }
.hero-card {
    background: linear-gradient(135deg, #111827, #020617);
    border: 1px solid rgba(34,197,94,0.40);
    border-radius: 24px;
    padding: 26px;
    margin-bottom: 20px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.20);
}
.brand-title { font-size: 34px; font-weight: 800; color: #f8fafc; margin-bottom: 6px; }
.brand-subtitle { font-size: 16px; color: #d1d5db; }
.green { color: #22c55e; }
.small-note { color: #9ca3af; font-size: 13px; margin-top: 8px; }
.stButton button {
    border-radius: 12px;
    background-color: #22c55e;
    color: #052e16;
    font-weight: 700;
    border: none;
}
.stButton button:hover { background-color: #16a34a; color: #052e16; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="hero-card">
    <div class="brand-title">HarsH AI <span class="green">:Local AI Chatbot</span></div>
    <div class="brand-subtitle">Hii Iam HarsH.Ask me Anything.</div>
    <div class="small-note">I Can help you in the form of text </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar Settings
# -----------------------------
with st.sidebar:
    st.title("⚙️ Settings")

    groq_api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="Enter your Groq API key..."
    )

    model = st.selectbox(
        "Choose Model",
        ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768", "gemma2-9b-it"],
        index=0
    )

    temperature = st.slider(
        "Temperature / Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="0 = focused/robotic, 1 = creative"
    )

    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful AI assistant. Explain concepts clearly and simply. When useful, respond with examples.",
        height=120
    )

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("### Notes")
    st.markdown("- Groq runs models in the cloud")
    st.markdown("- Get free API key at console.groq.com")
    st.markdown("- Temperature = creativity dial")
    st.markdown("- LLMs are stateless unless we send history")

# -----------------------------
# Check API Key
# -----------------------------
if not groq_api_key:
    st.warning("👈 Please enter your Groq API key in the sidebar to start chatting.")
    st.markdown("Get a free API key at [console.groq.com](https://console.groq.com)")
    st.stop()

# -----------------------------
# Init Groq Client
# -----------------------------
client = Groq(api_key=groq_api_key)

# -----------------------------
# Session State / Memory
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Show Chat History
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Chat Input
# -----------------------------
user_prompt = st.chat_input("Ask anything... Try Telugu also: 'Generative AI ante enti?'")

if user_prompt:
    # 1. Display user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # 2. Build messages list
    messages_for_groq = [{"role": "system", "content": system_prompt}]
    messages_for_groq.extend(st.session_state.messages)

    # 3. Stream assistant response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            stream = client.chat.completions.create(
                model=model,
                messages=messages_for_groq,
                temperature=temperature,
                stream=True,
                max_tokens=1024
            )

            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    full_response += content
                    response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"Error: {str(e)}"
            response_placeholder.error(full_response)

    # 4. Store assistant response
    st.session_state.messages.append({"role": "assistant", "content": full_response})
