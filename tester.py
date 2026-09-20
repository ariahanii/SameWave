"""
Axis - end-to-end demo using fully LOCAL scoring (no API key, no
network calls needed after the one-time model download).

Usage:
    pip install -r requirements.txt
    python main.py
"""

from config import AXIS_NAMES
from local_scorer import score_user_answers
from matcher import find_top_matches, vector_from_scores
from sample_answers import SAMPLE_USERS


def main():
    users = [dict(u) for u in SAMPLE_USERS]

    print(f"Scoring {len(users)} users locally across axes: {AXIS_NAMES}\n")
    for user in users:
        scores = score_user_answers(user["answers"])
        user["scores"] = scores
        user["vector"] = vector_from_scores(scores)
        print(f"{user['name']}  ({user['persona']})")
        print(f"  scores: {scores}\n")

    print("Finding top matches...\n")
    matches = find_top_matches(users, top_k=2)

    for name, top in matches.items():
        print(f"{name} -> {top}")


if __name__ == "__main__":
    main()
