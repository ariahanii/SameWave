"""
SameWave - Streamlit app, main page.

Run with:
    streamlit run Home.py
"""

import streamlit as st

from config import AXIS_NAMES, QUESTIONS
from local_scorer import score_user_answers
from matcher import similarity_score, vector_from_scores
from sample_answers import SAMPLE_USERS

st.set_page_config(page_title="SameWave", page_icon="🧭", layout="centered")

st.title("🧭 SameWave")
st.write(
    "Answer 3 weird questions. You get matched based on **how** you answer "
    "them, not the literal content - practicality, focus, elaboration, and "
    "assertiveness, extracted from your phrasing."
)


@st.cache_data(show_spinner="Scoring sample users...")
def get_scored_sample_users():
    """
    Scores every user in sample_answers.py once and caches the result,
    so re-running the matcher on every button click doesn't re-embed
    the same 6 users' answers each time.
    """
    scored = []
    for u in SAMPLE_USERS:
        scores = score_user_answers(u["answers"])
        scored.append({**u, "scores": scores, "vector": vector_from_scores(scores)})
    return scored


sample_users = get_scored_sample_users()

st.subheader("Your answers")
answers = {}
for q in QUESTIONS:
    answers[q["id"]] = st.text_area(q["text"], key=q["id"], height=90)

if st.button("Find my matches", type="primary"):
    if not all(a.strip() for a in answers.values()):
        st.warning("Answer all 3 questions first.")
    else:
        with st.spinner("Scoring your answers..."):
            my_scores = score_user_answers(answers)
            my_vector = vector_from_scores(my_scores)

        st.subheader("Your scores")
        cols = st.columns(len(AXIS_NAMES))
        for col, axis in zip(cols, AXIS_NAMES):
            col.metric(axis, f"{my_scores[axis]:.1f}")

        st.subheader("Your top matches")
        ranked = sorted(
            (
                (u["name"], u["persona"], similarity_score(my_vector, u["vector"]))
                for u in sample_users
            ),
            key=lambda x: x[2],
            reverse=True,
        )
        for name, persona, score in ranked[:3]:
            st.write(f"**{name}**  ·  _{persona}_  ·  compatibility: **{score}%**")
            st.progress(min(max(score / 100, 0.0), 1.0))

st.divider()
st.caption("See the **All Users** page (sidebar) to browse the synthetic personas and their answers.")
