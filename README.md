# Enhanced Sentiment Analyzer (VADER + Custom Rules)

## Overview

This project is a command‑line sentiment analysis tool that classifies user input as **Positive**, **Negative**, or **Neutral** based on the text they type.

The project started with a simple approach using **TextBlob** for polarity scoring. Over time, the design evolved to use **VADER (Valence Aware Dictionary and sEntiment Reasoner)** from NLTK combined with custom **intensifier** and **negation** handling. The goal of this evolution was to make the analyzer behave more realistically on everyday, real‑world language such as reviews, comments, and short messages.

***

## Motivation

Traditional sentiment tools like TextBlob are easy to start with but can struggle with:

- Short, informal text (e.g., tweets, chats).
- Phrases with **negations** such as “not good” or “never liked it”.
- Phrases with **intensifiers** such as “extremely happy” or “slightly annoyed”.

To handle these better, this project:

1. Began with **TextBlob** to understand basic sentiment analysis.
2. Migrated to **VADER**, which is specifically tuned for social‑media‑style language.
3. Added an extra rule‑based layer for intensifiers and negators to better capture nuanced real‑world expressions.

***

## Evolution: From TextBlob to VADER + Rules

### Phase 1: Baseline with TextBlob

In the initial version:

- The tool used `TextBlob(text).sentiment.polarity` to get a single score between -1 and 1.
- Sentiment labels were assigned using simple thresholds on this polarity.
- This worked reasonably on plain sentences like “I like this product” but failed on more subtle phrases:
  - “I don’t really like this”  
  - “I am extremely happy with this”  

These phrases were not always scored in a way that matched human intuition.

### Phase 2: Switching to VADER

To improve performance on short, informal sentences, the project switched to **VADER** (from NLTK):

- VADER provides a **compound score** in the range \([-1, 1]\) summarizing the sentiment of the whole text.
- It is built from a lexicon tuned for social media and already handles many emojis, slang, and punctuation cues.

This upgrade immediately made the analyzer more robust for comments and short phrases.

### Phase 3: Adding Intensifiers and Negators

To further adapt the tool for real‑world language, a custom rule layer was added on top of VADER:

- **Intensifiers** (e.g., `extremely`, `very`, `slightly`) adjust the strength of a nearby sentiment word using predefined multipliers.
  - Example: “good” vs. “very good” vs. “extremely good”.
- **Negations** (e.g., `not`, `never`, `don’t`) can flip the sentiment of the following emotional word within a small window.
  - Example: “good” vs. “not good” vs. “never really good”.

The final polarity is a **blend** of:

- VADER’s global compound score for the entire text, and
- The average of the adjusted word‑level scores after handling intensifiers and negations.

This combination aims to keep VADER’s robustness while adding better control over local modifiers, making the system more interpretable and closer to human intuition.

***

## Features

- Interactive **command‑line interface**.
- Real‑time sentiment output:
  - Sentiment label: `Positive`, `Negative`, or `Neutral`.
  - Numerical polarity score in the range \([-1, 1]\).
- Explanation of **key words** that influenced the score, including:
  - Original word‑level sentiment.
  - Adjusted sentiment after intensifiers and/or negation.
- Graceful handling of:
  - Empty input.
  - Exit commands (`exit`, `quit`, `q`).

***

## How It Works

1. **Global Sentiment (VADER)**  
   - The input text is passed to VADER’s `polarity_scores`, and the **compound** score is extracted as a baseline.

2. **Tokenization and Cleaning**  
   - The text is split into words.
   - Each word is lowercased and stripped of punctuation before analysis.

3. **Word‑Level Scoring**  
   - For each cleaned word, VADER is used again to obtain a **base score**.
   - If the base score is zero (no apparent sentiment), the word is skipped.

4. **Intensifier Handling**  
   - For each sentiment word, the previous 1–2 words are checked against the `INTENSIFIERS` dictionary.
   - If an intensifier is found, its multiplier (e.g., 2.0 for “extremely”, 0.6 for “slightly”) is applied to the base score.

5. **Negation Handling**  
   - The previous 1–3 words are checked against the `NEGATIONS` list.
   - If a negation is detected, the (possibly intensified) score is multiplied by `-1`.

6. **Score Aggregation**  
   - Adjusted scores for all emotional words are summed and averaged.
   - The final polarity is computed as a 50/50 blend between:
     - VADER’s global compound score, and
     - The custom averaged score from the rule‑based layer.

7. **Label Assignment**  
   - If the final score ≥ 0.05 → `Positive`
   - If the final score ≤ -0.05 → `Negative`
   - Otherwise → `Neutral`

8. **Explanation Output**  
   - For each influential word, an entry like  
     `good (0.44 -> 0.88)`  
     is generated, showing how the custom rules modified VADER’s base sentiment for that word.

***

## Project Structure

- `sentiment_analyzer.py`  
  Main script containing:
  - Imports and setup for NLTK and VADER.
  - Definitions of `NEGATIONS` and `INTENSIFIERS`.
  - The `analyze(text)` function implementing the core logic.
  - The `main()` function providing the CLI loop.

You can optionally separate logic into modules (e.g., `analyzer.py`, `config.py`, `cli.py`) if your course or team prefers a more modular design.

***

## Installation and Setup

1. **Clone or download** the repository.

2. **Create and activate a virtual environment** (recommended):

```bash
python -m venv venv
venv\Scripts\activate    # Windows
# or
source venv/bin/activate # macOS / Linux
```

3. **Install dependencies**:

```bash
pip install nltk
```

4. The script itself downloads the VADER lexicon on first run, so no extra step is required.

***

## Usage

Run the analyzer from the command line:

```bash
python sentiment_analyzer.py
```

You will see a banner and a prompt like:

```text
==================================================
 Sentiment Analyzer
 Type a sentence to analyze, or 'exit' to quit.
==================================================
-> 
```

Type any sentence and press Enter. The program will print:

- The sentiment label.
- The numeric polarity score.
- A list of key words with their base and adjusted scores.

Type `exit`, `quit`, or `q` to end the session.

***

## Example Interactions

**Example 1**

Input:

```text
-> I am very happy with this product!
```

Output (conceptually):

- Sentiment: `Positive`
- Polarity: (a high positive value)
- Key Words:
  - `happy (base -> intensified by "very")`

**Example 2**

Input:

```text
-> I am not really happy with this service.
```

Output (conceptually):

- Sentiment: closer to `Negative` or slightly negative.
- Polarity: a negative or low positive value.
- Key Words:
  - `happy (base positive -> intensified by "really" -> flipped negative by "not")`

These examples illustrate why adding intensifiers and negators on top of VADER produces behavior that more closely matches human expectations compared with the original, simpler TextBlob‑only version.

***

## Limitations and Future Work

- The analyzer currently supports only English text.
- It may misinterpret sarcasm or highly complex sentences.
- Intensifier and negation lists are handcrafted and may miss some domain‑specific expressions.
- Future improvements could include:
  - Expanding the lexicon for specific domains (e.g., product reviews, social media).
  - Adding a simple GUI or web interface.
  - Logging analyzed sentences and scores for evaluation and tuning.

***

## Acknowledgements

- **TextBlob** for providing a simple entry point into sentiment analysis concepts in the early version of the project.
- **NLTK** and **VADER** for the underlying sentiment lexicon and scoring functions.
- Various online tutorials and documentation on sentiment analysis and VADER that inspired the migration from baseline TextBlob to the current, more realistic rule‑enhanced design.