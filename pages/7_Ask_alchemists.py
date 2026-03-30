import json
from pathlib import Path

import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =========================================================
# Paths
# =========================================================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# =========================================================
# Styling
# =========================================================
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at top left, rgba(30,111,92,0.18) 0%, transparent 28%),
        radial-gradient(circle at top right, rgba(253,184,19,0.08) 0%, transparent 18%),
        linear-gradient(180deg, #040816 0%, #07111d 45%, #081423 100%);
    color: #F8FAFC;
}

.block-container {
    padding-top: 1.6rem;
    padding-bottom: 2.4rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
    max-width: 1400px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141B2D 0%, #182133 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}

section[data-testid="stSidebar"] * {
    color: #E5E7EB !important;
}

.hero-box {
    background: linear-gradient(135deg, rgba(30,111,92,0.96) 0%, rgba(11,60,93,0.96) 100%);
    padding: 2.4rem;
    border-radius: 28px;
    color: white;
    box-shadow: 0 20px 46px rgba(0,0,0,0.34);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 1.4rem;
}

.hero-title {
    font-size: 2.6rem;
    font-weight: 900;
    margin-bottom: 0.9rem;
}

.hero-highlight {
    color: #FDB813 !important;
}

.hero-text {
    font-size: 1.03rem;
    line-height: 1.8;
    color: #F3F7F6 !important;
}

.card {
    background: linear-gradient(180deg, #F8FAFC 0%, #EEF2F7 100%);
    border-radius: 22px;
    padding: 1.3rem;
    box-shadow: 0 10px 24px rgba(0,0,0,0.16);
    margin-bottom: 1rem;
    border: 1px solid rgba(0,0,0,0.05);
}

.card-title {
    color: #0B3C5D;
    font-size: 1.25rem;
    font-weight: 850;
    margin-bottom: 0.5rem;
}

.card-text {
    color: #334155;
    font-size: 0.97rem;
    line-height: 1.75;
}

.question-chip {
    display: inline-block;
    background: rgba(255,255,255,0.10);
    color: #F8FAFC;
    border: 1px solid rgba(255,255,255,0.14);
    padding: 0.55rem 0.95rem;
    border-radius: 999px;
    font-size: 0.84rem;
    font-weight: 700;
    margin: 0.2rem 0.35rem 0.35rem 0;
}

.answer-box {
    background: linear-gradient(90deg, rgba(30,111,92,0.20), rgba(11,60,93,0.18));
    border-left: 6px solid #FDB813;
    border-radius: 18px;
    padding: 1.1rem 1.25rem;
    margin-top: 0.8rem;
    margin-bottom: 1.3rem;
    color: #E5F3EE !important;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 10px 24px rgba(0,0,0,0.16);
    font-size: 0.98rem;
    line-height: 1.75;
}

.source-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 0.95rem 1rem;
    margin-top: 0.7rem;
    color: #CBD5E1 !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# Data loading
# =========================================================
@st.cache_data
def load_knowledge_base():
    kb_path = DATA_DIR / "rag_knowledge_base.json"
    with open(kb_path, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_resource
def build_vector_store(kb_items):
    texts = [item["text"] for item in kb_items]
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(texts)
    return vectorizer, matrix

def retrieve_chunks(query, kb_items, vectorizer, matrix, top_k=3):
    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, matrix).flatten()
    top_idx = scores.argsort()[::-1][:top_k]

    results = []
    for idx in top_idx:
        results.append({
            "title": kb_items[idx]["title"],
            "text": kb_items[idx]["text"],
            "score": float(scores[idx])
        })
    return results

def build_answer(query, retrieved):
    if not retrieved:
        return "I could not find a strong match in the dashboard knowledge base."

    top = retrieved[0]
    answer = f"Based on the dashboard knowledge base, the most relevant insight is: {top['text']}"

    if len(retrieved) > 1:
        supporting_titles = ", ".join([item["title"] for item in retrieved[:3]])
        answer += f" Related context was also found in: {supporting_titles}."

    return answer

# =========================================================
# Page content
# =========================================================
st.markdown("""
<div class="hero-box">
    <div class="hero-title">Ask <span class="hero-highlight">SPICE</span></div>
    <div class="hero-text">
        This AI assistant helps explain dashboard results in simple language.
        You can ask about solar simulation, design choices, financial meaning,
        environmental impact, and dashboard terms.
    </div>
</div>
""", unsafe_allow_html=True)

kb_items = load_knowledge_base()
vectorizer, matrix = build_vector_store(kb_items)

example_questions = [
    "What is normalized output?",
    "Why is May usually the peak month?",
    "How does tilt affect production?",
    "What does reference comparison mean?",
    "How does the dashboard support decision making?",
    "What does the financial impact page show?",
]

st.markdown('<div class="card"><div class="card-title">Suggested Questions</div>', unsafe_allow_html=True)
for q in example_questions:
    st.markdown(f'<span class="question-chip">{q}</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

user_query = st.text_input("Ask a question about the dashboard")

if user_query:
    retrieved = retrieve_chunks(user_query, kb_items, vectorizer, matrix, top_k=3)
    answer = build_answer(user_query, retrieved)

    st.markdown(f'<div class="answer-box"><strong>Answer:</strong> {answer}</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">Retrieved Sources</div>', unsafe_allow_html=True)
    for item in retrieved:
        st.markdown(
            f"""
            <div class="source-box">
                <strong>{item['title']}</strong><br>
                {item['text']}<br>
                <em>Similarity score: {item['score']:.3f}</em>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="card">
        <div class="card-title">How to use this page</div>
        <div class="card-text">
            Ask a plain-English question about solar performance, design comparison,
            financial meaning, environmental impact, or dashboard concepts.
            This page retrieves the most relevant dashboard knowledge and returns a simple answer.
        </div>
    </div>
    """, unsafe_allow_html=True)