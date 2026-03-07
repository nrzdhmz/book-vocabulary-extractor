import re
import spacy
from spacy.cli import download

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

ASCII_WORD = re.compile(r"^[A-Za-z]+$")


def process_text(text: str):
    doc = nlp(text)

    tokens = []

    for token in doc:
        if not token.is_alpha:
            continue

        # Keep only pure English alphabet (A–Z) words to avoid odd spacy bugs.
        if not token.text.isascii() or not token.lemma_.isascii():
            continue
        if not ASCII_WORD.match(token.text):
            continue

        tokens.append({
            "word": token.text.lower(),
            "lemma": token.lemma_.lower(),
            "pos": token.pos_,
            "is_stop": token.is_stop,
            "ent_type": token.ent_type_,
            "is_title": token.text.istitle(),
        })

    return tokens
