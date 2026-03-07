from pathlib import Path

import pandas as pd

from src.vocab_builder import build_vocabulary
from src.vocab_ranker import rank_vocabulary
from src.vocab_saver import save_vocab_by_difficulty


def test_build_vocabulary_filters_and_counts():
    tokens = [
        {"lemma": "apple", "pos": "NOUN", "is_stop": False, "ent_type": "", "is_title": False},
        {"lemma": "apple", "pos": "NOUN", "is_stop": False, "ent_type": "", "is_title": False},
        {"lemma": "123", "pos": "NOUN", "is_stop": False, "ent_type": "", "is_title": False},  
        {"lemma": "run", "pos": "VERB", "is_stop": False, "ent_type": "", "is_title": False},
        {"lemma": "run", "pos": "VERB", "is_stop": False, "ent_type": "", "is_title": False},
    ]
    df = build_vocabulary(tokens, min_frequency=2)
    assert set(df["lemma"]) == {"apple", "run"}
    assert df.loc[df["lemma"] == "apple", "frequency"].iloc[0] == 2


def test_rank_vocabulary_adds_difficulty():
    vocab_df = pd.DataFrame(
        [
            {"lemma": "apple", "pos": "NOUN", "frequency": 5},
            {"lemma": "xylophone", "pos": "NOUN", "frequency": 2},
        ]
    )
    ranked = rank_vocabulary(vocab_df)
    assert "difficulty" in ranked.columns
    assert set(ranked["difficulty"]) >= {"easy", "hard"}


def test_save_vocab_by_difficulty(tmp_path: Path):
    df = pd.DataFrame(
        [
            {"lemma": "apple", "pos": "NOUN", "frequency": 5, "difficulty": "easy"},
            {"lemma": "run", "pos": "VERB", "frequency": 3, "difficulty": "intermediate"},
            {"lemma": "xylophone", "pos": "NOUN", "frequency": 2, "difficulty": "hard"},
        ]
    )
    saved = save_vocab_by_difficulty(df, out_dir=tmp_path, base_name="test_vocab")
    expected = {"all", "easy", "intermediate", "hard"}
    assert expected.issubset(saved.keys())
    for path in saved.values():
        assert Path(path).exists()
