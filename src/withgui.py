import re
import nltk
import tkinter as tk
from tkinter import messagebox
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download("vader_lexicon", quiet=True)

va = SentimentIntensityAnalyzer()

NEG = [
    "not", "no", "never", "none", "nobody", "nothing", "nowhere",
    "neither", "nor", "cannot", "can't", "ain't", "isn't", "aren't",
    "wasn't", "weren't", "won't", "wouldn't", "shouldn't", "couldn't",
    "don't", "doesn't", "didn't", "without", "lacking", "against",
    "hardly", "scarcely", "barely", "seldom",
]

INT = {
    "extremely": 2.0, "incredibly": 1.9, "absolutely": 1.8, "astonishingly": 2.1,
    "exceptionally": 1.95, "unbelievably": 2.2, "very": 1.5, "really": 1.3,
    "totally": 1.6, "completely": 1.7, "remarkably": 1.7, "particularly": 1.4,
    "especially": 1.4, "slightly": 0.6, "somewhat": 0.7, "moderately": 0.75,
    "a bit": 0.8,
}


def analyze(txt):
    vs = va.polarity_scores(txt)["compound"]
    wds = txt.split()
    sc = 0.0
    cnt = 0
    sw = []

    for i, w in enumerate(wds):
        cw = re.sub(r"[^\w\s-]", "", w.lower().strip())
        ws = va.polarity_scores(cw)["compound"]

        if ws != 0:
            os = ws
            m = 1.0

            # Intensifier check (2 words back)
            for j in range(max(0, i - 2), i):
                if wds[j].lower() in INT:
                    m = INT[wds[j].lower()]

            ws *= m

            # Negation check (3 words back)
            ng = False
            for j in range(max(0, i - 3), i):
                if wds[j].lower() in NEG:
                    ng = True

            if ng:
                ws *= -1.0

            sc += ws
            cnt += 1
            sw.append(f"{w}({os}->{ws})")

    if cnt > 0:
        avg = sc / cnt
        fp = (vs * 0.5) + (avg * 0.5)
    else:
        fp = vs

    if fp >= 0.05:
        lbl = "Positive"
    elif fp <= -0.05:
        lbl = "Negative"
    else:
        lbl = "Neutral"

    return lbl, fp, sw


def run_analysis():
    text = input_box.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "Please enter some text!")
        return

    sentiment, polarity, words = analyze(text)

    result_label.config(text=f"Sentiment: {sentiment}")
    polarity_label.config(text=f"Polarity: {polarity}")

    keyword_box.delete("1.0", tk.END)
    if words:
        for w in words:
            keyword_box.insert(tk.END, "• " + w + "\n")


# Main Tkinter window
root = tk.Tk()
root.title("Sentiment Analysis GUI")
root.geometry("600x500")
root.config(bg="#e8e8e8")

# Input label
tk.Label(root, text="Enter your text:", font=("Arial", 12, "bold"), bg="#e8e8e8").pack(pady=5)

# Multi-line text input
input_box = tk.Text(root, height=5, width=60, font=("Arial", 12))
input_box.pack(pady=5)

# Analyze button
tk.Button(root, text="Analyze Sentiment", font=("Arial", 12, "bold"),
          bg="#4CAF50", fg="white", command=run_analysis).pack(pady=10)

# Result labels
result_label = tk.Label(root, text="Sentiment: ", font=("Arial", 14, "bold"), bg="#e8e8e8")
result_label.pack(pady=5)

polarity_label = tk.Label(root, text="Polarity: ", font=("Arial", 14, "bold"), bg="#e8e8e8")
polarity_label.pack(pady=5)

# Keywords box
tk.Label(root, text="Key Words:", font=("Arial", 12, "bold"), bg="#e8e8e8").pack(pady=5)
keyword_box = tk.Text(root, height=8, width=60, font=("Arial", 11))
keyword_box.pack()

# Run GUI loop
root.mainloop()