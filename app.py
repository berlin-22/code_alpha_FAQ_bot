import streamlit as st
import time
from chatbot import FAQChatbot

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FAQ Assistant",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Custom CSS: Modern Clean Minimalist Design (Strictly Zero Blue) ───────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        color: #18181b !important;
    }

    .stApp {
        background-color: #f7f7f8 !important;
    }

    #MainMenu, header, footer, .stDeployButton {
        display: none !important;
    }

    /* Brand Header */
    .brand-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 1.25rem;
        margin-bottom: 1.25rem;
        border-bottom: 1px solid #e4e4e7;
    }
    .brand-title-wrap {
        display: flex;
        flex-direction: column;
        gap: 0.2rem;
    }
    .brand-title {
        font-size: 1.35rem;
        font-weight: 600;
        color: #18181b;
        letter-spacing: -0.025em;
        margin: 0;
    }
    .brand-subtitle {
        font-size: 0.82rem;
        color: #71717a;
        margin: 0;
    }
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        font-size: 0.75rem;
        font-weight: 500;
        color: #52525b;
        background: #ffffff;
        border: 1px solid #e4e4e7;
        padding: 0.3rem 0.75rem;
        border-radius: 9999px;
    }
    .status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: #10b981;
    }

    /* Confidence Badges */
    .confidence-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 500;
        margin-top: 8px;
    }
    .conf-high {
        background: #f0fdf4;
        color: #15803d;
        border: 1px solid #bbf7d0;
    }
    .conf-medium {
        background: #fefce8;
        color: #a16207;
        border: 1px solid #fef08a;
    }
    .conf-low {
        background: #f4f4f5;
        color: #71717a;
        border: 1px solid #e4e4e7;
    }

    /* Chat message styling */
    div[data-testid="stChatMessage"] {
        background: #ffffff !important;
        border: 1px solid #e4e4e7 !important;
        border-radius: 10px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
        padding: 1rem !important;
        margin-bottom: 0.75rem !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e4e4e7 !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem !important;
    }

    /* Buttons */
    button[data-testid="stBaseButton-secondary"] {
        background-color: #ffffff !important;
        color: #3f3f46 !important;
        border: 1px solid #e4e4e7 !important;
        border-radius: 6px !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        transition: all 0.15s ease !important;
    }
    button[data-testid="stBaseButton-secondary"]:hover {
        background-color: #f4f4f5 !important;
        border-color: #d4d4d8 !important;
        color: #18181b !important;
    }

    /* Chat Input */
    div[data-testid="stChatInput"] {
        border-color: #e4e4e7 !important;
    }
    div[data-testid="stChatInput"]:focus-within {
        border-color: #18181b !important;
    }

    .sidebar-heading {
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #71717a;
        margin-bottom: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Initialize Chatbot (Neural Embeddings) ───────────────────────────────────
@st.cache_resource
def load_chatbot():
    return FAQChatbot()


bot = load_chatbot()

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="brand-nav">
        <div class="brand-title-wrap">
            <h1 class="brand-title">FAQ Assistant</h1>
            <p class="brand-subtitle">Automated question answering powered by Semantic Embeddings</p>
        </div>
        <div class="status-pill">
            <span class="status-dot"></span>
            <span>Neural Semantic Matcher</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-heading">Browse Topics</div>', unsafe_allow_html=True)
    st.caption("Click any frequently asked question to query the assistant:")

    categories = bot.get_categories()
    for category, questions in categories.items():
        with st.expander(category, expanded=False):
            for q in questions:
                if st.button(q, key=f"sidebar_{q[:30]}", use_container_width=True):
                    st.session_state.sidebar_question = q

    st.divider()
    if st.button("Clear Conversation", use_container_width=True, key="clear_chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        "<div style='text-align: center; color: #a1a1aa; font-size: 0.75rem; margin-top: 1.5rem;'>"
        "CodeAlpha AI Internship • Task 2"
        "</div>",
        unsafe_allow_html=True,
    )

# ── Session State ────────────────────────────────────────────────────────────
if "messages" not in st.session_state or not st.session_state.messages:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! I am your **FAQ Assistant**.\n\n"
                "I can answer questions regarding **shipping**, **returns**, **payments**, **orders**, and **account management**.\n\n"
                "Examples you can ask:\n"
                "- *What is your return policy?*\n"
                "- *How can I track my order?*\n"
                "- *Do you offer international shipping?*"
            ),
        }
    ]

# ── Display Chat History ─────────────────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if "status" in message and message["status"]:
            status = message["status"]
            conf = message.get("confidence", 0.0)
            if status == "matched":
                badge_class = "conf-high"
                label = f"Match confidence: {conf:.0%}"
            elif status == "clarify":
                badge_class = "conf-medium"
                label = f"Possible match: {conf:.0%}"
            else:
                badge_class = "conf-low"
                label = "No direct match"

            st.markdown(
                f'<span class="confidence-badge {badge_class}">{label}</span>',
                unsafe_allow_html=True,
            )


# ── Helper: Process & Respond ────────────────────────────────────────────────
def process_question(question: str):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    result = bot.get_response(question)
    response_content = result["answer"]

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for char in response_content:
            full_response += char
            time.sleep(0.004)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

        status = result.get("status", "matched")
        conf = result.get("confidence", 0.0)
        if status == "matched":
            badge_class = "conf-high"
            label = f"Match confidence: {conf:.0%}"
        elif status == "clarify":
            badge_class = "conf-medium"
            label = f"Possible match: {conf:.0%}"
        else:
            badge_class = "conf-low"
            label = "No direct match"

        st.markdown(
            f'<span class="confidence-badge {badge_class}">{label}</span>',
            unsafe_allow_html=True,
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response_content,
            "confidence": result["confidence"],
            "status": result.get("status", "matched"),
        }
    )


# ── Handle Sidebar Click ─────────────────────────────────────────────────────
if "sidebar_question" in st.session_state and st.session_state.sidebar_question:
    question = st.session_state.sidebar_question
    st.session_state.sidebar_question = None
    process_question(question)

# ── Chat Input ───────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask a question about orders, shipping, returns, or policies..."):
    process_question(prompt)
