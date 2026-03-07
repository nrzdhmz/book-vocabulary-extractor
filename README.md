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

## Current Layout
```
backend/
  src/                # all processing modules
  data/raw/book.pdf   # sample input
  outputs/            # generated CSVs
  cli.py              # command-line runner
  requirements.txt
  tests/
notebooks/
  main.ipynb          # exploratory notebook using backend modules
frontend/             # (placeholder for your UI)
```

## Outputs
Written to `backend/outputs/`:
- `ranked_vocabulary_all.csv`
- `ranked_vocabulary_easy.csv`
- `ranked_vocabulary_intermediate.csv`
- `ranked_vocabulary_hard.csv`
- `ranked_vocabulary.csv` (combined)
- `ranked_vocabulary_metadata.json` (run parameters + counts)

Each row includes lemma, POS, frequency, difficulty, definition, and an in-book example sentence.

## Run via CLI
```
cd backend
python cli.py --pdf data/raw/book.pdf --min-frequency 2 --out outputs --base-name ranked_vocabulary
```
Avoid scanned PDFs; text-based PDFs work best.

## Run API (for frontend)
```
cd backend
uvicorn api.main:app --reload --port 8000
```
The endpoint `POST /api/extract` accepts a PDF file (`file`) and `min_frequency` form field, returning `summary` and base64 CSVs (all/easy/intermediate/hard). Enable CORS for local dev (Vite default port 5173).

## Notebook
Open `notebooks/main.ipynb`. It already adds `../backend` to `sys.path` and saves to `../backend/outputs/`.

## Testing
```
cd backend
pytest
```
