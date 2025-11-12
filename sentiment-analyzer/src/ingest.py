from __future__ import annotations

import os
import re
import time
import datetime as dt
from typing import Dict, List, Optional

import pandas as pd
import yfinance as yf
import feedparser


#All Downloaded CSV go here
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)


def cache_to_csv(df, name):
    
    if not name.endswith(".csv"): #if the file doesnt end with csv, add it to the end
        name = name + ".csv"
    
    path = os.path.join(DATA_DIR, name) #adds the file into data folder
    
    df.to_csv(path, index=False) #creates csv in path
    
    return os.path.abspath(path) ## converts to absolute path


def _as_date(x):
   return pd.to_datetime(x).date() # removes time to just YYYY-MM-DD
    

def _clean_text(s):
    if not s:
        return ""
    return re.sub(r"\s+", " ", s).strip()

def fetch_prices(ticker, start="2024-01-01", end=None, auto_adjust=True):
    # Download daily Ticker with yfinance and compute daily returns from Adjusted Close.
    # Returns: DataFrame with columns:
    #Date, Open, High, Low, Close, Adj Close, Volume, Return

    if end is None:
        end = dt.date.today().isoformat()

    df = yf.download(
        tickers=ticker,
        start=start,
        end=end,
        progress=False,
        auto_adjust=auto_adjust,
        interval="1d",
    )

    if df.empty:
        raise ValueError(f"No price data returned for {ticker} in range {start}..{end}")

    # Make Date a normal column and normalize to plain date
    df = df.reset_index()
    df["Date"] = df["Date"].apply(_as_date)

    # Ensure Adj Close exists (fallback to Close if needed)
    if "Adj Close" not in df.columns and "Close" in df.columns:
        df["Adj Close"] = df["Close"]

    # Daily percent return from adjusted close
    df["Return"] = df["Adj Close"].pct_change()

    # Reorder columns neatly (keep only those that exist)
    cols = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume", "Return"]
    df = df[[c for c in cols if c in df.columns]]

    return df

    

