import streamlit as st
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download("vader_lexicon", quiet=True)

SENT_ANALYZER = SentimentIntensityAnalyzer()

NEGATIONS = [
    "not",
    "no",
    "never",
    "none",
    "nobody",
    "nothing",
    "nowhere",
    "neither",
    "nor",
    "cannot",
    "can't",
    "ain't",
    "isn't",
    "aren't",
    "wasn't",
    "weren't",
    "won't",
    "wouldn't",
    "shouldn't",
    "couldn't",
    "don't",
    "doesn't",
    "didn't",
    "without",
    "lacking",
    "against",
    "hardly",
    "scarcely",
    "barely",
    "seldom",
]

INTENSIFIERS = {
    "extremely": 2.0,
    "incredibly": 1.9,
    "absolutely": 1.8,
    "astonishingly": 2.1,
    "exceptionally": 1.95,
    "unbelievably": 2.2,
    "very": 1.5,
    "really": 1.3,
    "totally": 1.6,
    "completely": 1.7,
    "remarkably": 1.7,
    "particularly": 1.4,
    "especially": 1.4,
    "slightly": 0.6,
    "somewhat": 0.7,
    "moderately": 0.75,
    "a bit": 0.8,
}


def analyze(text):
    global_sent_score = SENT_ANALYZER.polarity_scores(text)["compound"]
    words = text.split()
    score_sum = 0.0
    count = 0
    highlights = []

    for i, word in enumerate(words):
        cleaned = re.sub(r"[^\w\s-]", "", word.lower().strip())
        word_base_score = SENT_ANALYZER.polarity_scores(cleaned)["compound"]
        if word_base_score == 0:
            continue

        adjusted = word_base_score
        modifier = 1.0

        for j in range(max(0, i - 2), i):
            prev = words[j].lower()
            if prev in INTENSIFIERS:
                modifier = INTENSIFIERS[prev]
                break

        adjusted *= modifier

        negated = any(words[j].lower() in NEGATIONS for j in range(max(0, i - 3), i))
        if negated:
            adjusted *= -1.0

        score_sum += adjusted
        count += 1
        highlights.append(f"{word}({word_base_score}->{adjusted})")

    if count > 0:
        avg = score_sum / count
        final_score = (global_sent_score * 0.5) + (avg * 0.5)
    else:
        final_score = global_sent_score

    if final_score >= 0.05:
        label = "Positive"
    elif final_score <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"

    return label, final_score, highlights


def _main():
    print("=" * 50)
    print(" Sentiment Analyzer")
    print(" type 'exit' to quit")
    print("=" * 50)
    while True:
        inp = input("-> ").strip()
        if inp.lower() in {"exit", "quit", "q"}:
            print("Goodbye!")
            break
        if not inp:
            continue
        label, score, highlights = analyze(inp)
        print("\n--- Result ---")
        print(f"Sentiment: {label}")
        print(f"Polarity: {score}")
        if highlights:
            print("\nKey Words:")
            for item in highlights:
                print(f"  • {item}")
        print("*************-\n")
if __name__ == "__main__":
    _main()