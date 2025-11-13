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

    if _sia is not None: #if variable has a value dont change nth
        return _sia
    
    #if it doesnt have that value, then give it that value (sia)
    try:
        _sia = SentimentIntensityAnalyzer()
    
    except LookupError:
        import nltk
        nltk.download("vader_lexicon")
        _sia = SentimentIntensityAnalyzer()

    return _sia

def score_headlines(df):
    #checks to see if valid 

    required = {"Date", "Headline"}
    
    if not required.issubset(df.columns):
        missing = required - set(df.columns)
        raise ValueError(f"Missing required columns: {missing}")

   
    if df.empty:
        return df.copy()
    
    analyzer = get_sia()

    texts = df["Headline"].fillna("").astype(str)

    scores_series = texts.apply(analyzer.polarity_scores) # Series of dicts
    scores_df = pd.DataFrame(scores_series.tolist())  # columns: neg, neu, pos, compound

    out = df.copy()
    out[["pos", "neu", 'neg', 'compound']] = scores_df[["pos", "neu", 'neg', 'compound']]

    return out










