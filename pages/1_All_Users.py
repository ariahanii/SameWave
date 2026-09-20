"""
SameWave - Streamlit app, "All Users" page.

Streamlit auto-discovers this as a page because it lives under pages/.
The "1_" prefix controls its position in the sidebar; the rest of the
filename (underscores -> spaces) becomes the page title.
"""

import streamlit as st

from config import QUESTIONS
from local_scorer import score_user_answers
from matcher import vector_from_scores
from sample_answers import SAMPLE_USERS

st.set_page_config(page_title="SameWave - All Users", page_icon="👥", layout="centered")

st.title("👥 Artificial users")
st.write("Synthetic personas used to test and demo the matching engine.")


@st.cache_data(show_spinner="Scoring sample users...")
def get_scored_sample_users():
    scored = []
    for u in SAMPLE_USERS:
        scores = score_user_answers(u["answers"])
        scored.append({**u, "scores": scores, "vector": vector_from_scores(scores)})
    return scored


sample_users = get_scored_sample_users()

for u in sample_users:
    with st.expander(f"**{u['name']}**  ·  {u['persona']}"):
        for q in QUESTIONS:
            st.markdown(f"**{q['text']}**")
            st.write(u["answers"][q["id"]])
            st.write("")

        st.markdown("**Scores**")
        score_cols = st.columns(len(u["scores"]))
        for col, (axis, value) in zip(score_cols, u["scores"].items()):
            col.metric(axis, f"{value:.1f}")
