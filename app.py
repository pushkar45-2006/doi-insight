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
    st.session_state.recent_searches = st.session_state.recent_searches[:8]


# ─── Hero Header ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="doi-hero">
        <div class="doi-hero-badge">🔬 Research Intelligence</div>
        <h1>DOI Insight</h1>
        <p>Paste any DOI to instantly surface paper metadata, citations, and more.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─── Search Area ──────────────────────────────────────────────────────────────
st.markdown('<div class="search-wrapper">', unsafe_allow_html=True)

col_input, col_btn = st.columns([5, 1], gap="small")

with col_input:
    doi_raw = st.text_input(
        label="DOI",
        value=st.session_state.doi_input,
        placeholder="e.g.  10.1038/nature12373  or  https://doi.org/10.1126/science.1218197",
        label_visibility="collapsed",
        key="doi_field",
    )

with col_btn:
    search_clicked = st.button("Search", type="primary", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ─── Recent Searches ─────────────────────────────────────────────────────────
if st.session_state.recent_searches:
    st.markdown('<p class="recents-header">Recent Searches</p>', unsafe_allow_html=True)
    recent_cols = st.columns(min(len(st.session_state.recent_searches), 4), gap="small")
    for idx, (rdoi, rtitle) in enumerate(st.session_state.recent_searches[:4]):
        with recent_cols[idx]:
            label = rtitle[:28] + "…" if len(rtitle) > 28 else rtitle
            if st.button(label, key=f"recent_{idx}", help=rdoi):
                st.session_state.doi_input = rdoi
                st.query_params["doi"] = rdoi
                st.rerun()

    st.markdown('<div class="doi-divider"></div>', unsafe_allow_html=True)

# ─── Trigger Search ───────────────────────────────────────────────────────────
def do_search(doi_raw: str) -> None:
    doi_clean = normalize_doi(doi_raw.strip())

    if not doi_clean:
        st.warning("Please enter a DOI.")
        return

    if not validate_doi(doi_clean):
        st.warning(
            f'**\u201c{doi_clean}\u201d** doesn\'t look like a valid DOI.  \n'
            "A DOI usually starts with `10.` followed by a registrant code and suffix, "
            "e.g. `10.1038/nature12373`."
        )
        return

    # Write DOI to URL so it's shareable
    st.query_params["doi"] = doi_clean
    st.session_state.doi_input = doi_clean

    with st.spinner("🔍 Querying Semantic Scholar…"):
        paper = fetch_paper(doi_clean)

    if paper["status"] == "rate_limited":
        st.error(
            "⏱️ **Rate limited.** The Semantic Scholar API is temporarily throttling requests. "
            "Please wait a moment and try again."
        )
        return

    if paper["status"] == "not_found":
        st.error(
            f"😕 **Paper not found** for DOI `{doi_clean}`.  \n"
            "Please double-check the DOI or try a slightly different format."
        )
        return

    st.session_state.current_paper = paper
    _add_recent(doi_clean, paper.get("title", doi_clean))


if search_clicked and doi_raw:
    do_search(doi_raw)
elif st.session_state.doi_input and not st.session_state.current_paper:
    # Auto-load from query param on first visit
    do_search(st.session_state.doi_input)


# ─── Result Display ───────────────────────────────────────────────────────────
paper = st.session_state.current_paper

if paper and paper.get("status") == "ok":

    title = paper.get("title", "Untitled")
    year = paper.get("year") or "–"
    journal = paper.get("journal") or "–"
    authors = paper.get("authors", [])
    citation_count = paper.get("citation_count")
    reference_count = paper.get("reference_count")
    abstract = paper.get("abstract", "")
    url = paper.get("url", "")
    source = paper.get("source", "")
    doi = paper.get("doi", "")

    # ── Title + meta chips ──────────────────────────────────────────────────
    authors_str = ", ".join(authors[:6])
    if len(authors) > 6:
        authors_str += f" +{len(authors) - 6} more"

    journal_chip = (
        f'<span class="meta-chip journal">📖 {journal}</span>' if journal != "–" else ""
    )
    source_chip = f'<span class="meta-chip source">⚡ via {source}</span>'
    year_chip = f'<span class="meta-chip">📅 {year}</span>'

    st.markdown(
        f"""
        <div class="result-card">
            <div class="paper-title">{title}</div>
            <div style="font-size:0.82rem;opacity:0.6;margin-bottom:0.6rem">{authors_str}</div>
            <div class="paper-meta">
                {year_chip}
                {journal_chip}
                {source_chip}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Metrics ──────────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(
            "📚 Citations",
            f"{citation_count:,}" if citation_count is not None else "–",
        )
    with c2:
        st.metric(
            "🔗 References",
            f"{reference_count:,}" if reference_count is not None else "–",
        )
    with c3:
        st.metric("📅 Year", year)

    st.markdown('<div class="doi-divider"></div>', unsafe_allow_html=True)

    # ── Abstract ─────────────────────────────────────────────────────────────
    if abstract:
        with st.expander("📄 Abstract", expanded=True):
            st.markdown(
                f'<div style="font-size:0.9rem;line-height:1.75;opacity:0.85">{abstract}</div>',
                unsafe_allow_html=True,
            )
    else:
        st.info("No abstract available from the data source.")

    st.markdown('<div class="doi-divider"></div>', unsafe_allow_html=True)

    # ── Action Buttons ────────────────────────────────────────────────────────
    st.markdown("**🛠️ Actions**")
    act1, act2, act3 = st.columns(3, gap="small")

    with act1:
        if url:
            st.link_button("🔗 Read Paper", url, use_container_width=True)
        else:
            st.button("🔗 Read Paper", disabled=True, use_container_width=True)

    with act2:
        if st.button("📋 Copy APA Citation", use_container_width=True):
            st.session_state["show_apa"] = not st.session_state.get("show_apa", False)

    with act3:
        if st.button("📋 Copy BibTeX", use_container_width=True):
            st.session_state["show_bibtex"] = not st.session_state.get("show_bibtex", False)

    if st.session_state.get("show_apa"):
        st.markdown("**APA Citation**")
        st.code(format_apa(paper), language=None)

    if st.session_state.get("show_bibtex"):
        st.markdown("**BibTeX**")
        st.code(format_bibtex(paper), language="bibtex")

    # ── DOI copy ─────────────────────────────────────────────────────────────
    with st.expander("🔑 DOI & Identifiers"):
        st.code(f"https://doi.org/{doi}", language=None)
        if url and url != f"https://doi.org/{doi}":
            st.caption(f"Direct link: {url}")

    # ── Influential Citations / Related Papers ────────────────────────────────
    influential = paper.get("influential_citations", [])
    if influential:
        st.markdown('<div class="doi-divider"></div>', unsafe_allow_html=True)
        st.markdown("### 🌟 Highly Cited Papers in References")
        st.caption("Papers from the reference list that themselves have significant impact.")

        for cp in influential:
            cp_title = cp.get("title", "Untitled")
            cp_year = cp.get("year", "")
            cp_cites = cp.get("citationCount", 0)
            cp_authors = cp.get("authors", [])
            cp_author_str = ", ".join(a.get("name", "") for a in cp_authors[:3])
            cp_doi = (cp.get("externalIds") or {}).get("DOI", "")
            cp_url = cp.get("url", "")

            col_info, col_link = st.columns([5, 1], gap="small")
            with col_info:
                st.markdown(
                    f"""
                    <div class="citation-item">
                        <div class="c-title">{cp_title}</div>
                        <div class="c-meta">{cp_author_str}{' · ' if cp_author_str else ''}{cp_year} · {cp_cites:,} citations</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col_link:
                link = f"https://doi.org/{cp_doi}" if cp_doi else cp_url
                if link:
                    st.link_button("↗", link, use_container_width=True)

    # ── Clear Button ─────────────────────────────────────────────────────────
    st.markdown('<div class="doi-divider"></div>', unsafe_allow_html=True)
    if st.button("🗑️ Clear Results", use_container_width=False):
        st.session_state.current_paper = None
        st.session_state.doi_input = ""
        st.session_state["show_apa"] = False
        st.session_state["show_bibtex"] = False
        st.query_params.clear()
        st.rerun()

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="text-align:center;margin-top:4rem;font-size:0.72rem;opacity:0.35;letter-spacing:0.03em">
        DOI Insight · Data from
        <a href="https://www.semanticscholar.org" target="_blank" style="opacity:0.7">Semantic Scholar</a>
        &amp;
        <a href="https://www.crossref.org" target="_blank" style="opacity:0.7">Crossref</a>
    </div>
    """,
    unsafe_allow_html=True,
)
