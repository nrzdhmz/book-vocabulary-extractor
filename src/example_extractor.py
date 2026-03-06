import spacy
import pandas as pd


nlp = spacy.load("en_core_web_sm")


def add_example_sentences(vocab_df: pd.DataFrame, text: str) -> pd.DataFrame:
    doc = nlp(text)

    sentence_lookup = {}

    for sent in doc.sents:
        sentence_text = sent.text.strip()

        if not sentence_text:
            continue

        for token in sent:
            if not token.is_alpha:
                continue

            lemma = token.lemma_.lower().strip()

            if lemma not in sentence_lookup:
                sentence_lookup[lemma] = sentence_text

    result_df = vocab_df.copy()
    result_df["example_sentence"] = result_df["lemma"].map(sentence_lookup)

    return result_df