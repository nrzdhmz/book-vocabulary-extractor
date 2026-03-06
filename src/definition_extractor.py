import pandas as pd
from nltk.corpus import wordnet as wn


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

    synsets = wn.synsets(lemma, pos=wn_pos)

    if not synsets:
        return None

    return synsets[0].definition()


def add_definitions(vocab_df: pd.DataFrame) -> pd.DataFrame:
    result_df = vocab_df.copy()

    result_df["definition"] = result_df.apply(
        lambda row: get_wordnet_definition(row["lemma"], row["pos"]),
        axis=1
    )

    return result_df