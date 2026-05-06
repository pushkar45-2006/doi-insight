"""
app.py — DOI Insight
Main Streamlit application.
"""

import streamlit as st
from utils.styles import load_styles
from utils.api import (
    validate_doi,
    normalize_doi,
    fetch_paper,
    format_apa,
    format_bibtex,
)

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DOI Insight",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

load_styles()

# ─── Session State Init ───────────────────────────────────────────────────────
if "recent_searches" not in st.session_state:
    st.session_state.recent_searches = []   # list of (doi, title) tuples
if "current_paper" not in st.session_state:
    st.session_state.current_paper = None
if "doi_input" not in st.session_state:
    st.session_state.doi_input = ""

# ─── Query Param: shareable URL support ──────────────────────────────────────
params = st.query_params
if "doi" in params and not st.session_state.doi_input:
    st.session_state.doi_input = params["doi"]

# ─── Helper: update recent searches ──────────────────────────────────────────
def _add_recent(doi: str, title: str) -> None:
    existing = [r[0] for r in st.session_state.recent_searches]
    if doi not in existing:
        st.session_state.recent_searches.insert(0, (doi, title))
    st.session_state.recent_searches = st.session_state.recent_searches[:4] # Keep it tight (max 4)

# ─── Hero Header ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="text-align: center; padding-bottom: 2rem;">
        <h1 style="font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem; color: #111827;">🔍 DOI Insight</h1>
        <p style="color: #6b7280; font-size: 1.1rem;">Paste any DOI to instantly surface paper metadata and citations.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─── Search Area ──────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1], gap="small")

with col_input:
    doi_raw = st.text_input(
        label="DOI",
        value=st.session_state.doi_input,
        placeholder="e.g. 10.1038/nature12373",
        label_visibility="collapsed",
        key="doi_field",
    )

with col_btn:
    search_clicked = st.button("Search", type="primary", use_container_width=True)

# ─── Recent Searches ─────────────────────────────────────────────────────────
if st.session_state.recent_searches:
    st.caption("Recent Searches:")
    recent_cols = st.columns(min(len(st.session_state.recent_searches), 4), gap="small")
    for idx, (rdoi, rtitle) in enumerate(st.session_state.recent_searches[:4]):
        with recent_cols[idx]:
            label = rtitle[:20] + "…" if len(rtitle) > 20 else rtitle
            if st.button(label, key=f"recent_{idx}", help=rdoi, use_container_width=True):
                st.session_state.doi_input = rdoi
                st.query_params["doi"] = rdoi
                st.rerun()

st.divider()

# ─── Trigger Search Logic ─────────────────────────────────────────────────────
def do_search(doi_raw: str) -> None:
    doi_clean = normalize_doi(doi_raw.strip())

    if not doi_clean:
        st.warning("Please enter a DOI.")
        return

    if not validate_doi(doi_clean):
        st.warning(f'**"{doi_clean}"** doesn\'t look like a valid DOI format.')
        return

    # Write DOI to URL so it's shareable
    st.query_params["doi"] = doi_clean
    st.session_state.doi_input = doi_clean

    with st.spinner("🔍 Querying Databases..."):
        paper = fetch_paper(doi_clean)

    if paper.get("status") == "rate_limited":
        st.error("⏱️ **Rate limited.** The API is throttling requests. Please wait a moment.")
        return

    if paper.get("status") == "not_found" or not paper:
        st.error(f"😕 **Paper not found** for DOI `{doi_clean}`. Please double-check.")
        return

    st.session_state.current_paper = paper
    _add_recent(doi_clean, paper.get("title", doi_clean))

# Execute Search
if search_clicked and doi_raw:
    do_search(doi_raw)
elif st.session_state.doi_input and not st.session_state.current_paper:
    do_search(st.session_state.doi_input)


# ─── Result Display ───────────────────────────────────────────────────────────
paper = st.session_state.current_paper

if paper and paper.get("status") in ["ok", None]: # 'None' fallback in case API doesn't set status

    title = paper.get("title", "Untitled")
    year = paper.get("year") or "N/A"
    journal = paper.get("journal") or "Unknown Journal"
    
    # Handle Journal dict from Semantic Scholar
    if isinstance(journal, dict):
        journal = journal.get('name', 'Unknown Journal')

    authors = paper.get("authors", [])
    # Extract names safely
    author_names = [a.get("name", "") if isinstance(a, dict) else str(a) for a in authors]
    
    citation_count = paper.get("citation_count", paper.get("citationCount", 0))
    reference_count = paper.get("reference_count", paper.get("referenceCount", 0))
    abstract = paper.get("abstract", "")
    url = paper.get("url", "")
    source = paper.get("source", "Semantic Scholar")
    doi = paper.get("doi", st.session_state.doi_input)

    authors_str = ", ".join(author_names[:6])
    if len(author_names) > 6:
        authors_str += f" +{len(author_names) - 6} more"

    # ── 1. Main Paper Card ──────────────────────────────────────────────────
    st.markdown(f"""
    <div class="paper-card">
        <h2 class="paper-title">{title}</h2>
        <div class="paper-authors">{authors_str}</div>
        <div class="badge-container">
            <span class="badge badge-blue">📅 {year}</span>
            <span class="badge badge-green">📖 {journal}</span>
            <span class="badge badge-yellow">⚡ {source}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 2. Metrics & Abstract (Side-by-Side) ─────────────────────────────────
    col_metrics, col_abstract = st.columns([1, 2.5])
    
    with col_metrics:
        st.markdown(f"""
        <div class="metric-container">
            <span class="metric-label">Citations</span>
            <span class="metric-value">{citation_count:,}</span>
        </div>
        <div class="metric-container" style="margin-top: 1.5rem;">
            <span class="metric-label">References</span>
            <span class="metric-value">{reference_count:,}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col_abstract:
        if abstract:
            st.markdown(f'<div class="abstract-box">{abstract}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="abstract-box" style="color: #9ca3af; font-style: italic;">No abstract available from the data source.</div>', unsafe_allow_html=True)

    st.write("") # Spacer

    # ── 3. Actions & Citations (Tabs) ─────────────────────────────────────────
    st.subheader("Actions & Citations")
    
    if url:
        st.link_button("🔗 Read Full Paper", url, type="primary")
    
    tab1, tab2, tab3 = st.tabs(["APA Citation", "BibTeX", "Identifiers"])
    
    with tab1:
        st.code(format_apa(paper), language="text")
    with tab2:
        st.code(format_bibtex(paper), language="bibtex")
    with tab3:
        st.code(f"DOI: {doi}\nURL: {url}", language="text")

    # ── 4. Influential Citations / Related Papers ─────────────────────────────
    influential = paper.get("influential_citations", [])
    if influential:
        st.divider()
        st.markdown("### 🌟 Highly Cited References")
        st.caption("Papers from this reference list that have significant impact.")

        for cp in influential[:3]: # Limit to top 3 for clean UI
            cp_title = cp.get("title", "Untitled")
            cp_year = cp.get("year", "")
            cp_cites = cp.get("citationCount", 0)
            cp_authors = cp.get("authors", [])
            cp_author_str = ", ".join(a.get("name", "") for a in cp_authors[:3])
            cp_doi = (cp.get("externalIds") or {}).get("DOI", "")
            cp_url = cp.get("url", f"https://doi.org/{cp_doi}" if cp_doi else "")

            with st.container(border=True):
                col_info, col_link = st.columns([5, 1])
                with col_info:
                    st.markdown(f"**{cp_title}**")
                    st.caption(f"{cp_author_str} · {cp_year} · 📚 {cp_cites:,} citations")
                with col_link:
                    if cp_url:
                        st.link_button("View ↗", cp_url)

    # ── Clear Button ─────────────────────────────────────────────────────────
    st.write("")
    if st.button("🗑️ Clear Results"):
        st.session_state.current_paper = None
        st.session_state.doi_input = ""
        st.query_params.clear()
        st.rerun()

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="text-align:center;margin-top:4rem;font-size:0.75rem;color:#9ca3af;">
        DOI Insight · Powered by <a href="https://www.semanticscholar.org" style="color:#6b7280;">Semantic Scholar</a>
    </div>
    """,
    unsafe_allow_html=True,
)
