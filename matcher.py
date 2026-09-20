"""
SameWave compatibility scoring between users, given their axis vectors.

Current logic treats every axis as "similar = compatible" (closer vectors
score higher). That's a deliberate placeholder, not a final design choice -
I may decide some axes (e.g. assertiveness) work better as complementary
rather than similar.
"""

import math

from config import AXIS_NAMES


def vector_from_scores(scores: dict) -> list:
    return [scores[axis] for axis in AXIS_NAMES]


def euclidean_distance(v1: list, v2: list) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


def similarity_score(v1: list, v2: list) -> float:
    """
    0-100 compatibility score based on closeness across all axes.
    Normalized against the maximum possible distance (all axes at
    opposite extremes, 1 vs 10).
    """
    max_distance = math.sqrt(len(AXIS_NAMES) * (9**2))
    distance = euclidean_distance(v1, v2)
    return round((1 - distance / max_distance) * 100, 1)


def find_top_matches(users: list, top_k: int = 3) -> dict:
    """
    users: list of {"name": ..., "vector": [...]}
    Returns {user_name: [(other_user_name, score), ...]} sorted descending
    by compatibility score.
    """
    results = {}
    for user in users:
        scored = []
        for other in users:
            if other["name"] == user["name"]:
                continue
            score = similarity_score(user["vector"], other["vector"])
            scored.append((other["name"], score))
        scored.sort(key=lambda x: x[1], reverse=True)
        results[user["name"]] = scored[:top_k]
    return results
