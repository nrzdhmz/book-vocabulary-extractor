import re
import spacy
import pandas as pd


nlp = spacy.load("en_core_web_sm")


def is_good_sentence(sentence: str) -> bool:
    sentence = sentence.strip()

    if not sentence:
        return False

    if len(sentence) < 40:
        return False

    if len(sentence) > 220:
        return False

    if sentence.isupper():
        return False

    if sentence.count(" ") < 5:
        return False

    if re.search(r"\bchapter\b", sentence, re.IGNORECASE):
        return False

    if re.search(r"\bcontents\b", sentence, re.IGNORECASE):
        return False

    return True


def sentence_score(sentence: str, lemma: str) -> int:
    score = 0
    lowered = sentence.lower()
    word_count = len(sentence.split())

    if lemma in lowered:
        score += 3

    if 8 <= word_count <= 20:
        score += 4
    elif 21 <= word_count <= 30:
        score += 3
    elif 5 <= word_count <= 35:
        score += 2
    else:
        score += 1

    if "," not in sentence:
        score += 1

    if ";" not in sentence and ":" not in sentence:
        score += 1

    if not sentence.isupper():
        score += 1

    return score


def add_example_sentences(vocab_df: pd.DataFrame, text: str) -> pd.DataFrame:
    doc = nlp(text)

    lemma_good_sentences = {}
    lemma_all_sentences = {}

    for sent in doc.sents:
        sentence_text = sent.text.strip()

        if not sentence_text:
            continue

        lemmas_in_sentence = set()

        for token in sent:
            if not token.is_alpha:
                continue

            lemma = token.lemma_.lower().strip()

            if len(lemma) < 3:
                continue

            lemmas_in_sentence.add(lemma)

        for lemma in lemmas_in_sentence:
            lemma_all_sentences.setdefault(lemma, []).append(sentence_text)

            if is_good_sentence(sentence_text):
                lemma_good_sentences.setdefault(lemma, []).append(sentence_text)

    selected_sentences = {}

    for lemma in vocab_df["lemma"]:
        good_candidates = lemma_good_sentences.get(lemma, [])
        all_candidates = lemma_all_sentences.get(lemma, [])

        if good_candidates:
            best_sentence = max(good_candidates, key=lambda s: sentence_score(s, lemma))
        elif all_candidates:
            best_sentence = max(all_candidates, key=lambda s: sentence_score(s, lemma))
        else:
            best_sentence = None

        selected_sentences[lemma] = best_sentence

    result_df = vocab_df.copy()
    result_df["example_sentence"] = result_df["lemma"].map(selected_sentences)

    return result_df