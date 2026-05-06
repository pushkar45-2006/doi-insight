"""
utils/api.py
API fetching, caching, fallback logic, and DOI validation for DOI Insight.
"""

import re
import time
import streamlit as st
import requests
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SEMANTIC_SCHOLAR_BASE = "https://api.semanticscholar.org/graph/v1"
CROSSREF_BASE = "https://api.crossref.org/works"
POLITE_EMAIL = "doi-insight-app@example.com"   # used in Crossref polite pool

SS_FIELDS = (
    "title,abstract,year,citationCount,referenceCount,"
    "authors,publicationVenue,externalIds,url,"
    "influentialCitationCount,citations"
)

SS_CITATION_FIELDS = (
    "title,year,authors,citationCount,externalIds,url"
)

DOI_RE = re.compile(
    r"^10\.\d{4,9}/[-._;()/:A-Za-z0-9]+$"
)

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_doi(doi: str) -> bool:
    """Return True if the string looks like a valid DOI."""
    doi = doi.strip()
    # Strip common prefixes users might paste
    for prefix in ("https://doi.org/", "http://doi.org/", "doi.org/", "doi:"):
        if doi.lower().startswith(prefix):
            doi = doi[len(prefix):]
            break
    return bool(DOI_RE.match(doi))


def normalize_doi(doi: str) -> str:
    """Strip URL prefixes and return the bare DOI string."""
    doi = doi.strip()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi.org/", "doi:"):
        if doi.lower().startswith(prefix):
            doi = doi[len(prefix):]
            break
    return doi

# ---------------------------------------------------------------------------
# Semantic Scholar
# ---------------------------------------------------------------------------

@st.cache_data(ttl=3600, show_spinner=False)
def _fetch_semantic_scholar(doi: str) -> Optional[dict]:
    """
    Fetch paper data from Semantic Scholar Graph API.
    Returns raw JSON dict or None on failure.
    """
    url = f"{SEMANTIC_SCHOLAR_BASE}/paper/DOI:{doi}"
    params = {"fields": SS_FIELDS}
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        if resp.status_code == 429:
            # Rate limited — surface this to caller
            return {"_error": "rate_limited"}
        return None
    except requests.RequestException:
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def _fetch_influential_citations(paper_id: str) -> list:
    """
    Fetch the top influential citations for a given Semantic Scholar paper ID.
    Returns a list of up to 5 citation dicts.
    """
    url = f"{SEMANTIC_SCHOLAR_BASE}/paper/{paper_id}/citations"
    params = {
        "fields": SS_CITATION_FIELDS,
        "limit": 20,
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code != 200:
            return []
        data = resp.json()
        citations = data.get("data", [])
        # Filter for highly cited papers (proxy for influential)
        filtered = [
            c["citedPaper"]
            for c in citations
            if c.get("citedPaper") and c["citedPaper"].get("citationCount", 0) > 50
        ]
        # Sort by citation count descending and take top 3
        filtered.sort(key=lambda x: x.get("citationCount", 0), reverse=True)
        return filtered[:3]
    except requests.RequestException:
        return []

# ---------------------------------------------------------------------------
# Crossref Fallback
# ---------------------------------------------------------------------------

@st.cache_data(ttl=3600, show_spinner=False)
def _fetch_crossref(doi: str) -> Optional[dict]:
    """
    Fetch paper data from Crossref API (polite pool).
    Returns raw JSON dict or None on failure.
    """
    url = f"{CROSSREF_BASE}/{doi}"
    headers = {
        "User-Agent": f"DOIInsight/1.0 (mailto:{POLITE_EMAIL})",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        return None
    except requests.RequestException:
        return None

# ---------------------------------------------------------------------------
# Normalisation
# ---------------------------------------------------------------------------

def _normalise_semantic_scholar(data: dict, doi: str) -> dict:
    """Convert Semantic Scholar response into unified paper dict."""
    authors = [a.get("name", "") for a in data.get("authors", [])]
    venue = data.get("publicationVenue") or {}
    journal = venue.get("name") or data.get("venue") or "N/A"

    external_ids = data.get("externalIds", {}) or {}
    paper_url = (
        data.get("url")
        or (f"https://doi.org/{doi}" if doi else None)
        or (f"https://arxiv.org/abs/{external_ids.get('ArXiv')}" if external_ids.get("ArXiv") else None)
        or ""
    )

    return {
        "title": data.get("title") or "Untitled",
        "abstract": data.get("abstract") or "",
        "year": data.get("year"),
        "citation_count": data.get("citationCount"),
        "reference_count": data.get("referenceCount"),
        "authors": authors,
        "journal": journal,
        "doi": doi,
        "url": paper_url,
        "source": "Semantic Scholar",
        "paper_id": data.get("paperId", ""),
    }


def _normalise_crossref(data: dict, doi: str) -> dict:
    """Convert Crossref response into unified paper dict."""
    msg = data.get("message", {})

    # Authors
    authors = []
    for a in msg.get("author", []):
        given = a.get("given", "")
        family = a.get("family", "")
        name = f"{given} {family}".strip()
        if name:
            authors.append(name)

    # Year
    year = None
    for date_field in ("published-print", "published-online", "issued"):
        parts = msg.get(date_field, {}).get("date-parts", [[]])
        if parts and parts[0]:
            year = parts[0][0]
            break

    # Journal
    container = msg.get("container-title", [])
    journal = container[0] if container else "N/A"

    # Abstract (Crossref sometimes returns JATS XML — strip tags)
    abstract_raw = msg.get("abstract", "")
    abstract = re.sub(r"<[^>]+>", "", abstract_raw).strip()

    paper_url = msg.get("URL") or (f"https://doi.org/{doi}" if doi else "")

    return {
        "title": (msg.get("title") or ["Untitled"])[0],
        "abstract": abstract,
        "year": year,
        "citation_count": msg.get("is-referenced-by-count"),
        "reference_count": msg.get("references-count"),
        "authors": authors,
        "journal": journal,
        "doi": doi,
        "url": paper_url,
        "source": "Crossref",
        "paper_id": "",
    }

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def fetch_paper(doi: str) -> dict:
    """
    Main entry point. Given a validated DOI string, try Semantic Scholar
    then fall back to Crossref. Returns a normalised paper dict with a
    'status' key: 'ok', 'not_found', 'rate_limited', or 'error'.
    """
    doi = normalize_doi(doi)

    # --- Semantic Scholar ---
    ss_raw = _fetch_semantic_scholar(doi)

    if ss_raw and ss_raw.get("_error") == "rate_limited":
        return {"status": "rate_limited", "source": "Semantic Scholar"}

    if ss_raw and ss_raw.get("title"):
        paper = _normalise_semantic_scholar(ss_raw, doi)
        paper["status"] = "ok"

        # Fetch influential citations if we have a paper ID
        if paper.get("paper_id"):
            paper["influential_citations"] = _fetch_influential_citations(paper["paper_id"])
        else:
            paper["influential_citations"] = []

        return paper

    # --- Crossref Fallback ---
    cr_raw = _fetch_crossref(doi)

    if cr_raw and cr_raw.get("message"):
        paper = _normalise_crossref(cr_raw, doi)
        paper["status"] = "ok"
        paper["influential_citations"] = []
        return paper

    return {"status": "not_found", "doi": doi}

# ---------------------------------------------------------------------------
# Citation Formatters
# ---------------------------------------------------------------------------

def format_apa(paper: dict) -> str:
    """Generate an APA 7th edition citation string."""
    authors = paper.get("authors", [])
    year = paper.get("year", "n.d.")
    title = paper.get("title", "")
    journal = paper.get("journal", "")
    doi = paper.get("doi", "")

    if not authors:
        author_str = "Unknown Author"
    elif len(authors) == 1:
        parts = authors[0].rsplit(" ", 1)
        author_str = f"{parts[-1]}, {parts[0][0]}." if len(parts) > 1 else authors[0]
    else:
        formatted = []
        for a in authors[:20]:
            parts = a.rsplit(" ", 1)
            formatted.append(f"{parts[-1]}, {parts[0][0]}." if len(parts) > 1 else a)
        if len(authors) > 20:
            author_str = ", ".join(formatted) + ", ... " + formatted[-1]
        else:
            author_str = ", & ".join([", ".join(formatted[:-1]), formatted[-1]])

    lines = [f"{author_str} ({year}). {title}."]
    if journal and journal != "N/A":
        lines.append(f" *{journal}*.")
    if doi:
        lines.append(f" https://doi.org/{doi}")

    return "".join(lines)


def format_bibtex(paper: dict) -> str:
    """Generate a BibTeX entry."""
    doi = paper.get("doi", "")
    year = paper.get("year", "")
    title = paper.get("title", "")
    journal = paper.get("journal", "N/A")
    authors = paper.get("authors", [])

    # Build a cite key from first author surname + year
    first_author = authors[0] if authors else "Unknown"
    surname = first_author.rsplit(" ", 1)[-1].lower()
    surname_clean = re.sub(r"[^a-z]", "", surname)
    cite_key = f"{surname_clean}{year or 'nd'}"

    author_str = " and ".join(authors) if authors else "Unknown"

    lines = [
        f"@article{{{cite_key},",
        f'  title     = {{{title}}},',
        f'  author    = {{{author_str}}},',
    ]
    if year:
        lines.append(f'  year      = {{{year}}},')
    if journal and journal != "N/A":
        lines.append(f'  journal   = {{{journal}}},')
    if doi:
        lines.append(f'  doi       = {{{doi}}},')
        lines.append(f'  url       = {{https://doi.org/{doi}}}')
    lines.append("}")

    return "\n".join(lines)
