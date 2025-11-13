from __future__ import annotations
import pandas as pd
import numpy as np
import datetime as dt


def merge_sentiment_prices(sentiment_df: pd.DataFrame, prices_df: pd.DataFrame) -> pd.DataFrame:
    def merge_sentiment_prices(sentiment_df: pd.DataFrame, prices_df: pd.DataFrame) -> pd.DataFrame:
    
   # Merge daily sentiment with daily prices and compute next-day returns.

    req_px = {'Date','Open','High','Low','Close','Adj Close','Volume','Return'}
    req_sent = {"Date","avg_pos","avg_neu","avg_neg","avg_compound","headline_count"}

    # Validate schemas
    if not req_px.issubset(prices_df.columns):
        missing = req_px - set(prices_df.columns)
        raise ValueError(f"Missing required price columns: {missing}")
    if not req_sent.issubset(sentiment_df.columns):
        missing = req_sent - set(sentiment_df.columns)
        raise ValueError(f"Missing required sentiment columns: {missing}")

    # Normalize Date to plain date (handles strings or timestamps)
    prices_df = prices_df.copy()
    sentiment_df = sentiment_df.copy()
    prices_df["Date"] = pd.to_datetime(prices_df["Date"]).dt.date
    sentiment_df["Date"] = pd.to_datetime(sentiment_df["Date"]).dt.date

    # Deduplicate by Date (keep first seen row per day)
    prices_df = prices_df.drop_duplicates(subset=["Date"], keep="first")
    sentiment_df = sentiment_df.drop_duplicates(subset=["Date"], keep="first")

    # Sort chronologically
    prices_df = prices_df.sort_values("Date").reset_index(drop=True)
    sentiment_df = sentiment_df.sort_values("Date").reset_index(drop=True)

    # Merge on Date; use inner join so both price & sentiment exist
    merged = prices_df.merge(sentiment_df, on="Date", how="inner")

    # Next day return: shift Return *up* so row t has return of t+1
    merged["next_day_return"] = merged["Return"].shift(-1)

    # Drop the last row (no next day available)
    merged = merged.dropna(subset=["next_day_return"]).reset_index(drop=True)

    # Friendly column order (keep extras if present)
    order = ["Date", "avg_compound", "headline_count", "Adj Close", "Return", "next_day_return"]
    merged = merged[[c for c in order if c in merged.columns]]

    return merged
