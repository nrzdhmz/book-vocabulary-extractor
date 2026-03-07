# Book Vocabulary Extractor

This project extracts useful vocabulary from a **book PDF** and generates a ranked vocabulary list with **example sentences and definitions**.

## How It Works

The pipeline processes a book in several stages:

1. **PDF Extraction**  
   The PDF is read using **PyMuPDF**, and all text is extracted.

2. **Text Processing**  
   The text is analyzed with **spaCy** to identify tokens, lemmas (base forms), and parts of speech.

3. **Vocabulary Filtering**  
   Tokens are filtered to keep meaningful words only:
   - nouns, verbs, adjectives, adverbs  
   - non-stopwords  
   - not named entities (people, places, organizations)

4. **Vocabulary Building**  
   Words are grouped by **lemma + part of speech** and their frequency in the book is counted.

5. **Example Sentences**  
   The pipeline finds good sentences from the book that contain each word.

6. **Ranking & Difficulty**  
   Words are ranked using:
   - frequency in the book
   - global English frequency (`wordfreq`)
   - part-of-speech weighting

7. **Definitions**  
   Definitions are added using **WordNet (NLTK)**.

## Output

The pipeline exports CSV files containing vocabulary data:

- `ranked_vocabulary_all.csv`
- `ranked_vocabulary_easy.csv`
- `ranked_vocabulary_intermediate.csv`
- `ranked_vocabulary_hard.csv`

Each entry includes:
- lemma
- part of speech
- frequency
- example sentence
- difficulty level
- definition

## Tech Stack

- Python
- spaCy
- PyMuPDF
- pandas
- wordfreq
- NLTK