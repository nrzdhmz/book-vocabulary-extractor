import pandas as pd
import nltk
from nltk.corpus import wordnet as wn
import numpy as np


POS_MAP = {
    "NOUN": wn.NOUN,
    "VERB": wn.VERB,
    "ADJ": wn.ADJ,
    "ADV": wn.ADV,
}

def get_wordnet_definition(lemma: str, pos: str) -> str | None:
    wn_pos = POS_MAP.get(pos)

    if wn_pos is None:
        return None

    try:
        synsets = wn.synsets(lemma, pos=wn_pos)
    except LookupError:
        # WordNet data missing; attempt a quiet download once.
        try:
            nltk.download("wordnet", quiet=True)
            synsets = wn.synsets(lemma, pos=wn_pos)
        except Exception:
            return None

    if not synsets:
        return None

    return synsets[0].definition()


def add_definitions(vocab_df: pd.DataFrame) -> pd.DataFrame:
    result_df = vocab_df.copy()

    result_df["definition"] = result_df.apply(
        lambda row: get_wordnet_definition(row["lemma"], row["pos"]),
        axis=1
    )

    # Ensure downstream JSON/CSV don't emit NaN/inf; use None for missing.
    result_df = result_df.replace([np.inf, -np.inf], np.nan)
    result_df = result_df.where(pd.notna(result_df), None)
    result_df["definition"] = result_df["definition"].fillna("")

    return result_df
