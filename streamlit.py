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
# Styling — paramdham-style golden background, twinkling stars,
# glowing Shiv Baba light-point, and Baba-photo blink/star effects
# ==============================================================================
CUSTOM_CSS = """
<style>
#MainMenu, footer, header {visibility: hidden;}

.stApp {
    background: radial-gradient(circle at 50% 20%, #fff8e1 0%, #ffe9b3 35%, #f7c873 65%, #e8a94a 100%);
    position: relative;
    overflow-x: hidden;
}

/* --- Twinkling star field over the paramdham background --- */
.star-field {
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
}
.twinkle-star {
    position: absolute;
    width: 3px; height: 3px;
    background: #fffbe6;
    border-radius: 50%;
    box-shadow: 0 0 6px 2px rgba(255,255,255,0.8);
    animation: twinkle 2.4s ease-in-out infinite;
}
@keyframes twinkle {
    0%, 100% { opacity: 0.2; transform: scale(0.8); }
    50% { opacity: 1; transform: scale(1.4); }
}

/* --- Shiv Baba — symbolic point of light (not a photo/person) --- */
.shivbaba-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 10px 0 22px 0;
    position: relative;
    z-index: 1;
}
.shivbaba-light {
    width: 46px; height: 46px;
    border-radius: 50%;
    background: radial-gradient(circle, #fff4d6 0%, #ffb347 45%, #ff7a1a 75%, rgba(255,122,26,0) 100%);
    box-shadow: 0 0 20px 8px rgba(255,171,64,0.7), 0 0 45px 20px rgba(255,196,110,0.4);
    animation: shivbaba-pulse 2.6s ease-in-out infinite;
}
@keyframes shivbaba-pulse {
    0%, 100% { transform: scale(1); box-shadow: 0 0 20px 8px rgba(255,171,64,0.6), 0 0 45px 20px rgba(255,196,110,0.35); }
    50% { transform: scale(1.12); box-shadow: 0 0 28px 12px rgba(255,171,64,0.85), 0 0 60px 26px rgba(255,196,110,0.55); }
}
.shivbaba-label {
    margin-top: 8px;
    font-size: 0.85rem;
    color: #8a5a1e;
    letter-spacing: 0.05em;
    font-weight: 600;
}

/* --- Brahma Baba photo frame --- */
.baba-frame-outer {
    display: flex;
    justify-content: center;
    margin-bottom: 18px;
    position: relative;
    z-index: 1;
}
.baba-frame {
    position: relative;
    width: 220px; height: 220px;
    border-radius: 50%;
    padding: 6px;
    background: conic-gradient(from 0deg, #ffd76a, #ffb347, #ffd76a, #fff3cf, #ffd76a);
    box-shadow: 0 0 30px rgba(255,183,77,0.6);
}
.baba-frame-inner {
    position: relative;
    width: 100%; height: 100%;
    border-radius: 50%;
    overflow: hidden;
    background: #fff3cf;
}
.baba-photo-a, .baba-photo-b {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    object-fit: cover;
}
.baba-photo-a { animation: blink-crossfade-a 4s steps(1) infinite; }
.baba-photo-b { animation: blink-crossfade-b 4s steps(1) infinite; }
@keyframes blink-crossfade-a {
    0%, 92% { opacity: 1; }
    94%, 97% { opacity: 0; }
    100% { opacity: 1; }
}
@keyframes blink-crossfade-b {
    0%, 92% { opacity: 0; }
    94%, 97% { opacity: 1; }
    100% { opacity: 0; }
}
.baba-photo-single {
    width: 100%; height: 100%;
    object-fit: cover;
    animation: glow-pulse 3.2s ease-in-out infinite;
}
@keyframes glow-pulse {
    0%, 100% { filter: brightness(1); }
    50% { filter: brightness(1.08); }
}

/* --- Pulsing forehead star --- */
.forehead-star {
    position: absolute;
    font-size: 20px;
    color: #fff4c2;
    text-shadow: 0 0 8px #ffcf4d, 0 0 16px #ff9d1e;
    animation: star-blink 1.8s ease-in-out infinite;
    pointer-events: none;
    z-index: 2;
}
@keyframes star-blink {
    0%, 100% { opacity: 0.35; transform: scale(0.85); }
    50% { opacity: 1; transform: scale(1.15); }
}

.baba-caption {
    text-align: center;
    color: #8a5a1e;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    margin-bottom: 6px;
}

/* --- Chat cards, restyled to match the golden theme --- */
h1 { color: #7a4a12 !important; text-align: center; }
.qa-card {
    background: rgba(255,255,255,0.55);
    border: 1px solid rgba(191,140,58,0.35);
    border-radius: 14px;
    padding: 16px 18px;
    margin-bottom: 14px;
}
.q-label { color: #a5670f; font-weight: 700; font-size: 0.78rem; text-transform: uppercase; margin-bottom: 4px; }
.q-text { color: #4a3210; font-size: 1.02rem; margin-bottom: 10px; }
.a-label { color: #8a5a1e; font-weight: 700; font-size: 0.78rem; text-transform: uppercase; margin-bottom: 4px; }
.a-text { color: #5c3d14; line-height: 1.55; }
.pages-row { margin-top: 10px; padding-top: 8px; border-top: 1px dashed rgba(191,140,58,0.4); font-size: 0.8rem; color: #8a5a1e; }

div.stButton > button {
    background: linear-gradient(90deg, #ffb347, #ff8a1e);
    color: #4a2c00; font-weight: 700; border: none;
    border-radius: 10px;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Sprinkle some twinkling stars across the background
STAR_FIELD_HTML = '<div class="star-field">' + "".join(
    f'<div class="twinkle-star" style="top:{(i * 37) % 100}%; left:{(i * 53) % 100}%; '
    f'animation-delay:{(i % 6) * 0.4}s;"></div>'
    for i in range(28)
) + "</div>"
st.markdown(STAR_FIELD_HTML, unsafe_allow_html=True)


def render_shivbaba():
    """Shiv Baba is represented symbolically as a point of light, per BK
    tradition — not as a photo of a person."""
    st.markdown(
        """
        <div class="shivbaba-wrap">
            <div class="shivbaba-light"></div>
            <div class="shivbaba-label">Shiv Baba</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_baba_frame(photo_a_b64, photo_a_mime, photo_b_b64=None, photo_b_mime=None,
                       star_top_pct=22, star_left_pct=48):
    """Renders the uploaded Brahma Baba photo(s) in a glowing frame with a
    pulsing star near the forehead. If two photos are supplied (eyes open /
    eyes closed), they crossfade for a real blink; otherwise a single photo
    gets a gentle glow-pulse instead."""
    if photo_b_b64:
        photo_html = f"""
            <img class="baba-photo-a" src="data:{photo_a_mime};base64,{photo_a_b64}">
            <img class="baba-photo-b" src="data:{photo_b_mime};base64,{photo_b_b64}">
        """
    else:
        photo_html = f'<img class="baba-photo-single" src="data:{photo_a_mime};base64,{photo_a_b64}">'

    st.markdown(
        f"""
        <div class="baba-caption">Brahma Baba</div>
        <div class="baba-frame-outer">
            <div class="baba-frame">
                <div class="baba-frame-inner">
                    {photo_html}
                    <div class="forehead-star" style="top:{star_top_pct}%; left:{star_left_pct}%;">⭐</div>
                </div>
            </div>
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

with st.expander("🖼️ Add Brahma Baba's photo", expanded="baba_photo_a" not in st.session_state):
    st.caption(
        "Upload one photo for a soft glow effect, or two (eyes-open + eyes-closed / mid-blink) "
        "for a real blinking animation."
    )
    col1, col2 = st.columns(2)
    with col1:
        photo_a_file = st.file_uploader("Photo (eyes open)", type=["png", "jpg", "jpeg"], key="photo_a_upload")
    with col2:
        photo_b_file = st.file_uploader("Photo (eyes closed / blinking) — optional", type=["png", "jpg", "jpeg"], key="photo_b_upload")

    star_top = st.slider("Star vertical position (%)", 0, 60, 22)
    star_left = st.slider("Star horizontal position (%)", 20, 80, 48)

    if photo_a_file is not None:
        import base64
        st.session_state.baba_photo_a = base64.b64encode(photo_a_file.getvalue()).decode("utf-8")
        st.session_state.baba_photo_a_mime = photo_a_file.type or "image/png"
        if photo_b_file is not None:
            st.session_state.baba_photo_b = base64.b64encode(photo_b_file.getvalue()).decode("utf-8")
            st.session_state.baba_photo_b_mime = photo_b_file.type or "image/png"
        else:
            st.session_state.pop("baba_photo_b", None)
        st.session_state.star_top = star_top
        st.session_state.star_left = star_left

if "baba_photo_a" in st.session_state:
    render_baba_frame(
        st.session_state.baba_photo_a,
        st.session_state.baba_photo_a_mime,
        st.session_state.get("baba_photo_b"),
        st.session_state.get("baba_photo_b_mime"),
        st.session_state.get("star_top", 22),
        st.session_state.get("star_left", 48),
    )

st.write("")

question = st.text_input("Ask a question from the textbook")

if st.button("Submit") and question.strip():
    with st.spinner("Searching textbook..."):
        answer, pages = chat(question)
    st.session_state.history.insert(0, (question, answer, pages))

for q, a, pages in st.session_state.history:
    render_qa_card(q, a, pages)
