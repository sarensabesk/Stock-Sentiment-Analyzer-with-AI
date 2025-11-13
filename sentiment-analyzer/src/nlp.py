from __future__ import annotations
import pandas as pd

# Core Python libraries
import datetime as dt
import time

# Try to import VADER; handle missing packages instead of crashing
try:
    from nltk.sentiment import SentimentIntensityAnalyzer
except ImportError:
    SentimentIntensityAnalyzer = None  # We'll handle this later in get_sia()

# Global variable for caching the analyzer (so we don't re-create it every time)
_sia = None

def get_sia():
    
    global _sia

    if _sia is not None:
        return _sia
    
    _sia = SentimentIntensityAnalyzer()

    try:
        _sia = SentimentIntensityAnalyzer()
    
    except LookupError:
        import nltk
        nltk.download("vader_lexicon")
        _sia = SentimentIntensityAnalyzer()

    
    return _sia





