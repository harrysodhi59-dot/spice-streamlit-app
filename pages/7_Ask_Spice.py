import json
from pathlib import Path

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
    texts = [
        f"{item.get('page', '')} {item.get('title', '')} {' '.join(item.get('keywords', []))} {item.get('text', '')}"
        for item in kb_items
    ]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(texts)
    return vectorizer, matrix

def retrieve_chunks(query, kb_items, vectorizer, matrix, top_k=3):
    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, matrix).flatten()
    top_idx = scores.argsort()[::-1][:top_k]

    results = []
    for idx in top_idx:
        results.append({
            "page": kb_items[idx].get("page", "General"),
            "title": kb_items[idx].get("title", "Untitled"),
            "text": kb_items[idx].get("text", ""),
            "score": float(scores[idx])
        })
    return results

# =========================================================
# Helpers
# =========================================================
def detect_intent(query: str) -> str:
    q = query.lower()

    if any(x in q for x in ["what is", "define", "meaning", "means"]):
        return "definition"
    if any(x in q for x in ["current", "right now", "this page", "summarize", "what is happening"]):
        return "live_summary"
    if any(x in q for x in ["compare", "difference", "vs", "versus", "better", "worse"]):
        return "comparison"
    if any(x in q for x in ["financial", "payback", "roi", "savings", "cost", "investment"]):
        return "financial"
    if any(x in q for x in ["environment", "carbon", "co2", "emissions", "trees", "cars"]):
        return "environmental"
    if any(x in q for x in ["scale", "scalability", "larger system", "bigger system"]):
        return "scalability"
    return "general"

def get_live_context():
    return {
        "current_page": st.session_state.get("current_page"),
        "home": st.session_state.get("home_context"),
        "solar": st.session_state.get("solar_simulation_context"),
        "validation": st.session_state.get("real_site_validation_context"),
        "financial": st.session_state.get("financial_impact_context"),
        "environmental": st.session_state.get("environmental_impact_context"),
        "scalability": st.session_state.get("scalability_impact_context"),
    }

def build_live_answer(query: str, context: dict):
    q = query.lower()
    current_page = context.get("current_page")

    # Home page
    if context.get("home") and (
        current_page == "Home" or any(x in q for x in ["dashboard", "home page", "what is this dashboard", "who is this for"])
    ):
        home = context["home"]
        return (
            f"This dashboard is about solar investment, performance, and sustainability decision support. "
            f"It is designed for {', '.join(home['primary_stakeholders'][:3])}, and its main business question is: "
            f"{home['strategic_question']}"
        )

    # Solar Simulation
    if context.get("solar") and (
        current_page == "Solar Simulation" or any(x in q for x in ["tilt", "azimuth", "simulation", "reference", "peak month", "scenario range"])
    ):
        solar = context["solar"]

        if "peak month" in q:
            return f"The current peak month on the Solar Simulation page is {solar['best_month']}."

        if "reference" in q or "compare" in q or "comparison" in q:
            return (
                f"The current solar design differs from the reference by {solar['comparison_gap_kwh']:,.0f} kWh, "
                f"which is {solar['comparison_pct']:+.1f}%."
            )

        if "scenario" in q or "range" in q:
            return (
                f"The current solar scenario range is approximately {solar['low_scenario_kwh']:,.0f} kWh low, "
                f"{solar['expected_scenario_kwh']:,.0f} kWh expected, and "
                f"{solar['high_scenario_kwh']:,.0f} kWh high."
            )

        return (
            f"You are on the Solar Simulation page. The current setup is {solar['system_size_kw']} kW, "
            f"{solar['tilt_deg']}° tilt, and {solar['azimuth_deg']}° azimuth. Estimated annual output is "
            f"{solar['annual_output_kwh']:,.0f} kWh, with normalized output of "
            f"{solar['normalized_output_kwh_per_kw']:,.0f} kWh per kW. "
            f"The peak month is {solar['best_month']}."
        )

    # Real Site Validation
    if context.get("validation") and (
        current_page == "Real Site Validation" or any(x in q for x in ["bissell", "visser", "site validation", "real site", "selected years"])
    ):
        val = context["validation"]

        if "leader" in q or "stronger" in q or "better" in q:
            if val["leader_site"]:
                return (
                    f"On the Real Site Validation page, {val['leader_site']} is currently leading, "
                    f"with a production gap of about {val['production_gap_pct']:.1f}%."
                )

        return (
            f"You are on the Real Site Validation page. The selected years are {val['selected_years']}, "
            f"and the selected sites are {val['selected_sites']}. Total energy across the selected sites is "
            f"{val['total_energy_kwh']:,.0f} kWh, with estimated revenue of "
            f"${val['total_revenue_cad']:,.0f}."
        )

    # Financial Impact
    if context.get("financial") and (
        current_page == "Financial Impact" or any(x in q for x in ["payback", "financial", "savings", "project", "investment", "net value"])
    ):
        fin = context["financial"]

        if "payback" in q:
            return f"The current estimated payback period is {fin['payback_years']:.1f} years."

        if "savings" in q:
            return (
                f"The current annual savings estimate is ${fin['annual_savings_cad']:,.0f}, "
                f"and the lifetime savings estimate is ${fin['lifetime_savings_cad']:,.0f}."
            )

        if "net value" in q:
            return f"The current estimated net value after cost recovery is ${fin['net_value_cad']:,.0f}."

        return (
            f"You are on the Financial Impact page. The selected project is {fin['selected_project']}. "
            f"Annual savings are estimated at ${fin['annual_savings_cad']:,.0f}, "
            f"payback is about {fin['payback_years']:.1f} years, and lifetime savings are "
            f"${fin['lifetime_savings_cad']:,.0f}."
        )

    # Environmental Impact
    if context.get("environmental") and (
        current_page == "Environmental Impact" or any(x in q for x in ["carbon", "co2", "environment", "emissions", "trees", "cars"])
    ):
        env = context["environmental"]

        if "trees" in q:
            return f"The current environmental case is equivalent to about {env['trees_equivalent']:,.0f} trees."
        if "cars" in q:
            return f"The current environmental case is roughly equal to removing {env['cars_removed_equivalent']:.1f} cars from the road for one year."
        if "carbon value" in q:
            return (
                f"The current annual carbon value is ${env['annual_carbon_value_cad']:,.0f}, "
                f"and the lifetime carbon value is ${env['lifetime_carbon_value_cad']:,.0f}."
            )

        return (
            f"You are on the Environmental Impact page. The current setup avoids about "
            f"{env['annual_co2_tonnes']:,.2f} tonnes of CO₂ per year, with an annual carbon value of "
            f"${env['annual_carbon_value_cad']:,.0f}. Over {env['lifetime_years']} years, "
            f"the avoided emissions reach {env['lifetime_co2_tonnes']:,.2f} tonnes."
        )

    # Scalability
    if context.get("scalability") and (
        current_page == "Scalability & Business Impact" or any(x in q for x in ["scalability", "system size", "larger", "bigger", "scale"])
    ):
        scale = context["scalability"]

        return (
            f"You are on the Scalability & Business Impact page. The selected system size is "
            f"{scale['selected_system_size_kw']:.0f} kW under the {scale['irradiance_scenario']} irradiance scenario. "
            f"This gives about {scale['annual_production_kwh']:,.0f} kWh annual production, "
            f"${scale['annual_savings_cad']:,.0f} in annual savings, and "
            f"{scale['annual_co2_avoided_tonnes']:.2f} tonnes of CO₂ avoided."
        )

    return None

def build_retrieval_answer(query, retrieved):
    if not retrieved:
        return "I could not find a strong match in the dashboard knowledge base."

    intent = detect_intent(query)
    top_texts = [item["text"] for item in retrieved[:3]]

    if intent == "definition":
        return top_texts[0]

    if intent == "comparison":
        return " ".join(top_texts[:2])

    if intent == "financial":
        return " ".join(top_texts[:2])

    if intent == "environmental":
        return " ".join(top_texts[:2])

    return " ".join(top_texts[:3])

# =========================================================
# Page content
# =========================================================
st.markdown("""
<div class="hero-box">
    <div class="hero-title">Ask <span class="hero-highlight">SPICE</span></div>
    <div class="hero-text">
        This AI assistant explains both the dashboard concepts and the current live dashboard state.
        You can ask what a page means, what is happening right now, or how a result should be interpreted.
    </div>
</div>
""", unsafe_allow_html=True)

kb_items = load_knowledge_base()
vectorizer, matrix = build_vector_store(kb_items)
live_context = get_live_context()

example_questions = [
    "What is normalized output?",
    "What is happening on this page right now?",
    "How is the current solar design performing?",
    "What is the current payback period?",
    "How much CO2 is being avoided?",
    "How does the dashboard support decision making?",
]

st.markdown('<div class="card"><div class="card-title">Suggested Questions</div>', unsafe_allow_html=True)
for q in example_questions:
    st.markdown(f'<span class="question-chip">{q}</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

user_query = st.text_input("Ask a question about the dashboard")

if user_query:
    live_answer = build_live_answer(user_query, live_context)
    retrieved = retrieve_chunks(user_query, kb_items, vectorizer, matrix, top_k=3)

    if live_answer:
        answer = live_answer
        answer_mode = "Live dashboard context"
    else:
        answer = build_retrieval_answer(user_query, retrieved)
        answer_mode = "Knowledge base"

    st.markdown(
        f'<div class="answer-box"><strong>Answer:</strong> {answer}<br><br><em>Response source: {answer_mode}</em></div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card"><div class="card-title">Retrieved Knowledge</div>', unsafe_allow_html=True)
    for item in retrieved:
        st.markdown(
            f"""
            <div class="source-box">
                <strong>{item['page']} • {item['title']}</strong><br>
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
            Ask a plain-English question about the dashboard. The assistant first checks for live page context,
            then falls back to the knowledge base for definitions and general explanations.
        </div>
    </div>
    """, unsafe_allow_html=True)