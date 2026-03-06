from collections import Counter
import pandas as pd


ALLOWED_POS = {"NOUN", "VERB", "ADJ", "ADV"}


def build_vocabulary(tokens, min_frequency: int = 1) -> pd.DataFrame:
    filtered = []

    for token in tokens:
        if token["is_stop"]:
            continue

        if token["pos"] not in ALLOWED_POS:
            continue

        lemma = token["lemma"].strip().lower()

        if not lemma.isalpha():
            continue

        if len(lemma) < 3:
            continue

        filtered.append((lemma, token["pos"]))

    counts = Counter(filtered)

    rows = []
    for (lemma, pos), frequency in counts.items():
        if frequency >= min_frequency:
            rows.append({
                "lemma": lemma,
                "pos": pos,
                "frequency": frequency
            })

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    df = df.sort_values(
        by=["frequency", "lemma"],
        ascending=[False, True]
    ).reset_index(drop=True)

    return df