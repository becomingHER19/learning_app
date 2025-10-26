# utils/compare.py
import difflib, html, re

def tokenize_words(text):
    return re.findall(r"\b[\w']+\b", text)

def compare_texts(expected, spoken):
    # overall similarity
    matcher = difflib.SequenceMatcher(None, expected.lower(), spoken.lower())
    score = matcher.ratio()
    # diffs list (ndiff)
    diffs = list(difflib.ndiff(expected.split(), spoken.split()))
    return {"score": score, "diffs": diffs}

def highlight_comparison(expected, spoken):
    exp_words = tokenize_words(expected)
    sp_words = tokenize_words(spoken)
    sm = difflib.SequenceMatcher(None, exp_words, sp_words)
    parts = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for w in exp_words[i1:i2]:
                parts.append(f"<span class='highlight-correct'>{html.escape(w)}</span>")
        elif tag == "delete":
            for w in exp_words[i1:i2]:
                parts.append(f"<span class='highlight-missed'>{html.escape(w)}</span>")
        elif tag == "replace":
            for w in exp_words[i1:i2]:
                parts.append(f"<span class='highlight-wrong'>{html.escape(w)}</span>")
        elif tag == "insert":
            for w in sp_words[j1:j2]:
                parts.append(f"<span style='color:#666;margin:3px'>+{html.escape(w)}</span>")
    return " ".join(parts)
