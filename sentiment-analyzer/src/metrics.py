from __future__ import annotations
import pandas as pd
import numpy as np
import datetime as dt


def merge_sentiment_prices(sentiment_df: pd.DataFrame, prices_df: pd.DataFrame) -> pd.DataFrame:
    req_price = {'Date','Open','High','Low','Close','Adj Close','Volume','Return'}
    req_nip = {"Date","avg_pos","avg_neu","avg_neg","avg_compound","headline_count"}

    if not req_price.issubset(prices_df.columns):
        missing = req_price - set(prices_df.columns)
        raise ValueError(f"Missing required columns: {missing}")
    
    if not req_nip.issubset(sentiment_df.columns):
        missing = req_nip - set(sentiment_df.columns)
        raise ValueError(f"Missing required columns: {missing}")
    
    