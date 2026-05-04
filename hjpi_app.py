# ============================================================
# HJPI Scoring Tool V3 — Streamlit Web Interface
# Human Judgment Preservation Index | The Responsibility Lens
# By Aderayo Adelanwa | Ethentra Limited
# ============================================================

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import csv
from datetime import datetime
from io import BytesIO, StringIO

st.set_page_config(
    page_title="HJPI Tool | The Responsibility Lens",
    page_icon="🔍",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500&display=swap');

.brand-header {
    background: #1A1A1A;
    color: #FAF7F2;
    padding: 2rem 2.5rem;
    border-radius: 4px;
    margin-bottom: 2rem;
}
.brand-header h1 { color: #FAF7F2; font-size: 1.8rem; margin: 0 0 0.3rem 0; }
.brand-header p { color: #B85C2C; font-size: 0.9rem; margin: 0; letter-spacing: 0.08em; text-transform: uppercase; }
.section-label { font-size: 0.75rem; letter-spacing: 0.12em; text-transform: uppercase; color: #B85C2C; font-weight: 500; margin-bottom: 0.3rem; }
.verdict-box { padding: 1.5rem 2rem; border-radius: 4px; margin: 1.5rem 0; border-left: 5px solid; }
.verdict-pass { background: #F0F7F0; border-color: #2D7A2D; color: #1A3D1A; }
.verdict-conditional { background: #FFF8EC; border-color: #C97D00; color: #3D2800; }
.verdict-redesign { background: #FFF3EC; border-color: #B85C2C; color: #3D1500; }
.verdict-fail { background: #FFF0F0; border-color: #C0392B; color: #3D0000; }
.score-summary { display: flex; gap: 1.5rem; margin: 1.5rem 0; }
.score-card { background: #1A1A1A; color: #FAF7F2; padding: 1rem 1.5rem; border-radius: 4px; text-align: center; flex: 1; }
.score-card .number { font-size: 2rem; color: #B85C2C; }
.score-card .label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; opacity: 0.7; }
.footer { text-align: center; color: #7A6A5E; font-size: 0.8rem; padding: 2rem 0 1rem 0; border-top: 1px solid #DDD0C4; margin-top: 3rem; }
.stButton > button { background: #B85C2C !important; color: #FAF7F2 !important; border: none !important; border-radius: 4px !important; font-weight: 500 !important; width: 100%; }
.stButton > button:hover { background: #9A4820 !important; }
</style>
""", unsafe_allow_html=True)


def get_verdict(percentage):
    if percentage >= 85:
        return "PASS — FLOURISHING-ORIENTED", "PASS"
    elif percentage >= 70:
        return "CONDITIONAL PASS", "CONDITIONAL"
    elif percentage >= 50:
        return "REDESIGN REQUIRED", "REDESIGN"
    else:
        return "FAIL — REJECT DEPLOYMENT", "FAIL"


def get_verdict_message(level):
    messages = {
        "PASS": "This system preserves and develops human judgment. Users become better decision-makers over time. Cleared for deployment with standard monitoring.",
        "CONDITIONAL": "This system broadly preserves human judgment but has gaps. Address flagged dimensions before or after deployment. Schedule a review in 90 days.",
        "REDESIGN": "Significant human judgment preservation failures found. Do not deploy until red-flagged dimensions are resolved. Return to design team with specific recommendations.",
        "FAIL": "Serious risk to human judgment and autonomy detected. Reject deployment. Return to design phase. Request an independent Responsibility Lens audit."
    }
    return messages[level]


def create_radar_chart(scores, system_name, total, percentage, verdict):
    dimensions = ['Reasoning\nTransparency', 'User Override\nCapability', 'Skill\nDevelopment', 'No Decision\nOutsourcing', 'Transparency\nat Use']
    num_dims = len(dimensions)
    angles = np.linspace(0, 2 * np.pi, num_dims, endpoint=False).tolist()
    scores_plot = scores + [scores[0]]
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#FAF7F2')
    ax.set_facecolor('#FAF7F2')
    ax.fill(angles, scores_plot, color='#B85C2C', alpha=0.25)
    ax.plot(angles, scores_plot, color='#B85C2C', linewidth=2.5)
    for angle, score in zip(angles[:-1], scores):
        ax.plot(angle, score, 'o', color='#B85C2C', markersize=7, zorder=5)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dimensions, size=10, fontweight='bold', color='#1A1A1A')
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['1', '2', '3', '4', '5'], size=8, color='#7A6A5E')
    ax.grid(color='#DDD0C4', linestyle='--', linewidth=0.6)
    ax.spines['polar'].set_color('#DDD0C4')
    plt.title(f"HJPI — {system_name}\n{total}/25  ({percentage:.1f}%)  |  {verdict}", size=11, fontweight='bold', color='#1A1A1A', pad=20)
    fig.text(0.5, 0.01, 'The Responsibility Lens  |  Ethentra Limited  |  contact@aderayoadelanwa.com', ha='center', size=8, color='#7A6A5E')
    return fig


def csv_to_download(meta, scores, total, percentage, verdict):
    row = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "System Name": meta["system_name"], "Evaluator": meta["evaluator"],
        "Organisation": meta["organisation"], "Context": meta["context"],
        "Q1 Reasoning": scores[0], "Q2 Override": scores[1], "Q3 Skill Dev": scores[2],
        "Q4 No Outsourcing": scores[3], "Q5 Transparency": scores[4],
        "Total": total, "Percentage": round(percentage, 1), "Verdict": verdict
    }
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=row.keys())
    writer.writeheader()
    writer.writerow(row)
    return output.getvalue().encode("utf-8")


if "step" not in st.session_state:
    st.session_state.step = "intro"

st.markdown("""
<div class="brand-header">
    <h1>The Responsibility Lens</h1>
    <p>Human Judgment Preservation Index · Ethentra Limited</p>
</div>
""", unsafe_allow_html=True)


if st.session_state.step == "intro":
    st.markdown("### What is the HJPI Tool?")
    st.markdown("""
    The **Human Judgment Preservation Index (HJPI)** evaluates whether an AI system
    supports or erodes human judgment over time.

    It scores any AI system across **five dimensions** and returns a
    **Flourishing Verdict** — telling you whether the system is safe to deploy,
    needs redesign, or should be rejected.
    """)
    st.markdown("---")
    st.markdown('<div class="section-label">The Five Dimensions</div>', unsafe_allow_html=True)
    for icon, title, desc in [
        ("🔍", "Reasoning Transparency", "Does the AI show its reasoning?"),
        ("🎛️", "User Override Capability", "Can users override — and do they?"),
        ("📈", "Skill Development", "Does use build user skills over time?"),
        ("🧠", "No Decision Outsourcing", "Are users genuinely reviewing outputs?"),
        ("💡", "Transparency at Use", "Do users understand what the system does?"),
    ]:
        st.markdown(f"**{icon} {title}** — {desc}")
    st.markdown("---")
    if st.button("Begin Evaluation →"):
        st.session_state.step = "details"
        st.rerun()


elif st.session_state.step == "details":
    st.markdown("### Step 1 of 2 — System Details")
    st.markdown('<div class="section-label">Tell us about the AI system you are evaluating</div>', unsafe_allow_html=True)
    with st.form("details_form"):
        system_name = st.text_input("AI System / Product Name *")
        evaluator = st.text_input("Your Name *")
        organisation = st.text_input("Organisation *")
        context = st.text_area("Your role and reason for this evaluation", height=80)
        submitted = st.form_submit_button("Continue to Scoring →")
        if submitted:
            if not system_name or not evaluator or not organisation:
                st.error("Please complete all required fields (*).")
            else:
                st.session_state.meta = {"system_name": system_name, "evaluator": evaluator, "organisation": organisation, "context": context}
                st.session_state.step = "scoring"
                st.rerun()


elif st.session_state.step == "scoring":
    st.markdown("### Step 2 of 2 — Dimension Scoring")
    st.markdown(f'<div class="section-label">Evaluating: {st.session_state.meta["system_name"]}</div>', unsafe_allow_html=True)
    st.markdown("Rate each dimension from **1 (Very Poor)** to **5 (Excellent)**.")
    st.markdown("---")
    questions = [
        ("🔍 Reasoning Transparency", "Does the AI system present its reasoning so users can evaluate the logic themselves?"),
        ("🎛️ User Override Capability", "Do users retain the ability to override the system — and do they actually use it?"),
        ("📈 Skill Development", "Is there evidence that regular use builds user skills rather than causing dependency?"),
        ("🧠 No Decision Outsourcing", "Are users genuinely reviewing outputs rather than simply approving them?"),
        ("💡 Transparency at Use", "Is the system behaviour transparent at point of use — users understand what it does?"),
    ]
    score_options = {"1 — Very Poor": 1, "2 — Poor": 2, "3 — Moderate": 3, "4 — Good": 4, "5 — Excellent": 5}
    with st.form("scoring_form"):
        scores = []
        for i, (dim, question) in enumerate(questions):
            st.markdown(f"**Q{i+1}. {dim}**")
            st.caption(question)
            choice = st.radio(f"score_{i}", options=list(score_options.keys()), index=2, horizontal=True, label_visibility="collapsed", key=f"q{i}")
            scores.append(score_options[choice])
            if i < len(questions) - 1:
                st.markdown("---")
        submitted = st.form_submit_button("Generate Results →")
        if submitted:
            st.session_state.scores = scores
            st.session_state.step = "results"
            st.rerun()


elif st.session_state.step == "results":
    scores = st.session_state.scores
    meta = st.session_state.meta
    total = sum(scores)
    percentage = (total / 25) * 100
    verdict, level = get_verdict(percentage)
    dimensions = ["Reasoning Transparency", "User Override Capability", "Skill Development", "No Decision Outsourcing", "Transparency at Use"]
    verdict_class = {"PASS": "verdict-pass", "CONDITIONAL": "verdict-conditional", "REDESIGN": "verdict-redesign", "FAIL": "verdict-fail"}[level]

    st.markdown("### Evaluation Results")
    st.markdown(f'<div class="section-label">{meta["system_name"]} · {meta["organisation"]}</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="score-summary">
        <div class="score-card"><div class="number">{total}/25</div><div class="label">Total Score</div></div>
        <div class="score-card"><div class="number">{percentage:.1f}%</div><div class="label">HJPI Score</div></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="verdict-box {verdict_class}">
        <strong>FLOURISHING VERDICT</strong><br>
        <span style="font-size:1.1rem; font-weight:600">{verdict}</span><br><br>
        {get_verdict_message(level)}
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Dimension Breakdown**")
    for dim, score in zip(dimensions, scores):
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.markdown(f"<small>{dim}</small>", unsafe_allow_html=True)
        col2.markdown(f"<small style='color:#B85C2C'>{'█' * score}{'░' * (5 - score)}</small>", unsafe_allow_html=True)
        col3.markdown(f"<small><b>{score}/5</b></small>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**HJPI Radar Chart**")
    fig = create_radar_chart(scores, meta["system_name"], total, percentage, verdict)
    st.pyplot(fig)
    st.markdown("---")
    st.markdown("**Download Results**")
    col1, col2 = st.columns(2)
    csv_data = csv_to_download(meta, scores, total, percentage, verdict)
    col1.download_button(label="⬇ Download CSV", data=csv_data, file_name=f"hjpi_{meta['system_name'].replace(' ', '_')}.csv", mime="text/csv")
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches='tight', facecolor='#FAF7F2')
    buf.seek(0)
    col2.download_button(label="⬇ Download Chart", data=buf, file_name=f"hjpi_{meta['system_name'].replace(' ', '_')}.png", mime="image/png")
    st.markdown("---")
    if st.button("← Run Another Evaluation"):
        for key in ["step", "meta", "scores"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()


st.markdown("""
<div class="footer">
    The Responsibility Lens &nbsp;|&nbsp; Ethentra Limited &nbsp;|&nbsp;
    contact@aderayoadelanwa.com &nbsp;|&nbsp; store.aderayoadelanwa.com
</div>
""", unsafe_allow_html=True)