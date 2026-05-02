import streamlit as st
from bot_logic import get_bot_response

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="WanderBot – Travel Assistant",
    page_icon="✈️",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }

.stApp {
    background: linear-gradient(160deg, #e8f4fd 0%, #ffffff 60%, #dbeeff 100%);
}

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #1a8fe3 0%, #45b4f5 60%, #7dd4fc 100%);
    border-radius: 20px;
    padding: 28px 32px 22px;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(26,143,227,0.18);
    text-align: center;
}
.hero-banner h1 { color: #fff; font-size: 2.2rem; font-weight: 800; margin: 0 0 4px; }
.hero-banner p  { color: rgba(255,255,255,0.88); font-size: 1rem; margin: 0; }

/* Chat bubbles */
.chat-user { display: flex; justify-content: flex-end; margin: 10px 0; }
.chat-user .bubble {
    background: linear-gradient(135deg, #1a8fe3, #45b4f5);
    color: #fff;
    padding: 12px 18px;
    border-radius: 20px 20px 4px 20px;
    max-width: 78%;
    font-size: 0.95rem;
    line-height: 1.5;
    box-shadow: 0 3px 12px rgba(26,143,227,0.22);
}
.chat-bot { display: flex; justify-content: flex-start; margin: 10px 0; align-items: flex-start; gap: 10px; }
.bot-avatar {
    background: linear-gradient(135deg, #1a8fe3, #7dd4fc);
    color: #fff;
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
    margin-top: 2px;
    box-shadow: 0 2px 8px rgba(26,143,227,0.2);
}
.chat-bot .bubble {
    background: #fff;
    color: #1a2b4a;
    padding: 12px 18px;
    border-radius: 20px 20px 20px 4px;
    max-width: 78%;
    font-size: 0.95rem;
    line-height: 1.55;
    box-shadow: 0 3px 14px rgba(26,143,227,0.10);
    border: 1px solid #d6eaf8;
}

/* Chat container */
.chat-container {
    background: rgba(255,255,255,0.55);
    border-radius: 16px;
    padding: 18px 16px 8px;
    min-height: 320px;
    max-height: 420px;
    overflow-y: auto;
    border: 1px solid #c5e3f7;
    margin-bottom: 16px;
    backdrop-filter: blur(6px);
}

/* Input */
.stTextInput > div > div > input {
    border-radius: 50px !important;
    border: 2px solid #90cff5 !important;
    padding: 12px 20px !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.95rem !important;
    background: #fff !important;
    color: #1a2b4a !important;
}
.stTextInput > div > div > input:focus {
    border-color: #1a8fe3 !important;
    box-shadow: 0 0 0 3px rgba(26,143,227,0.12) !important;
}

/* Button */
.stButton > button {
    border-radius: 50px !important;
    background: linear-gradient(135deg, #1a8fe3, #45b4f5) !important;
    color: #fff !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 10px 28px !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(26,143,227,0.28) !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(26,143,227,0.36) !important;
}

/* Sidebar */
[data-testid="stSidebar"] { background: linear-gradient(180deg, #1a8fe3 0%, #45b4f5 100%) !important; }
[data-testid="stSidebar"] * { color: #fff !important; }
[data-testid="stSidebar"] .stTextInput > div > div > input {
    color: #1a2b4a !important;
    background: #fff !important;
}

/* Chips */
.tip-chip {
    display: inline-block;
    background: rgba(26,143,227,0.10);
    border: 1px solid #b3d9f7;
    color: #1a6db0;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.82rem;
    font-weight: 600;
    margin: 3px;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ✈️ WanderBot")
    st.markdown("Your AI-powered travel companion")
    st.divider()
    api_key = st.text_input("🔑 Gemini API Key", type="password", placeholder="Paste your key here")
    st.markdown("---")
    st.markdown("**What I can help with:**")
    for tip in ["🗺️ Trip itineraries", "🏨 Hotel recommendations",
                 "🛂 Visa & documents", "💰 Budget planning",
                 "🌤️ Best travel seasons", "🍜 Local food & culture"]:
        st.markdown(f"- {tip}")
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Hero banner ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <h1>✈️ WanderBot</h1>
  <p>Your personal AI travel planner — itineraries, tips, destinations & more</p>
</div>
""", unsafe_allow_html=True)

# ── Chat display ──────────────────────────────────────────────────────────────
chat_html = '<div class="chat-container">'

if not st.session_state.messages:
    chat_html += """
    <div class="chat-bot">
      <div class="bot-avatar">🌍</div>
      <div class="bubble">
        Hi there! 👋 I'm <strong>WanderBot</strong>, your travel assistant.<br>
        Ask me about destinations, itineraries, hotels, visa tips, packing lists — anything travel! ✈️
      </div>
    </div>"""
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            chat_html += f'<div class="chat-user"><div class="bubble">{msg["content"]}</div></div>'
        else:
            content = msg["content"].replace("\n", "<br>")
            chat_html += f'<div class="chat-bot"><div class="bot-avatar">🌍</div><div class="bubble">{content}</div></div>'

chat_html += "</div>"
st.markdown(chat_html, unsafe_allow_html=True)

# ── Quick suggestion chips ────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:10px;">
  <span class="tip-chip">🗺️ 7-day Paris itinerary</span>
  <span class="tip-chip">🏝️ Best beaches in Asia</span>
  <span class="tip-chip">💰 Budget Europe travel</span>
  <span class="tip-chip">🛂 India visa tips</span>
</div>
""", unsafe_allow_html=True)

# ── Input row ─────────────────────────────────────────────────────────────────
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        "", placeholder="Ask me about your next adventure... 🌏",
        label_visibility="collapsed", key="user_input"
    )
with col2:
    send = st.button("Send ➤")

# ── Handle send ───────────────────────────────────────────────────────────────
if send and user_input.strip():
    if not api_key:
        st.warning("⚠️ Please enter your Gemini API key in the sidebar.")
    else:
        # Save user message
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})

        # Get reply from bot_logic
        reply = get_bot_response(
            api_key=api_key,
            messages=st.session_state.messages[:-1],   # history without current msg
            user_input=user_input.strip(),
        )

        # Save bot reply
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
