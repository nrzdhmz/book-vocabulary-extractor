import spacy

nlp = spacy.load("en_core_web_sm")

def process_text(text):
    doc = nlp(text)

    tokens = []

    for token in doc:
        if token.is_alpha:
            tokens.append({
                "word": token.text.lower(),
                "lemma": token.lemma_.lower(),
                "pos": token.pos_,
                "is_stop": token.is_stop
            })

    return tokens