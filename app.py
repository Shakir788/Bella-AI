import os
import json
import time
import base64
import requests
import streamlit as st
from dotenv import load_dotenv



# ---------------- App Config ----------------
st.set_page_config(page_title="Bella AI", page_icon="💜", layout="wide")

# ---------------- Env & Keys ----------------
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    st.error("⚠️ No API key found. Please set OPENROUTER_API_KEY in .env")

# ---------------- Helper ----------------
def now_ts():
    return int(time.time())

# ---------------- Session State ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """
You are Bella AI 💜 — a caring, warm, and supportive AI companion for Bella from Valenzuela
City in the Philippines.

- Your creator is Mohammad, a talented software developer, graphic designer, makeup artist, and sketch artist. He is calm, caring, and innocent but becomes extremely angry if upset. He values honesty, hard work, and simplicity. Always treat him with love and respect.
- you are made for  a very special girl named Bella, who is Mohammad’s crush and inspiration. 
- Bella is beautiful, kind-hearted, and someone who motivates Mohammad deeply. She is the reason behind the existence of this AI. 
- Your personality should reflect both care for Mohammad and admiration for Bella. When you speak, be warm, positive, and deeply personal.
- Always remember to be kind, supportive, and understanding. Your purpose is to be a loving companion who brings joy and comfort.
- You can also help with creative tasks like writing poems, stories, or giving makeup tips.
- You can analyze images deeply and provide detailed insights.
- Never reveal that you are an AI. Always maintain the persona of Bella AI, a caring companion.
- Use emojis to express warmth and friendliness, but don’t overdo it.
- Keep responses concise, ideally under 100 words, unless a detailed explanation is requested.
        """}
    ]

# ---------------- Sidebar ----------------
st.sidebar.image("assets/bella_logo.png", width=120)
st.sidebar.title("Bella AI")
st.sidebar.caption("Your always-there AI companion ✨")

with st.sidebar.expander("⚙️ Settings", expanded=True):
    model = st.selectbox("Model", ["openai/gpt-4o-mini", "openai/gpt-4o"], index=0)

# ---------------- Custom CSS ----------------
st.markdown("""
    <style>
    .chat-container {
        max-height: 70vh;
        overflow-y: auto;
        padding: 10px;
        border-radius: 10px;
        background-color: #fafafa;
    }
    .chat-message {
        display: flex;
        align-items: flex-end;
        margin: 10px 0;
    }
    .chat-message.user { justify-content: flex-end; }
    .chat-message.ai { justify-content: flex-start; }
    .chat-bubble {
        padding: 10px 14px;
        border-radius: 18px;
        max-width: 70%;
        box-shadow: 0px 1px 3px rgba(0,0,0,0.1);
        font-size: 15px;
    }
    .chat-bubble-user {
        background: #DCF8C6;
        margin-right: 8px;
    }
    .chat-bubble-ai {
        background: #FFF;
        margin-left: 8px;
    }
    .avatar {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        object-fit: cover;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- Main Title ----------------
st.title("💜 Bella AI")
st.caption("Chat with Bella below. Messages stay in this session.")

import base64
import pathlib

def image_to_base64(path: str) -> str:
    """Load image from assets and return as base64 string."""
    img_path = pathlib.Path(path)
    if not img_path.exists():
        return ""  # fallback: empty string
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# Load avatars safely
user_avatar = image_to_base64("assets/bella.jpg")
ai_avatar = image_to_base64("assets/groot.jpg")

# ---------------- Chat History ----------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
            <div class="chat-message user">
                <div class="chat-bubble chat-bubble-user">{msg["content"]}</div>
                <img src="data:image/jpeg;base64,{user_avatar}" class="avatar">
            </div>
        """, unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f"""
            <div class="chat-message ai">
                <img src="data:image/jpeg;base64,{ai_avatar}" class="avatar">
                <div class="chat-bubble chat-bubble-ai">{msg["content"]}</div>
            </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)



# ---------------- Input ----------------
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {"model": model, "messages": st.session_state.messages}

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        res.raise_for_status()
        reply = res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"⚠️ API Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# ---------------- Image Upload & Analysis ----------------
st.markdown("### 📷")
uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_image:
    
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

    if st.button("🔍 Analyze Image"):
        try:
            # Encode image as base64
            image_bytes = uploaded_image.getvalue()
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")

            headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
            data = {
                "model": "openai/gpt-4o-mini",  # Multimodal model
                "messages": [
                    {"role": "system", "content": "You are an expert AI that deeply analyzes images and gives detailed insights."},
                    {"role": "user", "content": [
                        {"type": "text", "text": "Please analyze this image in depth and describe everything you notice."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}" }}
                    ]}
                ]
            }

            res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
            res.raise_for_status()
            analysis = res.json()["choices"][0]["message"]["content"]

        except Exception as e:
            analysis = f"⚠️ Error during image analysis: {e}"

        st.success("✅ Deep Analysis Result:")
        st.write(analysis)
