# Book Vocabulary Extractor

A small NLP project that extracts useful vocabulary from a book (PDF).

## What it does
- Reads a PDF book
- Processes the text with spaCy
- Extracts meaningful words (nouns, verbs, adjectives, adverbs)
- Ranks vocabulary using frequency and word rarity
- Finds example sentences from the book

## Current stage
Prototype built in a notebook.  
Pipeline: **PDF → text → tokens → vocabulary → examples → ranking**

## Tech
Python, spaCy, pandas, wordfreq