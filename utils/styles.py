"""
utils/styles.py
Refined Adaptive CSS for DOI Insight.
Uses native Streamlit variables to fix visibility across all themes.
"""

CUSTOM_CSS = """
<style>
/* ─── Google Font Import ─── */
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=JetBrains+Mono:wght@500;700&display=swap');

/* ─── Root Variables ─── */
:root {
    --brand-accent: #6366f1;
    --radius-card: 16px;
    --font-body: 'Sora', sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
}

/* ─── Global Typography ─── */
html, body, [class*="css"], .stApp {
    font-family: var(--font-body) !important;
}

/* ─── Paper Card Fix ─── */
/* Using Streamlit variables ensures the card matches the theme background */
.paper-card {
    background-color: var(--secondary-background-color); 
    border: 1px solid rgba(128, 128, 128, 0.1);
    border-radius: var(--radius-card);
    padding: 2rem;
    margin: 1.5rem 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.03);
    transition: transform 0.3s ease;
}

/* ─── Text Visibility Fix ─── */
/* We force the color to use Streamlit's primary text variable */
.paper-title {
    font-size: 1.5rem;
    font-weight: 700;
    line-height: 1.3;
    margin-bottom: 0.75rem;
    color: var(--text-color) !important;
}

.paper-authors {
    font-size: 0.95rem;
    opacity: 0.7;
    margin-bottom: 1.5rem;
    color: var(--text-color) !important;
}

/* ─── Metrics ─── */
.metric-container {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.metric-label {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-color);
    opacity: 0.5;
}

.metric-value {
    font-family: var(--font-mono);
    font-size: 2rem;
    font-weight: 700;
    color: var(--brand-accent) !important;
}

/* ─── Abstract Box ─── */
.abstract-box {
    background-color: rgba(99, 102, 241, 0.08);
    border-left: 4px solid var(--brand-accent);
    padding: 1.5rem;
    border-radius: 0 12px 12px 0;
    font-size: 0.95rem;
    line-height: 1.8;
    color: var(--text-color) !important;
}

/* ─── Recent Searches / Badges ─── */
.badge-container {
    display: flex;
    gap: 10px;
    margin-bottom: 1rem;
}

.badge {
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    background: rgba(128, 128, 128, 0.1);
    color: var(--text-color);
}

/* ─── Hide Clutter ─── */
header, footer, #MainMenu { visibility: hidden; }

/* ─── Mobile Responsiveness ─── */
@media (max-width: 640px) {
    .paper-card { padding: 1.2rem; }
    .metric-value { font-size: 1.5rem; }
}
</style>
"""

def load_styles() -> None:
    """Inject custom CSS into the Streamlit app."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
