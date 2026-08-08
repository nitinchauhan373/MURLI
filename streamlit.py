import streamlit as st
from Avyakt_Murli_Assistant import chat

# ==============================================================================
# Page configuration
# ==============================================================================
st.set_page_config(
    page_title="AVYAKT MURLI Teaching Assistant",
    page_icon="🎓",
    layout="centered",
)

# ==============================================================================
# Session state
# ==============================================================================
if "history" not in st.session_state:
    st.session_state.history = []  # list of (question, answer, pages)

# ==============================================================================
# Styling — paramdham golden-sky background + blinking Shiv Baba point of
# light + white chat box with black text
# ==============================================================================
CUSTOM_CSS = """
<style>
#MainMenu, footer, header {visibility: hidden;}

/* --- Paramdham background: soft golden sky --- */
.stApp {
    background: radial-gradient(circle at 50% 15%, #fffdf3 0%, #fff3cf 30%, #ffd98a 60%, #f4b350 100%);
}

h1 { color: #7a4a12 !important; text-align: center; }

/* --- Shiv Baba — blinking point of light --- */
.shivbaba-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 8px 0 26px 0;
}
.shivbaba-light {
    width: 42px; height: 42px;
    border-radius: 50%;
    background: radial-gradient(circle, #ffffff 0%, #fff4c2 30%, #ffb347 60%, rgba(255,122,26,0) 100%);
    animation: shivbaba-blink 2.2s ease-in-out infinite;
}
@keyframes shivbaba-blink {
    0%, 100% {
        transform: scale(1);
        box-shadow: 0 0 18px 6px rgba(255,183,64,0.6), 0 0 40px 18px rgba(255,214,140,0.35);
        opacity: 1;
    }
    50% {
        transform: scale(1.25);
        box-shadow: 0 0 30px 12px rgba(255,183,64,0.9), 0 0 60px 28px rgba(255,214,140,0.6);
        opacity: 0.85;
    }
}
.shivbaba-label {
    margin-top: 10px;
    font-size: 0.85rem;
    color: #8a5a1e;
    letter-spacing: 0.05em;
    font-weight: 600;
}

/* --- Prompt above the chat box --- */
.yaad-prompt {
    text-align: center;
    font-size: 1.15rem;
    font-weight: 600;
    color: #6b4212;
    margin-bottom: 10px;
}

/* --- Chat input box: white background, black text --- */
.stTextInput input {
    background-color: #ffffff !important;
    color: #000000 !important;
    border-radius: 10px;
    border: 1px solid #d9b877;
}

div.stButton > button {
    background: linear-gradient(90deg, #ffb347, #ff8a1e);
    color: #4a2c00; font-weight: 700; border: none;
    border-radius: 10px;
}

/* --- Q&A cards: white background, black text --- */
.qa-card {
    background: #ffffff;
    border: 1px solid #e3c48c;
    border-radius: 14px;
    padding: 16px 18px;
    margin-bottom: 14px;
}
.q-label, .a-label { color: #a5670f; font-weight: 700; font-size: 0.78rem; text-transform: uppercase; margin-bottom: 4px; }
.q-text, .a-text { color: #000000 !important; }
.q-text { margin-bottom: 10px; }
.a-text { line-height: 1.55; }
.pages-row { margin-top: 10px; padding-top: 8px; border-top: 1px dashed #d9b877; font-size: 0.8rem; color: #8a5a1e; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_shivbaba():
    """Shiv Baba is represented symbolically as a blinking point of light,
    per BK tradition — not as a photo of a person."""
    st.markdown(
        """
        <div class="shivbaba-wrap">
            <div class="shivbaba-light"></div>
            <div class="shivbaba-label">Shiv Baba</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_qa_card(question: str, answer: str, pages: list):
    pages_html = ", ".join(str(p) for p in pages) if pages else "No source pages returned"
    st.markdown(
        f"""
        <div class="qa-card">
            <div class="q-label">Question</div>
            <div class="q-text">{question}</div>
            <div class="a-label">Answer</div>
            <div class="a-text">{answer}</div>
            <div class="pages-row">📚 Source Pages: {pages_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==============================================================================
# Page layout
# ==============================================================================
st.title("🎓 AVYAKT MURLI Teaching Assistant")

render_shivbaba()

st.markdown('<div class="yaad-prompt">Shiv Baba Yaad Hai...?</div>', unsafe_allow_html=True)

question = st.text_input("Ask a question from the textbook", label_visibility="collapsed")

if st.button("Submit") and question.strip():
    with st.spinner("Searching textbook..."):
        answer, pages = chat(question)
    st.session_state.history.insert(0, (question, answer, pages))

for q, a, pages in st.session_state.history:
    render_qa_card(q, a, pages)
