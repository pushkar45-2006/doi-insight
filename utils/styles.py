"""
utils/styles.py
Custom CSS definitions for DOI Insight — Notion/Perplexity-inspired aesthetic.
Works seamlessly with Streamlit light and dark modes.
"""

CUSTOM_CSS = """
<style>
/* ─── Google Font Import ─────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

/* ─── Root Variables ─────────────────────────────────────────────── */
:root {
    --brand-accent: #6366f1;          /* indigo */
    --brand-accent-soft: #818cf8;
    --brand-accent-dim: rgba(99, 102, 241, 0.08);
    --radius-card: 14px;
    --radius-sm: 8px;
    --shadow-card: 0 1px 3px rgba(0,0,0,.08), 0 8px 24px rgba(0,0,0,.04);
    --shadow-hover: 0 2px 6px rgba(0,0,0,.10), 0 12px 32px rgba(0,0,0,.08);
    --transition: 0.25s ease;
    --font-body: 'Sora', sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
}

/* ─── Global Typography ──────────────────────────────────────────── */
html, body, .stApp, [class*="css"], h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-body) !important;
}

/* ─── Main content max-width constraint ─────────────────────────── */
.block-container {
    max-width: 850px !important;
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
}

/* ─── Streamlit Native Input Overrides ───────────────────────────── */
.stTextInput > div > div > input {
    font-family: var(--font-mono) !important;
    font-size: 0.95rem !important;
    border-radius: var(--radius-sm) !important;
    transition: all var(--transition) !important;
    letter-spacing: 0.01em;
}

.stTextInput > div > div > input:focus {
    border-color: var(--brand-accent) !important;
    box-shadow: 0 0 0 2px var(--brand-accent-dim) !important;
}

/* ─── Refined Paper Card (Main Result) ───────────────────────────── */
.paper-card {
    background-color: var(--secondary-background-color, #ffffff);
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: var(--radius-card);
    padding: 2rem 2.2rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--shadow-card);
    transition: box-shadow var(--transition), transform var(--transition);
    animation: fadeSlideUp 0.4s ease forwards;
}

.paper-card:hover {
    box-shadow: var(--shadow-hover);
    transform: translateY(-2px);
}

@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

.paper-title {
    margin-top: 0;
    padding-top: 0;
    font-size: 1.45rem;
    font-weight: 700;
    line-height: 1.35;
    letter-spacing: -0.02em;
    color: inherit;
}

.paper-authors {
    font-size: 1.05rem;
    opacity: 0.7;
    margin-top: 8px;
    margin-bottom: 18px;
    line-height: 1.4;
}

/* ─── Modern Badges ──────────────────────────────────────────────── */
.badge-container {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}
.badge {
    display: inline-flex;
    align-items: center;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    border: 1px solid transparent;
}
.badge-blue   { background: rgba(56, 189, 248, 0.1); color: #0284c7; border-color: rgba(56, 189, 248, 0.2); }
.badge-green  { background: rgba(16, 185, 129, 0.1); color: #10b981; border-color: rgba(16, 185, 129, 0.2); }
.badge-yellow { background: rgba(245, 158, 11, 0.1); color: #d97706; border-color: rgba(245, 158, 11, 0.2); }

/* ─── Minimalist Abstract Box ────────────────────────────────────── */
.abstract-box {
    background-color: var(--brand-accent-dim);
    border-left: 3px solid var(--brand-accent);
    padding: 1.2rem 1.4rem;
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    font-size: 0.95rem;
    line-height: 1.7;
    opacity: 0.9;
    margin-top: 0;
    animation: fadeSlideUp 0.5s ease forwards;
}

/* ─── Compact Metrics (Side layout) ──────────────────────────────── */
.metric-container {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding: 0.5rem 0;
}
.metric-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 700;
    opacity: 0.5;
}
.metric-value {
    font-family: var(--font-mono);
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--brand-accent);
    line-height: 1;
    letter-spacing: -0.04em;
}

/* ─── Hide Streamlit Defaults ────────────────────────────────────── */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* ─── Code Blocks (Tabs) ─────────────────────────────────────────── */
.stCodeBlock {
    border-radius: var(--radius-sm) !important;
    border: 1px solid rgba(0,0,0,0.05) !important;
}

/* ─── Scrollbar Polish ───────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.25); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.45); }
</style>
"""

def load_styles() -> None:
    """Inject custom CSS into the Streamlit app."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
