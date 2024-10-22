# Smart FAQ Module

This repository contains the implementation of a Smart FAQ module that combines traditional keyword-based search (fuzzy matching) with context-aware search using SBERT (Sentence-BERT) for enhanced query matching.

## Features

- **Fuzzy Matching**: Utilizes the `fuzzywuzzy` library to match user queries to FAQs based on string similarity.
- **Context Matching**: Leverages SBERT (Sentence-BERT) to compare user queries and FAQ questions based on semantic meaning using sentence embeddings.
- **Hybrid Approach**: Initially attempts fuzzy matching, and if the match score is below a threshold, context matching is used.
- **Django Backend**: The backend is built using Django, where FAQ data is loaded from a JSON file and served to the search module.

## Requirements
- Python 3.7+
- Django 4.x
- fuzzywuzzy for string matching
- sentence-transformers for context matching using SBERT
- spaCy for natural language processing (NLP) preprocessing
