import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import time
from pipline import run_research_pipeline

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:ital,wght@0,400;0,500;1,400&family=Instrument+Serif:ital@0;1&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
}

.stApp {
    background: #0a0a0f;
    color: #e8e4d9;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

/* ── Hero header ── */
.hero {
    position: relative;
    padding: 3.5rem 0 2.5rem;
    margin-bottom: 2rem;
    border-bottom: 1px solid #1e1e2e;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 80% 60% at 10% 50%, rgba(255,150,50,0.08) 0%, transparent 70%),
                radial-gradient(ellipse 50% 40% at 90% 20%, rgba(100,200,255,0.06) 0%, transparent 60%);
    pointer-events: none;
}
.hero-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    color: #f97316;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
    opacity: 0.9;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 5vw, 4rem);
    font-weight: 800;
    line-height: 1.05;
    color: #f0ece0;
    margin: 0 0 0.5rem;
    letter-spacing: -0.02em;
}
.hero-title span {
    color: #f97316;
    font-style: italic;
    font-family: 'Instrument Serif', serif;
}
.hero-sub {
    font-size: 0.82rem;
    color: #6b6b7a;
    letter-spacing: 0.03em;
    margin-top: 0.4rem;
}

/* ── Input card ── */
.input-card {
    background: #111118;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    padding: 2rem 2.2rem;
    margin-bottom: 2rem;
    position: relative;
}
.input-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #f97316 0%, #fb923c 40%, transparent 100%);
    border-radius: 12px 12px 0 0;
}

/* ── Streamlit input overrides ── */
.stTextInput > div > div > input {
    background: #0d0d14 !important;
    border: 1px solid #2a2a3a !important;
    border-radius: 8px !important;
    color: #e8e4d9 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    caret-color: #f97316;
}
.stTextInput > div > div > input:focus {
    border-color: #f97316 !important;
    box-shadow: 0 0 0 3px rgba(249,115,22,0.12) !important;
}
.stTextInput label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #6b6b7a !important;
    margin-bottom: 0.5rem !important;
}

/* ── Button ── */
.stButton > button {
    background: #f97316 !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.65rem 2rem !important;
    transition: all 0.2s ease !important;
    text-transform: uppercase;
}
.stButton > button:hover {
    background: #fb923c !important;
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(249,115,22,0.35) !important;
}
.stButton > button:active { transform: translateY(0px); }

/* ── Pipeline steps ── */
.pipeline-container {
    display: flex;
    gap: 0;
    margin: 1.8rem 0 2.2rem;
    position: relative;
}
.pipeline-container::before {
    content: '';
    position: absolute;
    top: 22px; left: 22px; right: 22px;
    height: 1px;
    background: #1e1e2e;
    z-index: 0;
}
.step-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    z-index: 1;
}
.step-dot {
    width: 44px; height: 44px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    font-weight: 500;
    border: 1.5px solid #2a2a3a;
    background: #0a0a0f;
    color: #4a4a5a;
    transition: all 0.4s ease;
    margin-bottom: 0.5rem;
}
.step-dot.active {
    background: #f97316;
    border-color: #f97316;
    color: #0a0a0f;
    box-shadow: 0 0 20px rgba(249,115,22,0.5);
}
.step-dot.done {
    background: #1a2e1a;
    border-color: #22c55e;
    color: #22c55e;
}
.step-label {
    font-size: 0.68rem;
    color: #4a4a5a;
    text-align: center;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    line-height: 1.3;
    max-width: 80px;
}
.step-label.active { color: #f97316; }
.step-label.done { color: #22c55e; }

/* ── Result sections ── */
.result-section {
    margin-bottom: 1.5rem;
    border: 1px solid #1e1e2e;
    border-radius: 10px;
    overflow: hidden;
}
.result-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.9rem 1.3rem;
    background: #0f0f18;
    border-bottom: 1px solid #1e1e2e;
}
.result-badge {
    font-size: 0.65rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.25rem 0.7rem;
    border-radius: 4px;
    font-weight: 500;
}
.badge-search  { background: rgba(59,130,246,0.15); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }
.badge-scrape  { background: rgba(168,85,247,0.15); color: #c084fc; border: 1px solid rgba(168,85,247,0.3); }
.badge-report  { background: rgba(249,115,22,0.15); color: #fb923c; border: 1px solid rgba(249,115,22,0.3); }
.badge-critic  { background: rgba(34,197,94,0.15);  color: #4ade80; border: 1px solid rgba(34,197,94,0.3); }

.result-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    color: #c8c4b8;
}
.result-body {
    padding: 1.3rem 1.5rem;
    background: #0a0a0f;
    font-size: 0.82rem;
    line-height: 1.75;
    color: #9a9690;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 320px;
    overflow-y: auto;
}
.result-body::-webkit-scrollbar { width: 4px; }
.result-body::-webkit-scrollbar-track { background: #0a0a0f; }
.result-body::-webkit-scrollbar-thumb { background: #2a2a3a; border-radius: 4px; }

/* ── Report highlight ── */
.report-body {
    background: #0c0f0c;
    color: #c8e6c9;
    max-height: 480px;
    font-size: 0.85rem;
}

/* ── Status bar ── */
.status-bar {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.7rem 1rem;
    background: #0f0f18;
    border: 1px solid #1e1e2e;
    border-radius: 8px;
    margin-bottom: 1.8rem;
    font-size: 0.75rem;
    color: #6b6b7a;
    letter-spacing: 0.05em;
}
.status-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: #f97316;
    animation: pulse 1.4s ease-in-out infinite;
}
@keyframes pulse {
    0%,100% { opacity: 1; transform: scale(1); }
    50%      { opacity: 0.4; transform: scale(0.75); }
}
.status-dot.done { background: #22c55e; animation: none; }

/* ── Success banner ── */
.success-banner {
    background: linear-gradient(135deg, #0c1f0c 0%, #0f1a0f 100%);
    border: 1px solid #22c55e40;
    border-radius: 10px;
    padding: 1.1rem 1.5rem;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    font-size: 0.8rem;
    color: #4ade80;
    letter-spacing: 0.05em;
}

/* ── Divider ── */
.section-divider {
    border: none;
    border-top: 1px solid #1e1e2e;
    margin: 2rem 0;
}

/* ── Footer ── */
.footer {
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid #1a1a22;
    font-size: 0.7rem;
    color: #3a3a4a;
    letter-spacing: 0.08em;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-label">⬡ AI Research Pipeline</div>
    <div class="hero-title">Research<span>Mind</span></div>
    <div class="hero-sub">SEARCH → SCRAPE → WRITE → CRITIQUE &nbsp;/&nbsp; POWERED BY MULTI-AGENT AI</div>
</div>
""", unsafe_allow_html=True)

# ── Pipeline step tracker ──────────────────────────────────────────────────────
def render_pipeline(active_step=0, done_steps=None):
    done_steps = done_steps or []
    steps = [
        ("01", "Search\nAgent"),
        ("02", "Reader\nAgent"),
        ("03", "Writer\nAgent"),
        ("04", "Critic\nAgent"),
    ]
    dots  = ""
    labels = ""
    for i, (num, label) in enumerate(steps):
        cls = "done" if i in done_steps else ("active" if i == active_step else "")
        icon = "✓" if i in done_steps else num
        dots  += f'<div class="step-item"><div class="step-dot {cls}">{icon}</div></div>'
        labels += f'<div class="step-item"><div class="step-label {cls}">{label.replace(chr(10),"<br>")}</div></div>'

    st.markdown(f"""
    <div class="pipeline-container">{dots}</div>
    <div class="pipeline-container" style="margin-top:-1.6rem;">{labels}</div>
    """, unsafe_allow_html=True)

# ── Input card ─────────────────────────────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)
col1, col2 = st.columns([4, 1], gap="medium")
with col1:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g.  Quantum computing breakthroughs 2025",
        label_visibility="visible",
    )
with col2:
    st.markdown("<div style='height:1.95rem'></div>", unsafe_allow_html=True)
    run_btn = st.button("⟶  Run Pipeline", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "result"    not in st.session_state: st.session_state.result    = None
if "running"   not in st.session_state: st.session_state.running   = False
if "error"     not in st.session_state: st.session_state.error     = None

# ── Run pipeline ───────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic before running.")
    else:
        st.session_state.result  = None
        st.session_state.error   = None
        st.session_state.running = True

        pipeline_placeholder = st.empty()
        status_placeholder   = st.empty()

        steps_labels = [
            "Searching the web for relevant sources…",
            "Scraping top resources for deep content…",
            "Compiling the research report…",
            "Critic agent reviewing the report…",
        ]

        try:
            # Animate steps
            for step_i in range(4):
                with pipeline_placeholder.container():
                    render_pipeline(active_step=step_i, done_steps=list(range(step_i)))
                with status_placeholder.container():
                    st.markdown(f"""
                    <div class="status-bar">
                        <div class="status-dot"></div>
                        STEP {step_i+1}/4 &nbsp;—&nbsp; {steps_labels[step_i]}
                    </div>
                    """, unsafe_allow_html=True)
                if step_i == 0:
                    result = run_research_pipeline(topic)
                    st.session_state.result = result
                    break  # real pipeline runs all steps internally

            # After pipeline runs
            with pipeline_placeholder.container():
                render_pipeline(active_step=-1, done_steps=[0,1,2,3])
            with status_placeholder.container():
                st.markdown("""
                <div class="status-bar">
                    <div class="status-dot done"></div>
                    ALL STEPS COMPLETE &nbsp;—&nbsp; Results ready
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.session_state.error = str(e)
        finally:
            st.session_state.running = False

# ── Idle state: show pipeline skeleton ────────────────────────────────────────
if not st.session_state.running and st.session_state.result is None and st.session_state.error is None:
    render_pipeline(active_step=-1, done_steps=[])
    st.markdown("""
    <div style="text-align:center; padding: 2.5rem 0 1rem; color: #3a3a4a; font-size:0.75rem; letter-spacing:0.1em;">
        ENTER A TOPIC ABOVE AND HIT RUN TO START THE PIPELINE
    </div>
    """, unsafe_allow_html=True)

# ── Error display ──────────────────────────────────────────────────────────────
if st.session_state.error:
    st.error(f"Pipeline error: {st.session_state.error}")

# ── Results ────────────────────────────────────────────────────────────────────
if st.session_state.result:
    res = st.session_state.result

    st.markdown(f"""
    <div class="success-banner">
        <span style="font-size:1.1rem">✦</span>
        <span>PIPELINE COMPLETE &nbsp;—&nbsp; Research on <strong style="color:#86efac">{topic}</strong> is ready.</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Layout: 2 columns top, full-width bottom ──
    col_l, col_r = st.columns(2, gap="large")

    with col_l:
        # Step 1 – Search Results
        st.markdown("""
        <div class="result-section">
            <div class="result-header">
                <span class="result-badge badge-search">Step 01</span>
                <span class="result-title">Search Agent Results</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="result-body" style="border:1px solid #1e1e2e; border-top:none; border-radius:0 0 10px 10px; padding:1.3rem 1.5rem; background:#0a0a0f; font-size:0.82rem; line-height:1.75; color:#9a9690; white-space:pre-wrap; word-break:break-word; max-height:320px; overflow-y:auto;">
{res.get('search_results', 'No data')}
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        # Step 2 – Scraped Content
        st.markdown("""
        <div class="result-section">
            <div class="result-header">
                <span class="result-badge badge-scrape">Step 02</span>
                <span class="result-title">Reader Agent — Scraped Content</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="result-body" style="border:1px solid #1e1e2e; border-top:none; border-radius:0 0 10px 10px; padding:1.3rem 1.5rem; background:#0a0a0f; font-size:0.82rem; line-height:1.75; color:#9a9690; white-space:pre-wrap; word-break:break-word; max-height:320px; overflow-y:auto;">
{res.get('scraped_content', 'No data')}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # Step 3 – Full Report
    st.markdown("""
    <div class="result-section">
        <div class="result-header">
            <span class="result-badge badge-report">Step 03</span>
            <span class="result-title">Writer Agent — Research Report</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="result-body report-body" style="border:1px solid #1e1e2e; border-top:none; border-radius:0 0 10px 10px; padding:1.3rem 1.5rem; background:#0c0f0c; color:#c8e6c9; font-size:0.85rem; line-height:1.85; white-space:pre-wrap; word-break:break-word; max-height:480px; overflow-y:auto;">
{res.get('report', 'No data')}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # Step 4 – Critic Feedback
    st.markdown("""
    <div class="result-section">
        <div class="result-header">
            <span class="result-badge badge-critic">Step 04</span>
            <span class="result-title">Critic Agent — Review & Feedback</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="result-body" style="border:1px solid #1e1e2e; border-top:none; border-radius:0 0 10px 10px; padding:1.3rem 1.5rem; background:#0a0a0f; font-size:0.82rem; line-height:1.75; color:#9a9690; white-space:pre-wrap; word-break:break-word; max-height:320px; overflow-y:auto;">
{res.get('feedback', 'No data')}
    </div>
    """, unsafe_allow_html=True)

    # ── Download buttons ──
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    dl_col1, dl_col2, _ = st.columns([1, 1, 3], gap="small")
    with dl_col1:
        st.download_button(
            "⬇  Download Report",
            data=str(res.get('report', '')),
            file_name=f"report_{topic[:30].replace(' ','_')}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with dl_col2:
        full_output = (
            f"TOPIC: {topic}\n\n"
            f"{'='*60}\nSEARCH RESULTS\n{'='*60}\n{res.get('search_results','')}\n\n"
            f"{'='*60}\nSCRAPED CONTENT\n{'='*60}\n{res.get('scraped_content','')}\n\n"
            f"{'='*60}\nRESEARCH REPORT\n{'='*60}\n{res.get('report','')}\n\n"
            f"{'='*60}\nCRITIC FEEDBACK\n{'='*60}\n{res.get('feedback','')}\n"
        )
        st.download_button(
            "⬇  Full Pipeline Export",
            data=full_output,
            file_name=f"full_pipeline_{topic[:30].replace(' ','_')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    RESEARCHMIND AI &nbsp;·&nbsp; MULTI-AGENT PIPELINE &nbsp;·&nbsp; SEARCH · SCRAPE · WRITE · CRITIQUE
</div>
""", unsafe_allow_html=True)