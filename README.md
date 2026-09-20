# SameWave

A matching-engine prototype for a niche dating app: instead of a
questionnaire, users answer 3 weird, open-ended questions. Answers are
scored against fixed "vibe" axes and turned into a numeric vector per
user. Matches are computed via vector similarity.

Scoring is **fully local** - no API key, no LLM calls. It uses sentence embeddings and a technique called axis projection.

## How local scoring works, in detail

### 1. What an embedding is

A sentence embedding model (`all-MiniLM-L6-v2` from the
`sentence-transformers` library) reads a sentence and outputs a vector -
a list of 384 numbers. The model is trained so that sentences with
similar *meaning* end up as vectors that are close together / point in
similar directions, regardless of exact wording. "I love dogs" and "Dogs
are my favorite animal" get very different words but very similar
vectors.

"Close together" is normally measured with **cosine similarity** - the
cosine of the angle between two vectors. 1.0 means pointing the exact
same direction (identical meaning), 0 means unrelated, -1 means opposite.

### 2. Defining an axis as a direction in that space

You can't just ask "is this sentence practical?" - the model doesn't
have a built-in practicality dial. But you CAN define what "practical"
means by example, and let the geometry do the work:

- Write 3 sentences that are clearly LOW on the axis (whimsical, ignores
  logistics) and 3 that are clearly HIGH (grounded, logistical). These
  live in `config.py` as `low_examples` / `high_examples`.
- Embed each group, and average the vectors within each group. Averaging
  cancels out noise specific to any one sentence and keeps what's common
  to the group - giving you a `low_anchor` vector and a `high_anchor`
  vector.
- The vector from `low_anchor` to `high_anchor` - i.e.
  `axis_direction = high_anchor - low_anchor` - is literally the
  "practicality direction" in the embedding space. This is the same
  "concept direction" idea used in embedding-bias research.

### 3. Scoring a new answer: vector projection

To score a new answer, embed it (call this vector `v`), then figure out
how far along the low->high line it falls. This is a standard operation
called **vector projection**:

```
t = dot(v - low_anchor, axis_direction) / dot(axis_direction, axis_direction)
```

Intuition: `v - low_anchor` is the vector from the low anchor to your
answer. The `dot(...)` in the numerator measures how much of that vector
points in the *same direction* as the axis. Dividing by
`dot(axis_direction, axis_direction)` (the axis's own squared length)
rescales this into a fraction: `t=0` means "right at the low anchor",
`t=1` means "right at the high anchor". `t` can go slightly below 0 or
above 1 if the answer is more extreme than your examples - the code
clips it to `[0, 1]` and rescales to a 1-10 score.

**Toy 2D example**, to make it concrete before trusting 384 dimensions:
imagine `low_anchor = (0, 0)`, `high_anchor = (4, 0)`, so
`axis_direction = (4, 0)`. An answer embedding at `(3, 1)`:

```
t = dot((3,1) - (0,0), (4,0)) / dot((4,0), (4,0))
  = dot((3,1), (4,0)) / 16
  = (3*4 + 1*0) / 16
  = 12 / 16 = 0.75
```

Score = `1 + 9 * 0.75 = 7.75`. The `y`-component (1) didn't matter to the
score at all - projection only cares about position ALONG the axis, and
ignores everything perpendicular to it. That's the whole trick: 384
dimensions capture all sorts of meaning, but projection isolates just
the one direction you defined.

## Project structure

- `config.py` - the 3 questions, and the 4 axes with their low/high
  anchor example sentences.
- `local_scorer.py` - builds axis directions from the anchor examples,
  embeds answers, projects them, returns 1-10 scores. This is the
  default scorer, fully offline.
- `sample_answers.py` - handwritten example answers for 6 personas, so
  you can test the pipeline with zero setup beyond installing packages.
- `matcher.py` - Euclidean distance between user vectors -> 0-100
  compatibility score. Unaffected by whether scores came from the local
  scorer or elsewhere.
- `main.py` - runs the full pipeline end to end using the local scorer
  and sample answers.

## Setup & run

```bash
cd SameWave
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

First run downloads the embedding model (~80MB) from Hugging Face once;
after that it's cached locally and runs fully offline, no internet
needed.

## Streamlit interface

Two pages:

- **Home.py** - enter your own answers to the 3 questions, see your axis
  scores, and see your top matches against the synthetic sample users.
- **pages/1_All_Users.py** - browse every synthetic persona from
  `sample_answers.py`: their name, their answers to each question, and
  their computed axis scores. Streamlit's naming convention
  (`pages/<order>_<Title>.py`) is what makes this show up as a second
  page in the sidebar automatically - no routing code needed.

Run it with:

```bash
streamlit run Home.py
```

This opens in your browser at `http://localhost:8501`. Both pages use
`@st.cache_data` around the sample-user scoring so the 6 sample users
are only embedded once per session, not re-scored on every click.



If scores look off, the fix is almost always **sharper or more numerous
anchor examples** in `config.py`, not a code change - the anchors define
the axis, so vague or overlapping examples give a vague, noisy axis.

## Next steps

1. Tune anchor examples based on the sanity check above.
2. Decide similar-vs-complementary matching per axis in `matcher.py`
   (currently every axis is scored as "closer = more compatible" - you
   may find e.g. `assertiveness` works better as complementary).