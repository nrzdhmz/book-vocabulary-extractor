from collections import Counter
import pandas as pd


CUSTOM_EXCLUDE = {
    "chapter",
    "contents",
    "preface",
    "introduction",
    "copyright",
    "publisher",
    "index",
}

ALLOWED_POS = {"NOUN", "VERB", "ADJ", "ADV"}
BAD_ENTITY_TYPES = {"PERSON", "GPE", "LOC", "ORG"}


def should_keep_token(token: dict) -> bool:
    lemma = token["lemma"].strip().lower()

    if token["is_stop"]:
        return False

    if token["pos"] not in ALLOWED_POS:
        return False

    if lemma in CUSTOM_EXCLUDE:
        return False

    if token.get("ent_type") in BAD_ENTITY_TYPES:
        return False

    if not lemma.isalpha():
        return False

    if len(lemma) < 3 or len(lemma) > 20:
        return False

    return True


def build_vocabulary(tokens, min_frequency: int = 1) -> pd.DataFrame:
    filtered = []

    for token in tokens:
        if not should_keep_token(token):
            continue

        filtered.append((token["lemma"].lower(), token["pos"]))

    counts = Counter(filtered)

    rows = []
    for (lemma, pos), frequency in counts.items():
        if frequency >= min_frequency:
            rows.append({
                "lemma": lemma,
                "pos": pos,
                "frequency": frequency,
            })

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    df = df.sort_values(
        by=["frequency", "lemma"],
        ascending=[False, True]
    ).reset_index(drop=True)

    return df