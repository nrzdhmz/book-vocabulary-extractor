import math
import pandas as pd
from wordfreq import zipf_frequency


POS_WEIGHTS = {
    "ADJ": 1.15,
    "ADV": 1.10,
    "NOUN": 1.00,
    "VERB": 1.00,
}


def compute_book_frequency_score(frequency: int) -> float:
    return math.log1p(frequency)


def compute_rarity_score(lemma: str) -> float:
    zipf = zipf_frequency(lemma, "en")

    if zipf <= 0:
        return 3.0

    rarity = max(0.5, 8.0 - zipf) # max zipf score is 8 so rarity decreases as frequency increases
    return rarity


def compute_pos_weight(pos: str) -> float:
    return POS_WEIGHTS.get(pos, 1.0)

def classify_difficulty(zipf: float) -> str:
    if pd.isna(zipf):
        return "unknown"
    if zipf >= 5.0:
        return "easy"
    if zipf >= 3.5:
        return "intermediate"
    return "hard"


def rank_vocabulary(vocab_df: pd.DataFrame) -> pd.DataFrame:
    df = vocab_df.copy()

    df["zipf_frequency"] = df["lemma"].apply(lambda x: zipf_frequency(x, "en"))
    df["book_frequency_score"] = df["frequency"].apply(compute_book_frequency_score)
    df["rarity_score"] = df["lemma"].apply(compute_rarity_score)
    df["pos_weight"] = df["pos"].apply(compute_pos_weight)

    df["vocab_score"] = (
        df["book_frequency_score"]
        * df["rarity_score"]
        * df["pos_weight"]
    )

    df["difficulty"] = df["zipf_frequency"].apply(classify_difficulty)

    df = df.sort_values(
        by=["vocab_score", "frequency", "lemma"],
        ascending=[False, False, True]
    ).reset_index(drop=True)

    return df
