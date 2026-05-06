# 🔬 DOI Insight

**DOI Insight** is a clean, modern research tool that lets you paste any DOI and instantly retrieve paper metadata — title, abstract, citation/reference counts, authors, journal, and more.

---

## ✨ Features

- **Instant lookup** — paste a DOI and get results in seconds
- **Smart fallback** — tries Semantic Scholar first, then Crossref automatically
- **Shareable URLs** — every search updates the URL query param (`?doi=...`) so you can share results
- **Session history** — recent searches are tracked per session for quick re-access
- **Influential citations** — surfaces highly-cited papers from the reference list
- **Export** — one-click APA citation and BibTeX generation
- **Zero API keys required** — uses public free-tier endpoints

---

## 🗂 Project Structure

```
doi_insight/
├── app.py              # Main Streamlit UI + logic
├── utils/
│   ├── __init__.py
│   ├── api.py          # API fetching, caching, validation, normalisation
│   └── styles.py       # Custom CSS (Notion/Perplexity aesthetic)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Running Locally

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/doi-insight.git
cd doi-insight
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## ☁️ Deploying to Streamlit Community Cloud

1. **Push to GitHub** — commit and push all files to a public (or private) GitHub repo.

2. **Sign in** to [share.streamlit.io](https://share.streamlit.io) with your GitHub account.

3. **New app** → select your repository, branch (`main`), and set the **Main file path** to `app.py`.

4. Click **Deploy**. No secrets or environment variables are needed.

Your app will be live at `https://YOUR_USERNAME-doi-insight-app-XXXX.streamlit.app`.

---

## 🔧 Configuration

No API keys are required. The app uses:

| API | Purpose | Rate Limit |
|-----|---------|------------|
| [Semantic Scholar Graph API](https://api.semanticscholar.org) | Primary data source | ~100 req/5 min (unauthenticated) |
| [Crossref API](https://api.crossref.org) | Fallback data source | Polite pool (no hard limit) |

Responses are cached for **1 hour** via `@st.cache_data(ttl=3600)` to minimise repeat API calls.

---

## 📝 Example DOIs to Try

```
10.1038/nature12373          # DeepMind — AlphaFold precursor
10.1126/science.1218197      # CRISPR-Cas9 original paper
10.1145/3442188.3445922      # "Stochastic Parrots" (LLMs)
10.48550/arXiv.1706.03762    # "Attention Is All You Need"
10.1016/j.cell.2016.05.010   # Single-cell RNA sequencing
```

---

## 📄 License

MIT — free to use, fork, and deploy.
