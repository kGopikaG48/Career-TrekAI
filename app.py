import streamlit as st
from api_client import IBMWatsonxClient

# ── 1. Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Career-Trek AI | Powered by IBM watsonx",
    page_icon="🧭",
    layout="wide",
)

# ── 2. Session State Bootstrap ─────────────────────────────────────────────────
if "page"     not in st.session_state: st.session_state.page     = "home"
if "messages" not in st.session_state: st.session_state.messages = []
if "client"   not in st.session_state: st.session_state.client   = IBMWatsonxClient()

# ── 3. Theme Palette (Dark / Gold — permanent) ─────────────────────────────────
T = {
    "bg":           "#0B0B0B",
    "card":         "#171717",
    "sidebar":      "#0F0F0F",
    "border":       "#2A2A2A",
    "gold":         "#D4AF37",
    "gold_hover":   "#F4C430",
    "text":         "#FFFFFF",
    "text_muted":   "#B8B8B8",
    "chat_user":    "#1A1A1A",
    "chat_bot":     "#141414",
    "input_bg":     "#1C1C1C",
    "hero_grad1":   "#1A1400",
    "hero_grad2":   "#0B0B0B",
    "shadow":       "rgba(212,175,55,0.18)",
}

# ── 4. Premium CSS ─────────────────────────────────────────────────────────────
CUSTOM_CSS = f"""
<style>

/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Global Reset ── */
html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif !important;
    scroll-behavior: smooth;
}}

.stApp {{
    background: {T["bg"]} !important;
    color: {T["text"]} !important;
}}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {{
    background: {T["sidebar"]} !important;
    border-right: 1px solid {T["border"]} !important;
    padding-top: 10px;
}}

section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {{
    color: {T["text_muted"]} !important;
    font-size: 14px;
}}

/* Sidebar nav buttons */
section[data-testid="stSidebar"] .stButton > button {{
    width: 100%;
    text-align: left !important;
    background: transparent !important;
    border: none !important;
    color: {T["text_muted"]} !important;
    font-size: 14px;
    font-weight: 500;
    padding: 10px 16px;
    border-radius: 8px;
    transition: all 0.2s ease;
    margin-bottom: 2px;
}}

section[data-testid="stSidebar"] .stButton > button:hover {{
    background: {T["gold"]}18 !important;
    color: {T["gold"]} !important;
    border-left: 3px solid {T["gold"]} !important;
    padding-left: 20px !important;
}}

/* ── Hero Section ── */
.hero-section {{
    background: linear-gradient(135deg, {T["hero_grad1"]} 0%, {T["hero_grad2"]} 100%);
    border: 1px solid {T["gold"]}44;
    border-radius: 20px;
    padding: 44px 52px;
    margin-bottom: 40px;
    position: relative;
    overflow: hidden;
    animation: fadeInDown 0.7s ease both;
}}

/* Two-column hero layout */
.hero-inner {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 40px;
}}

.hero-text {{
    flex: 1;
    min-width: 0;
}}

.hero-illustration {{
    flex: 0 0 260px;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0.82;
}}

.hero-badge {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 16px;
    border: 1px solid {T["gold"]}66;
    border-radius: 50px;
    color: {T["gold"]};
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 24px;
    background: {T["gold"]}0D;
}}

.hero-title {{
    font-size: 56px;
    font-weight: 900;
    letter-spacing: -1.5px;
    line-height: 1.1;
    margin: 0 0 10px 0;
    background: linear-gradient(90deg, {T["text"]} 0%, {T["gold"]} 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

.hero-subtitle {{
    font-size: 21px;
    font-weight: 600;
    color: {T["gold"]};
    margin: 0 0 14px 0;
    letter-spacing: 0.3px;
}}

.hero-desc {{
    color: {T["text_muted"]};
    font-size: 15px;
    line-height: 1.75;
    max-width: 560px;
    margin-bottom: 24px;
}}

.hero-powered {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: {T["text_muted"]};
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 0.5px;
    margin-bottom: 24px;
}}

.hero-powered span {{
    color: {T["gold"]};
    font-weight: 700;
}}

/* ── Hero CTA Button ── */
.hero-cta-btn {{
    display: inline-block;
    background: linear-gradient(135deg, {T["gold"]} 0%, {T["gold_hover"]} 100%);
    color: #000000 !important;
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 0.5px;
    padding: 16px 40px;
    border-radius: 12px;
    text-decoration: none;
    border: none;
    cursor: pointer;
    transition: all 0.25s ease;
    box-shadow: 0 4px 24px {T["shadow"]};
}}

/* ── Section Title ── */
.section-title {{
    font-size: 28px;
    font-weight: 800;
    color: {T["text"]};
    margin: 8px 0 28px 0;
    letter-spacing: -0.5px;
}}

.section-title span {{
    color: {T["gold"]};
}}

/* ── Feature Cards ── */
.feature-card {{
    background: {T["card"]};
    border: 1px solid {T["border"]};
    border-radius: 16px;
    padding: 32px 28px;
    height: 100%;
    min-height: 200px;
    transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1);
    animation: fadeInUp 0.6s ease both;
    position: relative;
    overflow: hidden;
}}

.feature-card::after {{
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, {T["gold"]} 0%, {T["gold_hover"]} 100%);
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.3s ease;
}}

.feature-card:hover {{
    border-color: {T["gold"]}88;
    transform: translateY(-6px);
    box-shadow: 0 12px 40px {T["shadow"]};
}}

.feature-card:hover::after {{
    transform: scaleX(1);
}}

.feature-icon {{
    font-size: 36px;
    margin-bottom: 16px;
    display: block;
}}

.feature-title {{
    font-size: 17px;
    font-weight: 700;
    color: {T["text"]};
    margin-bottom: 10px;
}}

.feature-desc {{
    font-size: 14px;
    color: {T["text_muted"]};
    line-height: 1.7;
}}

/* ── Main Action Buttons ── */
.stButton > button {{
    background: linear-gradient(135deg, {T["gold"]} 0%, {T["gold_hover"]} 100%) !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 12px 32px !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 16px {T["shadow"]} !important;
    letter-spacing: 0.3px;
}}

.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px {T["shadow"]} !important;
    background: linear-gradient(135deg, {T["gold_hover"]} 0%, {T["gold"]} 100%) !important;
}}

.stButton > button:active {{
    transform: translateY(0px) !important;
}}

/* ── Chat Interface ── */
.chat-header {{
    display: flex;
    align-items: center;
    gap: 14px;
    background: {T["card"]};
    border: 1px solid {T["border"]};
    border-radius: 16px;
    padding: 20px 28px;
    margin-bottom: 24px;
    animation: fadeInDown 0.5s ease both;
}}

.chat-header-icon {{
    font-size: 32px;
}}

.chat-header-title {{
    font-size: 22px;
    font-weight: 800;
    color: {T["text"]};
}}

.chat-header-sub {{
    font-size: 13px;
    color: {T["gold"]};
    font-weight: 500;
    letter-spacing: 0.3px;
}}

/* Streamlit chat messages */
[data-testid="stChatMessage"] {{
    background: {T["card"]} !important;
    border: 1px solid {T["border"]} !important;
    border-radius: 14px !important;
    margin-bottom: 12px !important;
    padding: 4px !important;
}}

[data-testid="stChatInput"] textarea {{
    background: {T["input_bg"]} !important;
    color: {T["text"]} !important;
    border: 1px solid {T["border"]} !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
}}

[data-testid="stChatInput"] textarea:focus {{
    border-color: {T["gold"]} !important;
    box-shadow: 0 0 0 2px {T["gold"]}22 !important;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 6px; }}
::-webkit-scrollbar-track {{ background: {T["bg"]}; }}
::-webkit-scrollbar-thumb {{ background: {T["gold"]}55; border-radius: 6px; }}
::-webkit-scrollbar-thumb:hover {{ background: {T["gold"]}; }}

/* ── Footer ── */
.footer {{
    margin-top: 64px;
    padding: 24px;
    border-top: 1px solid {T["border"]};
    text-align: center;
    color: {T["text_muted"]};
    font-size: 13px;
    line-height: 1.8;
}}

.footer strong {{
    color: {T["gold"]};
}}

/* ── Animations ── */
@keyframes fadeInDown {{
    from {{ opacity: 0; transform: translateY(-18px); }}
    to   {{ opacity: 1; transform: translateY(0);     }}
}}

@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(18px); }}
    to   {{ opacity: 1; transform: translateY(0);    }}
}}

/* ── Divider ── */
hr {{
    border: none;
    border-top: 1px solid {T["border"]} !important;
    margin: 8px 0 !important;
}}

/* ── Metric/info overrides ── */
[data-testid="stMetric"] {{
    background: {T["card"]} !important;
    border: 1px solid {T["border"]} !important;
    border-radius: 12px !important;
    padding: 20px !important;
}}

[data-testid="stMetricValue"] {{
    color: {T["gold"]} !important;
}}

/* ── Selectbox / Radio ── */
.stSelectbox div[data-baseweb="select"] > div {{
    background: {T["input_bg"]} !important;
    border-color: {T["border"]} !important;
    color: {T["text"]} !important;
}}

</style>
"""


# ── 5. Helper: render footer ───────────────────────────────────────────────────
def render_footer():
    st.markdown(
        '<div class="footer">'
        'Career-Trek AI &nbsp;|&nbsp; Enterprise AI powered by <strong>IBM watsonx Orchestrate</strong><br>'
        '© 2026 K Gopika Gopalakrishnan'
        '</div>',
        unsafe_allow_html=True,
    )


# ── 6. Sidebar ─────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown(
            f"""
            <div style="padding:16px 8px 8px 8px;">
                <div style="font-size:22px;font-weight:900;color:{T['gold']};letter-spacing:-0.5px;">
                    🧭 Career-Trek AI
                </div>
                <div style="font-size:12px;color:{T['text_muted']};margin-top:4px;font-weight:500;">
                    Powered by IBM watsonx Orchestrate
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("---")

        nav_items = [
            ("🏠", "Dashboard",    "home"),
            ("🤖", "AI Assistant", "chat"),
        ]

        for icon, label, target in nav_items:
            if st.button(f"{icon}  {label}", key=f"nav_{label}"):
                st.session_state.page = target
                st.rerun()

        st.markdown("---")
        st.markdown(
            f'<div style="font-size:11px;color:{T["text_muted"]};text-align:center;padding:8px;">'
            f'<strong style="color:{T["gold"]};">IBM watsonx Orchestrate</strong><br>'
            f'Active &amp; Connected'
            f'</div>',
            unsafe_allow_html=True,
        )


# ── 7. Dashboard Page ──────────────────────────────────────────────────────────

# The SVG is built as a plain string (no f-string) so its curly braces are safe.
# Python .format() is used only for the two colour tokens we actually need.
_COMPASS_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 260"'
    ' width="240" height="240" aria-hidden="true" focusable="false">'
    "<defs>"
    '<radialGradient id="ct-glow" cx="50%" cy="50%" r="50%">'
    '<stop offset="0%"   stop-color="#D4AF37" stop-opacity="0.20"/>'
    '<stop offset="100%" stop-color="#D4AF37" stop-opacity="0"/>'
    "</radialGradient>"
    '<radialGradient id="ct-jewel" cx="50%" cy="50%" r="50%">'
    '<stop offset="0%"   stop-color="#F4C430" stop-opacity="0.80"/>'
    '<stop offset="100%" stop-color="#D4AF37" stop-opacity="0.10"/>'
    "</radialGradient>"
    '<linearGradient id="ct-north" x1="0%" y1="0%" x2="0%" y2="100%">'
    '<stop offset="0%"   stop-color="#F4C430"/>'
    '<stop offset="100%" stop-color="#D4AF37" stop-opacity="0.50"/>'
    "</linearGradient>"
    '<linearGradient id="ct-south" x1="0%" y1="0%" x2="0%" y2="100%">'
    '<stop offset="0%"   stop-color="#3A3A3A"/>'
    '<stop offset="100%" stop-color="#1C1C1C"/>'
    "</linearGradient>"
    "</defs>"
    # ambient glow
    '<circle cx="130" cy="130" r="120" fill="url(#ct-glow)"/>'
    # rings
    '<circle cx="130" cy="130" r="112" fill="none" stroke="#D4AF37" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="4 6"/>'
    '<circle cx="130" cy="130" r="98"  fill="none" stroke="#D4AF37" stroke-width="1.5" stroke-opacity="0.42"/>'
    '<circle cx="130" cy="130" r="74"  fill="none" stroke="#D4AF37" stroke-width="0.7" stroke-opacity="0.20"/>'
    '<circle cx="130" cy="130" r="52"  fill="none" stroke="#D4AF37" stroke-width="0.9" stroke-opacity="0.28"/>'
    # cardinal ticks
    '<line x1="130" y1="28"  x2="130" y2="46"  stroke="#D4AF37" stroke-width="2.8" stroke-opacity="0.85" stroke-linecap="round"/>'
    '<line x1="130" y1="214" x2="130" y2="232" stroke="#D4AF37" stroke-width="2.8" stroke-opacity="0.85" stroke-linecap="round"/>'
    '<line x1="28"  y1="130" x2="46"  y2="130" stroke="#D4AF37" stroke-width="2.8" stroke-opacity="0.85" stroke-linecap="round"/>'
    '<line x1="214" y1="130" x2="232" y2="130" stroke="#D4AF37" stroke-width="2.8" stroke-opacity="0.85" stroke-linecap="round"/>'
    # intercardinal ticks
    '<line x1="56"  y1="56"  x2="64"  y2="64"  stroke="#D4AF37" stroke-width="1.4" stroke-opacity="0.38" stroke-linecap="round"/>'
    '<line x1="204" y1="56"  x2="196" y2="64"  stroke="#D4AF37" stroke-width="1.4" stroke-opacity="0.38" stroke-linecap="round"/>'
    '<line x1="56"  y1="204" x2="64"  y2="196" stroke="#D4AF37" stroke-width="1.4" stroke-opacity="0.38" stroke-linecap="round"/>'
    '<line x1="204" y1="204" x2="196" y2="196" stroke="#D4AF37" stroke-width="1.4" stroke-opacity="0.38" stroke-linecap="round"/>'
    # labels
    '<text x="130" y="20"  text-anchor="middle" fill="#F4C430" font-size="12" font-weight="700" opacity="0.92">N</text>'
    '<text x="130" y="250" text-anchor="middle" fill="#D4AF37" font-size="12" font-weight="700" opacity="0.45">S</text>'
    '<text x="12"  y="135" text-anchor="middle" fill="#D4AF37" font-size="12" font-weight="700" opacity="0.45">W</text>'
    '<text x="248" y="135" text-anchor="middle" fill="#D4AF37" font-size="12" font-weight="700" opacity="0.45">E</text>'
    # petals
    '<polygon points="130,46 122,118 130,130 138,118" fill="url(#ct-north)" opacity="0.96"/>'
    '<polygon points="130,214 122,142 130,130 138,142" fill="url(#ct-south)" opacity="0.72"/>'
    '<polygon points="46,130 118,122 130,130 118,138" fill="#D4AF37" opacity="0.32"/>'
    '<polygon points="214,130 142,122 130,130 142,138" fill="#D4AF37" opacity="0.32"/>'
    '<polygon points="60,60  119,119 130,130 119,119" fill="#D4AF37" opacity="0.14"/>'
    '<polygon points="200,60 141,119 130,130 141,119" fill="#D4AF37" opacity="0.14"/>'
    '<polygon points="60,200 119,141 130,130 119,141" fill="#D4AF37" opacity="0.14"/>'
    '<polygon points="200,200 141,141 130,130 141,141" fill="#D4AF37" opacity="0.14"/>'
    # jewel
    '<circle cx="130" cy="130" r="11" fill="url(#ct-jewel)"/>'
    '<circle cx="130" cy="130" r="5"  fill="#F4C430" opacity="0.92"/>'
    '<circle cx="130" cy="130" r="2"  fill="#FFFFFF"  opacity="0.85"/>'
    "</svg>"
)


def dashboard():

    # ── Hero — single st.markdown block; uses string concatenation, NOT f-string,
    #    so the SVG's url(#...) and gradient stop-opacity values are never parsed
    #    as Python format fields. ──────────────────────────────────────────────────
    hero_html = (
        '<div class="hero-section">'
        '<div class="hero-inner">'
        '<div class="hero-text">'
        '<div class="hero-badge">&#9889;Your Career Counseling Companion</div>'
        '<h1 class="hero-title">Career-Trek AI</h1>'
        '<p class="hero-subtitle">Your Personal AI Career Mentor</p>'
        '<p class="hero-desc">'
        "Discover career opportunities, analyze your skills, receive personalized "
        "learning roadmaps, resume guidance, interview preparation, and "
        "certification recommendations using AI."
        "</p>"
        '<div class="hero-powered">'
        "&#128311;&nbsp;Powered by&nbsp;<span>IBM watsonx Orchestrate</span>"
        "</div>"
        "</div>"                        # .hero-text
        '<div class="hero-illustration">'
        + _COMPASS_SVG +
        "</div>"                        # .hero-illustration
        "</div>"                        # .hero-inner
        "</div>"                        # .hero-section
    )
    st.markdown(hero_html, unsafe_allow_html=True)

    # ── Hero CTA button ──
    if st.button("🚀  Launch AI Assistant", key="hero_cta"):
        st.session_state.page = "chat"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Platform Features — 2×3 CSS grid (pure HTML, no st.columns) ──────────────
    st.markdown(
        f'<p class="section-title">Platform <span>Features</span></p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        .features-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 40px;
        }
        .features-grid .feature-card {
            min-height: 200px;
            box-sizing: border-box;
        }
        @media (max-width: 900px) {
            .features-grid { grid-template-columns: repeat(2, 1fr); }
        }
        @media (max-width: 580px) {
            .features-grid { grid-template-columns: 1fr; }
        }
        </style>

        <div class="features-grid">

          <div class="feature-card">
            <span class="feature-icon">&#129302;</span>
            <div class="feature-title">AI Career Assistant</div>
            <div class="feature-desc">Personalized AI-powered career guidance through IBM watsonx Orchestrate.</div>
          </div>

          <div class="feature-card">
            <span class="feature-icon">&#128202;</span>
            <div class="feature-title">Skill Analysis</div>
            <div class="feature-desc">Analyze your strengths and identify skill gaps to grow strategically.</div>
          </div>

          <div class="feature-card">
            <span class="feature-icon">&#128739;</span>
            <div class="feature-title">Learning Roadmap</div>
            <div class="feature-desc">Receive personalized, step-by-step learning plans aligned to your goals.</div>
          </div>

          <div class="feature-card">
            <span class="feature-icon">&#128196;</span>
            <div class="feature-title">Resume &amp; Interview</div>
            <div class="feature-desc">Improve your resume and prepare confidently for interviews with AI guidance.</div>
          </div>

          <div class="feature-card">
            <span class="feature-icon">&#127891;</span>
            <div class="feature-title">Certifications</div>
            <div class="feature-desc">Get certification recommendations based on your career goals and skill profile.</div>
          </div>

          <div class="feature-card">
            <span class="feature-icon">&#128188;</span>
            <div class="feature-title">Career Recommendations</div>
            <div class="feature-desc">Discover suitable career paths based on your skills, interests, and aspirations.</div>
          </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    render_footer()


# ── 8. Chat Page ───────────────────────────────────────────────────────────────
def chat():
    # Chat header
    st.markdown(
        f"""
        <div class="chat-header">
            <span class="chat-header-icon">🤖</span>
            <div>
                <div class="chat-header-title">IBM watsonx Career Assistant</div>
                <div class="chat-header-sub">Powered by IBM watsonx Orchestrate · Ready</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("← Back to Dashboard", key="back_btn"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Render conversation history
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])

    # Chat input — ALL API/session logic unchanged
    if prompt := st.chat_input("Ask a professional career question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Analyzing with IBM watsonx..."):
                reply = st.session_state.client.chat(st.session_state.messages)
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})


# ── 9. Entry Point ─────────────────────────────────────────────────────────────
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
render_sidebar()

if st.session_state.page == "home":
    dashboard()
else:
    chat()
