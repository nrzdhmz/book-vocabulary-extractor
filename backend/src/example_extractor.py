import re
import spacy
import pandas as pd


nlp = spacy.load("en_core_web_sm")


BAD_PATTERNS = [
    r"\bchapter\b",
    r"\bcontents\b",
    r"\bpraise for\b",
    r"\btable of contents\b",
    r"\bcopyright\b",
    r"\bpublished by\b",
    r"\bintroduction\b",
    r"\bpreface\b",
    r"\backnowledg",
]


def clean_sentence_text(sentence: str) -> str:
    sentence = sentence.replace("\n", " ")
    sentence = re.sub(r"\s+", " ", sentence)
    return sentence.strip()


def uppercase_ratio(text: str) -> float:
    letters = [ch for ch in text if ch.isalpha()]
    if not letters:                                    # to prevent zero division | upper/len(letters) -> Zero division error | 
        return 0.0
    upper = sum(1 for ch in letters if ch.isupper())
    return upper / len(letters)


def is_good_sentence(sentence: str) -> bool:
    sentence = clean_sentence_text(sentence)

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
    if uppercase_ratio(sentence) > 0.35:
        return False
    if sentence.count('"') > 4:
        return False
    if sentence.count("…") > 1:
        return False
    if re.search(r"[A-Z]{4,}", sentence):
        return False

    for pattern in BAD_PATTERNS:
        if re.search(pattern, sentence, re.IGNORECASE):
            return False

    return True


def sentence_score(sentence: str, lemma: str) -> int:
    sentence = clean_sentence_text(sentence)
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


def highlight_lemma_in_sentence(sentence: str, lemma: str) -> str:
    doc = nlp(sentence)

    highlighted_tokens = []

    for token in doc:
        if token.lemma_.lower() == lemma.lower() and token.is_alpha:
            highlighted_tokens.append(f"**{token.text}**")
        else:
            highlighted_tokens.append(token.text)

    text = " ".join(highlighted_tokens)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)

    return text.strip()


def add_example_sentences(vocab_df: pd.DataFrame, text: str) -> pd.DataFrame:
    doc = nlp(text)

    lemma_good_sentences = {}
    lemma_all_sentences = {}

    for sent in doc.sents:
        raw_sentence = sent.text.strip()
        sentence_text = clean_sentence_text(raw_sentence)

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
    sentence_source = {}

    for lemma in vocab_df["lemma"]:
        good_candidates = lemma_good_sentences.get(lemma, [])
        all_candidates = lemma_all_sentences.get(lemma, [])

        if good_candidates:
            best_sentence = max(good_candidates, key=lambda s: sentence_score(s, lemma))
            sentence_source[lemma] = "good"
        elif all_candidates:
            best_sentence = max(all_candidates, key=lambda s: sentence_score(s, lemma))
            sentence_source[lemma] = "fallback"
        else:
            best_sentence = None
            sentence_source[lemma] = "missing"

        selected_sentences[lemma] = best_sentence

    result_df = vocab_df.copy()
    result_df["example_sentence"] = result_df["lemma"].map(selected_sentences)
    result_df["example_sentence"] = result_df.apply(
        lambda row: highlight_lemma_in_sentence(row["example_sentence"], row["lemma"])
        if pd.notna(row["example_sentence"]) else None,
        axis=1
    )
    result_df["example_source"] = result_df["lemma"].map(sentence_source)

    return result_df
