"""
utils/styles.py
Custom CSS definitions for DOI Insight — Notion/Perplexity-inspired aesthetic.
Works in both Streamlit light and dark modes.
"""

CUSTOM_CSS = """
<style>
/* ─── Google Font Import ─────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ─── Root Variables ─────────────────────────────────────────────── */
:root {
    --brand-accent: #6366f1;          /* indigo */
    --brand-accent-soft: #818cf8;
    --brand-accent-dim: rgba(99, 102, 241, 0.12);
    --brand-success: #10b981;
    --brand-warning: #f59e0b;
    --radius-card: 14px;
    --radius-sm: 8px;
    --shadow-card: 0 1px 3px rgba(0,0,0,.08), 0 8px 24px rgba(0,0,0,.06);
    --shadow-hover: 0 2px 6px rgba(0,0,0,.10), 0 12px 32px rgba(0,0,0,.10);
    --transition: 0.2s ease;
    --font-body: 'Sora', sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
}

/* ─── Global Typography ──────────────────────────────────────────── */
html, body, .stApp, [class*="css"] {
    font-family: var(--font-body) !important;
}

/* ─── App Background ─────────────────────────────────────────────── */
.stApp {
    background: var(--background-color, #fafafa);
}

/* ─── Main content max-width constraint ─────────────────────────── */
.block-container {
    max-width: 820px !important;
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
}

/* ─── Hero Header ────────────────────────────────────────────────── */
.doi-hero {
    text-align: center;
    padding: 3rem 0 2rem;
}

.doi-hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--brand-accent-dim);
    color: var(--brand-accent-soft);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}

.doi-hero h1 {
    font-size: clamp(1.9rem, 5vw, 2.8rem);
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.15;
    margin: 0 0 0.6rem;
    background: linear-gradient(135deg, var(--brand-accent) 0%, var(--brand-accent-soft) 60%, #a5b4fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.doi-hero p {
    font-size: 1.05rem;
    font-weight: 300;
    opacity: 0.65;
    margin: 0;
    letter-spacing: -0.01em;
}

/* ─── Search Container ───────────────────────────────────────────── */
.search-wrapper {
    background: var(--secondary-background-color, #ffffff);
    border: 1.5px solid rgba(99, 102, 241, 0.2);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin: 1.5rem 0;
    box-shadow: var(--shadow-card);
    transition: border-color var(--transition), box-shadow var(--transition);
}

.search-wrapper:focus-within {
    border-color: var(--brand-accent);
    box-shadow: 0 0 0 3px var(--brand-accent-dim), var(--shadow-card);
}

/* ─── Streamlit Input Override ───────────────────────────────────── */
.stTextInput > div > div > input {
    font-family: var(--font-mono) !important;
    font-size: 0.9rem !important;
    border-radius: var(--radius-sm) !important;
    border: 1.5px solid transparent !important;
    background: transparent !important;
    transition: all var(--transition) !important;
    letter-spacing: 0.01em;
}

.stTextInput > div > div > input:focus {
    border-color: var(--brand-accent) !important;
    box-shadow: 0 0 0 2px var(--brand-accent-dim) !important;
}

.stTextInput label {
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
    opacity: 0.55 !important;
}

/* ─── Buttons ────────────────────────────────────────────────────── */
.stButton > button {
    font-family: var(--font-body) !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    border-radius: var(--radius-sm) !important;
    transition: all var(--transition) !important;
    letter-spacing: -0.01em;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--brand-accent) 0%, #818cf8 100%) !important;
    border: none !important;
    color: #fff !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.35) !important;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(99,102,241,0.45) !important;
}

/* ─── Result Card ────────────────────────────────────────────────── */
.result-card {
    background: var(--secondary-background-color, #ffffff);
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: var(--radius-card);
    padding: 1.8rem 2rem;
    margin: 1.5rem 0;
    box-shadow: var(--shadow-card);
    transition: box-shadow var(--transition);
    animation: fadeSlideUp 0.35s ease forwards;
}

.result-card:hover {
    box-shadow: var(--shadow-hover);
}

@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

.result-card .paper-title {
    font-size: 1.3rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    line-height: 1.35;
    margin-bottom: 0.5rem;
}

.result-card .paper-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 0.75rem 0;
    align-items: center;
}

.meta-chip {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 0.78rem;
    font-weight: 500;
    padding: 3px 10px;
    border-radius: 999px;
    background: var(--brand-accent-dim);
    color: var(--brand-accent-soft);
    border: 1px solid rgba(99, 102, 241, 0.18);
    white-space: nowrap;
}

.meta-chip.journal {
    background: rgba(16,185,129,0.1);
    color: #10b981;
    border-color: rgba(16,185,129,0.2);
}

.meta-chip.source {
    background: rgba(245,158,11,0.1);
    color: #f59e0b;
    border-color: rgba(245,158,11,0.2);
}

/* ─── Metric Cards ───────────────────────────────────────────────── */
.metric-row {
    display: flex;
    gap: 1rem;
    margin: 1.2rem 0;
    flex-wrap: wrap;
}

.metric-card {
    flex: 1;
    min-width: 100px;
    background: var(--brand-accent-dim);
    border: 1px solid rgba(99, 102, 241, 0.18);
    border-radius: var(--radius-sm);
    padding: 1rem 1.2rem;
    text-align: center;
    transition: transform var(--transition);
}

.metric-card:hover {
    transform: translateY(-2px);
}

.metric-card .metric-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--brand-accent);
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 4px;
    font-family: var(--font-mono);
}

.metric-card .metric-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    opacity: 0.55;
}

/* ─── Action Buttons Row ─────────────────────────────────────────── */
.action-row {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}

/* ─── Influential Citations Card ─────────────────────────────────── */
.related-section h4 {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    opacity: 0.45;
    margin-bottom: 0.75rem;
}

.citation-item {
    background: var(--secondary-background-color, #ffffff);
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: var(--radius-sm);
    padding: 0.85rem 1rem;
    margin-bottom: 0.5rem;
    transition: all var(--transition);
    animation: fadeSlideUp 0.4s ease forwards;
}

.citation-item:hover {
    border-color: var(--brand-accent);
    box-shadow: 0 2px 8px rgba(99,102,241,0.12);
    transform: translateX(2px);
}

.citation-item .c-title {
    font-size: 0.88rem;
    font-weight: 600;
    letter-spacing: -0.01em;
    line-height: 1.3;
    margin-bottom: 4px;
}

.citation-item .c-meta {
    font-size: 0.75rem;
    opacity: 0.5;
}

/* ─── Recent Searches ────────────────────────────────────────────── */
.recents-header {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    opacity: 0.4;
    margin-bottom: 0.5rem;
}

/* ─── Divider ────────────────────────────────────────────────────── */
.doi-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.2) 40%, rgba(99,102,241,0.2) 60%, transparent);
    margin: 1.5rem 0;
}

/* ─── Expander Polish ────────────────────────────────────────────── */
.streamlit-expanderHeader {
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    border-radius: var(--radius-sm) !important;
}

.streamlit-expanderContent {
    font-size: 0.9rem !important;
    line-height: 1.7 !important;
    opacity: 0.85;
}

/* ─── Spinner text ───────────────────────────────────────────────── */
.stSpinner > div {
    font-family: var(--font-body) !important;
    font-size: 0.85rem !important;
    opacity: 0.7;
}

/* ─── Scrollbar ──────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.5); }
</style>
"""


def load_styles() -> None:
    """Inject custom CSS into the Streamlit app."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
