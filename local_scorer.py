"""
SameWave - fully local scoring using sentence embeddings. No API calls, no
LLM, no per-request cost. See README.md "How local scoring works" for
the full explanation - short version below.

1. Each axis has a few "low" example sentences and a few "high" example
   sentences (config.py). We embed each group and average it, giving a
   low_anchor vector and a high_anchor vector.
2. axis_direction = high_anchor - low_anchor. This vector, in embedding
   space, points from "low" toward "high" for that axis.
3. To score a new answer: embed it, then compute how far along
   axis_direction it falls, using vector projection. Clip to [0,1] and
   rescale to a 1-10 score.
"""

import numpy as np
from sentence_transformers import SentenceTransformer

from config import AXES, AXIS_NAMES

# Small, fast model (~80MB). Downloaded once from Hugging Face on first
# run, then cached locally and used fully offline after that.
_MODEL_NAME = "all-MiniLM-L6-v2"
_model = None
_AXIS_DIRECTIONS = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(_MODEL_NAME)
    return _model


def _embed(texts: list) -> np.ndarray:
    model = _get_model()
    return np.array(model.encode(texts, normalize_embeddings=True))


def _build_axis_directions() -> dict:
    """
    Returns {axis_name: (low_anchor_vec, axis_direction_vec)} where
    axis_direction_vec = high_anchor_vec - low_anchor_vec.
    """
    directions = {}
    for axis_name, spec in AXES.items():
        low_vecs = _embed(spec["low_examples"])
        high_vecs = _embed(spec["high_examples"])

        low_anchor = low_vecs.mean(axis=0)
        high_anchor = high_vecs.mean(axis=0)

        directions[axis_name] = (low_anchor, high_anchor - low_anchor)
    return directions


def _get_axis_directions() -> dict:
    global _AXIS_DIRECTIONS
    if _AXIS_DIRECTIONS is None:
        _AXIS_DIRECTIONS = _build_axis_directions()
    return _AXIS_DIRECTIONS


def score_answer(answer_text: str) -> dict:
    """
    Embeds one answer and projects it onto each axis direction.
    Returns {axis_name: score in [1, 10]}.
    """
    directions = _get_axis_directions()
    answer_vec = _embed([answer_text])[0]

    scores = {}
    for axis_name, (low_anchor, axis_dir) in directions.items():
        # Vector projection: how far along axis_dir does
        # (answer_vec - low_anchor) fall, as a fraction of axis_dir's length?
        t = float(np.dot(answer_vec - low_anchor, axis_dir) / np.dot(axis_dir, axis_dir))
        t_clipped = max(0.0, min(1.0, t))
        scores[axis_name] = round(1 + 9 * t_clipped, 2)

    return scores


def score_user_answers(answers: dict) -> dict:
    """
    answers: {question_id: answer_text}
    Returns: {axis_name: averaged_score_across_questions}
    """
    per_question_scores = [score_answer(text) for text in answers.values()]
    averaged = {}
    for axis in AXIS_NAMES:
        averaged[axis] = round(
            sum(s[axis] for s in per_question_scores) / len(per_question_scores), 2
        )
    return averaged
