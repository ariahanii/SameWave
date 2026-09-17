"""
SameWave - configuration: questions and scoring axes.

Each axis now carries, besides a human-readable "low"/"high" description,
a handful of "low_examples" / "high_examples" - short sentences that
exemplify each extreme. These examples are what the LOCAL scorer
(local_scorer.py) embeds to define the axis direction in vector space.
Add more examples per axis if you find scores are noisy - more, more
varied examples make the anchor average more stable.
"""

QUESTIONS = [
    {
        "id": "q1_gravity",
        "text": "You wake up and gravity is sideways for exactly one hour. Walk me through what you do.",
    },
    {
        "id": "q2_spirit_object",
        "text": "Which household object would be your spirit animal? Defend your choice.",
    },
    {
        "id": "q3_goose_goat_invasion",
        "text": "Aliens attack Earth, and they're all shaped like geese and goats. How do you approach fighting them?",
    },
]

AXES = {
    "practicality": {
        "low": "Whimsical, absurd, ignores real-world logistics entirely.",
        "high": "Grounded, logistical, treats the scenario like a real problem to solve.",
        "low_examples": [
            "I wouldn't bother planning, I'd just wing it and see what happens.",
            "Who cares about logistics, this is just fun chaos.",
            "I'd let it happen and enjoy the ride without thinking it through.",
        ],
        "high_examples": [
            "I would immediately assess the risks and make a step-by-step plan to stay safe.",
            "I'd calculate exactly what needs securing and execute a clear plan.",
            "I would treat this like a real problem and organize a practical response.",
            "I consider the rules of physics and try to solve this through scientific thinking and logical consideration.",
        ],
    },
    "focus": {
        "low": "Self-focused - centers on what the person themself would do.",
        "high": "World-focused - centers on how the scenario affects everyone/the bigger picture.",
        "low_examples": [
            "I would focus only on protecting myself and making sure I'm okay.",
            "My first priority is my own safety, not really thinking about anyone else.",
            "I'd worry about what this means for me personally before anything else.",
        ],
        "high_examples": [
            "I would think about how this affects everyone around me and try to help the community.",
            "My first thought would be for the safety of everyone, not just myself.",
            "I'd want to coordinate with others to protect the whole neighborhood.",
        ],
    },
    "elaboration": {
        "low": "One-liner or very short answer, minimal detail.",
        "high": "Builds a full scenario with details, steps, or a narrative arc.",
        "low_examples": [
            "I'd just deal with it.",
            "Not sure, I'd figure it out somehow.",
            "I'd just wait it out and see what happens.",
        ],
        "high_examples": [
            "First I would do this, then that, and finally this other thing, considering every detail and how each step affects the next.",
            "Let me walk through this step by step: first I'd assess the situation, then plan a response, then execute it, and finally review what happened.",
            "I'd build out a full strategy with multiple stages, backup plans, and a clear sequence of actions from start to finish.",
        ],
    },
    "assertiveness": {
        "low": "Avoidant, passive, diplomatic, prefers not to confront the problem head-on.",
        "high": "Decisive, confrontational, takes bold or aggressive action.",
        "low_examples": [
            "I'd try to avoid confrontation and hope it resolves itself.",
            "I would probably just hide and hope nothing bad happens.",
            "I'd try to negotiate peacefully rather than fight."
            "I might just do nothing about it.",
        ],
        "high_examples": [
            "I would take immediate, decisive action and confront the threat head-on.",
            "I'd go on the offensive right away without hesitation.",
            "I would fight back aggressively and take charge of the situation.",
        ],
    },
}

AXIS_NAMES = list(AXES.keys())
